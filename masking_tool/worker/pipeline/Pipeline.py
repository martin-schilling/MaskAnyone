import os
import time
from config import (
    BLENDSHAPES_BASE_PATH,
    RESULT_BASE_PATH,
    TS_BASE_PATH,
    VIDEOS_BASE_PATH,
)
import json
from backend_client import BackendClient
from pipeline.mask_extraction.DockerMaskExtractor import DockerMaskExtractor
from pipeline.ModelFactory import ModelFactory, ModelType
from pipeline.mask_extraction.MediaPipeMaskExtractor import MediaPipeMaskExtractor

from pipeline.detection.YoloDetector import YoloDetector
from pipeline.detection.MediaPipeDetector import MediaPipeDetector
from utils.drawing_utils import overlay_frames
from pipeline.hiding import Hider
from pipeline.PipelineTypes import (
    DetectionResult,
    HidingStategies,
    MaskingResult,
    Params3D,
    PartToDetect,
    PartToMask,
    RunParams,
)
from utils.video_utils import setup_video_processing
from utils.app_utils import save_preview_image
from models.docker_maskers import docker_maskers as known_docker_mask_extractors

import cv2


class Pipeline:
    def __init__(self, run_params: RunParams, backend_client: BackendClient):
        self.backend_client = backend_client
        self.ts_file_handlers = {}

        self.model_3d_only = False
        self.blendshapes_file_handle = None

        self.num_frames = 0
        self.progress_message_sent_time = None
        self.progress_update_interval = 5  # in seconds

        params_3d: Params3D = run_params["threeDModelCreation"]
        video_masking_params = run_params["videoMasking"]

        model_factory = ModelFactory()
        target_detection_model = video_masking_params.hiding_strategy_target.params[
            "detection_model"
        ]
        target_detection_params = video_masking_params.hiding_strategy_target.params[
            "detection_params"
        ]
        target_detection_params["target"] = video_masking_params.hiding_target
        self.detector_target = model_factory.make_model(
            target_detection_model, ModelType.DETECTION, target_detection_params
        )
        if not self.detector_target.target == "body":
            self.detector_bg = model_factory.make_model(
                target_detection_model, ModelType.DETECTION, target_detection_params
            )
        else:
            self.detector_bg = None

        self.mask_extractor = model_factory.make_model(
            video_masking_params.masking_strategy.key,
            ModelType.MASKING,
            video_masking_params.masking_strategy.params,
        )

        self.hider_target = Hider(run_params.video_masking.hiding_strategy_target)
        self.hider_bg = Hider(run_params.video_masking.hiding_strategy_background)

    def init_ts_file_handlers(self, video_id: str):
        for mask_extractor in self.mask_extractors:
            for part_to_mask in mask_extractor.parts_to_mask:
                if part_to_mask["save_timeseries"]:
                    file_path = os.path.join(
                        TS_BASE_PATH, f"{part_to_mask['part_name']}_{video_id}.json"
                    )
                    file_handle = open(file_path, "w+", newline="")
                    file_handle.write("[")
                    self.ts_file_handlers[part_to_mask["part_name"]] = file_handle

    def init_blendshapes_file_handle(self, video_id: str):
        file_path = os.path.join(BLENDSHAPES_BASE_PATH, f"{video_id}.json")
        file_handle = open(file_path, "w+", newline="")
        file_handle.write("[")
        self.blendshapes_file_handle = file_handle

    def write_timeseries(self, timeseries: dict, first: bool):
        for part_name in timeseries:
            file_handle = self.ts_file_handlers[part_name]
            if not first:
                file_handle.write(",")
            json_string = json.dumps(timeseries[part_name])
            file_handle.write(json_string)

    def close_ts_file_handles(self):
        for key in self.ts_file_handlers:
            self.ts_file_handlers[key].write("]")
            self.ts_file_handlers[key].close()

    def close_bs_file_handle(self):
        self.blendshapes_file_handle.write("]")
        self.blendshapes_file_handle.close()

    def write_blendshapes(self, blendshapes_dict, first):
        if blendshapes_dict:
            if not first:
                self.blendshapes_file_handle.write(",")
            json_string = json.dumps(blendshapes_dict)
            self.blendshapes_file_handle.write(json_string)

    def should_send_progress_message(self, index: int):
        if index == 0:
            return False

        if self.progress_message_sent_time is None:
            return True

        cur_time = time.time()
        elapsed_time = cur_time - self.progress_message_sent_time
        return elapsed_time > self.progress_update_interval

    def send_progress_update(self, job_id: str, current_index: int):
        if self.should_send_progress_message(current_index):
            progress = int((float(current_index) / float(self.num_frames)) * 100.0)
            self.backend_client.update_progress(job_id, progress)
            self.progress_message_sent_time = time.time()

    def run(self, video_id: str, job_id: str):
        print(f"Running job on video {video_id}")
        video_in_path = os.path.join(VIDEOS_BASE_PATH, video_id + ".mp4")
        video_out_path = os.path.join(RESULT_BASE_PATH, video_id + ".mp4")

        if isinstance(self.mask_extractor, DockerMaskExtractor):
            self.backend_client.create_job(
                self.mask_extractor.model_name, video_id, {"arg1": "someVal"}
            )

        video_cap, out = setup_video_processing(video_in_path, video_out_path)
        is_first_frame = True

        self.init_ts_file_handlers(video_id)
        self.init_blendshapes_file_handle(video_id)
        self.num_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        index = 0

        if not self.detectors and not self.mask_extractors:
            # Nothing to do
            return

        while True:
            ret, frame = video_cap.read()
            if not ret:
                break

            frame_timestamp_ms = int(video_cap.get(cv2.CAP_PROP_POS_MSEC))
            if not is_first_frame and frame_timestamp_ms == 0:
                continue

            # Detect all targets / background (as pixel masks)
            if self.detector_target:
                detection_result_target = self.detector_target.detect_target(
                    frame, frame_timestamp_ms
                )
            if self.detector_target.target == "body":
                detection_result_bg = 1 - detection_result_target
            else:
                detection_result_bg = 1 - self.detector_bg.detect_target(
                    frame, frame_timestamp_ms
                )

            # applies the hiding method on each detected part of the frame and combines them into one frame
            hidden_frame = frame.copy()
            hidden_frame = self.hider_bg.hide(hidden_frame, detection_result_bg["mask"])
            hidden_frame = self.hider_target.hide(
                hidden_frame, detection_result_target["mask"]
            )

            # Extracts the masks for each desired bodypart
            if self.mask_extractor and not isinstance(
                self.mask_extractor, DockerMaskExtractor
            ):
                masking_result: MaskingResult = self.mask_extractor.extract_mask(
                    frame, frame_timestamp_ms
                )
                self.write_timeseries(
                    self.mask_extractor.get_newest_timeseries(), is_first_frame
                )
                self.write_blendshapes(
                    self.mask_extractor.get_newest_blendshapes(), is_first_frame
                )

                if not self.model_3d_only:
                    out_frame = overlay_frames(hidden_frame, [masking_result["mask"]])
                    out.write(out_frame)

            is_first_frame = False
            self.send_progress_update(job_id, index)
            index += 1

        self.close_ts_file_handles()
        self.close_bs_file_handle()
        out.release()
        video_cap.release()
        print(f"Finished processing video {video_id}")

        if not self.model_3d_only:
            save_preview_image(video_out_path)

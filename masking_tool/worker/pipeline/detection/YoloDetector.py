import os
from typing import List, Literal
import numpy as np
import cv2
from utils.drawing_utils import draw_rectangle, overlay_segmask, yolo_draw_segmask
from pipeline.PipelineTypes import PartToDetect
from pipeline.detection.BaseDetector import BaseDetector

from ultralytics import YOLO

# @ToDo unifify models into one model with different classes?
body_bbox_model_path = os.path.join("models", "yolov8n.pt")
face_bbox_model_path = os.path.join("models", "yolov8n-face.pt")
seg_model_path = os.path.join("models", "yolov8n-seg.pt")


class YoloDetector(BaseDetector):
    def __init__(
        self,
        target: Literal["face", "body"],
        detection_type: Literal["silhouette", "bbox"],
        detection_params: dict,
    ):
        super().__init__(target, detection_type, detection_params)
        self.silhouette_methods = {
            "body": self.detect_body_silhouette,
        }
        self.boundingbox_methods = {
            "body": self.detect_body_bbox,
            "face": self.detect_face_bbox,
        }
        self.model = None

    def detect_body_bbox(self, frame: np.ndarray, timestamp_ms: int) -> np.ndarray:
        if not self.model:
            self.model = YOLO(body_bbox_model_path)
        # Returns the segmentation mask for the body [black / white]
        results = self.model.predict(frame, classes=[0])
        output_image = np.zeros((frame.shape))
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = [int(val) for val in box.xyxy[0].tolist()]
                output_image = draw_rectangle(output_image, x1, y1, x2, y2, 1)
        return output_image

    def detect_face_bbox(self, frame: np.ndarray, timestamp_ms: int) -> np.ndarray:
        if not self.model:
            self.model = YOLO(face_bbox_model_path)
        # Returns the segmentation mask for the body [black / white]
        results = self.model.predict(frame)
        output_image = np.zeros((frame.shape))
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = [int(val) for val in box.xyxy[0].tolist()]
                output_image = draw_rectangle(output_image, x1, y1, x2, y2, 1)
        return output_image

    def detect_body_silhouette(
        self, frame: np.ndarray, timestamp_ms: int
    ) -> np.ndarray:
        if not self.model:
            self.model = YOLO(seg_model_path)
        results = self.models["silhouette"].predict(frame)
        output_image = np.zeros((frame.shape))
        if not results:
            return output_image
        for r in results:
            masks = r.masks.masks
            if masks is not None:
                masks = masks.data.cpu()
                h, w, _ = frame.shape
                for seg in masks.data.cpu().numpy():
                    seg = cv2.resize(seg, (w, h))
                    output_image = overlay_segmask(output_image, seg, 1, 0.4)
        return output_image

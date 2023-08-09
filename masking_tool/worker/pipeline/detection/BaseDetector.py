from typing import List, Literal

from pipeline.PipelineTypes import DetectionResult
import numpy as np


class BaseDetector:
    def __init__(
        self,
        target: Literal["face", "body"],
        detection_type: Literal["silhouette", "bbox"],
        detection_params: dict,
    ):
        self.target = target
        self.detection_type = detection_type
        self.detection_params = detection_params
        self.silhouette_methods = {}
        self.bbox_methods = {}

    def detect(self, frame: np.ndarray, timestamp_ms: int) -> List[np.ndarray]:
        if self.detection_type == "bbox":
            return self.detect_boundingbox(frame, timestamp_ms)
        elif self.detection_type == "silhouette":
            return self.detect_silhouette(frame, timestamp_ms)
        else:
            raise Exception("Invalid detection type")

    def detect_silhouette(self, frame: np.ndarray, timestamp_ms: int) -> np.ndarray:
        # Detects the Silhouette of a certain video_part (e.g head, body...)
        if self.target not in self.silhouette_methods:
            raise Exception(
                f"Detection model does not support silhouette detection for target: {self.target}"
            )
        return self.silhouette_methods[self.target](frame, timestamp_ms)

    def detect_boundingbox(self, frame: np.ndarray, timestamp_ms: int) -> np.ndarray:
        # Detects the Boundingbox of a certain video_part (e.g head, body...)
        if self.target not in self.bbox_methods:
            raise Exception(
                f"Detection model does not support bounding-box detection for video_part: {self.target}"
            )
        return self.bbox_methods[self.target](frame, timestamp_ms)

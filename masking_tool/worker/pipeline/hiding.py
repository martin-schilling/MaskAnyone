import numpy as np
import cv2

from pipeline.PipelineTypes import (
    Strategy,
)


class Hider:
    def __init__(self, hiding_strategy: Strategy):
        self.hiding_strategy = hiding_strategy

    def hide(self, base_image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        if self.hiding_strategy.key == "blur":
            return self.hide_blur(base_image, mask, self.hiding_strategy.params)
        elif self.hiding_strategy.key == "blackout":
            return self.hide_blackout(base_image, mask, self.hiding_strategy.params)
        else:
            raise Exception("Invalid hiding strategy")

    def hide_blur(
        self, base_image: np.ndarray, mask: np.ndarray, params: dict
    ) -> np.ndarray:
        blurred_image = cv2.GaussianBlur(
            base_image, (int(params["kernelSize"]), int(params["kernelSize"])), 30
        )
        base_image[mask != 0] = blurred_image[mask != 0]
        return base_image

    def hide_blackout(
        self, base_image: np.ndarray, mask: np.ndarray, params: dict
    ) -> np.ndarray:
        base_image[mask != 0] = int(params["color"])
        return base_image

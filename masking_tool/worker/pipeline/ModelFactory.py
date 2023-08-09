from pipeline.mask_extraction.DockerMaskExtractor import DockerMaskExtractor
from pipeline.mask_extraction.MediaPipeMaskExtractor import MediaPipeMaskExtractor
from pipeline.detection.MediaPipeDetector import MediaPipeDetector
from pipeline.detection.YoloDetector import YoloDetector


class ModelType:
    DETECTION = 1
    MASKING = 2


model_detection_lookup = {
    "yolo": YoloDetector,
    "mediapipe": MediaPipeDetector,
}


class ModelFactory:
    def get_detection_model(self, model_name, model_params):
        detection_models = {
            "none": None,
            "yolo": YoloDetector(model_params),
            "mediapipe": MediaPipeDetector(model_params),
        }
        return detection_models[model_name]

    def get_masking_model(self, model_name, model_params):
        masking_models = {
            "none": None,
            "mediapipe": MediaPipeMaskExtractor(model_params),
            "vibe": DockerMaskExtractor("vibe"),
        }
        return masking_models[model_name]

    def make_model(self, model_name, model_type, model_params):
        if model_type == ModelType.DETECTION:
            return self.get_detection_model(model_name, model_params)
        elif model_type == ModelType.MASKING:
            return self.get_masking_model(model_name, model_params)
        else:
            raise Exception("Invalid model type")

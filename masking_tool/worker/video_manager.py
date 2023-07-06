from backend_client import BackendClient
from local_data_manager import LocalDataManager
import os


class VideoManager:
    __backend_client: BackendClient
    __local_data_manager: LocalDataManager

    def __init__(
        self, backend_client: BackendClient, local_data_manager: LocalDataManager
    ):
        self.__backend_client = backend_client
        self.__local_data_manager = local_data_manager

    def load_original_video(self, video_id: str):
        video_data = self.__backend_client.fetch_video(video_id)
        self.__local_data_manager.write_binary(
            os.path.join("original", video_id + ".mp4"), video_data
        )

    def upload_result_video(self, video_id: str, result_video_id: str):
        video_data = self.__local_data_manager.read_binary(
            os.path.join("results", video_id + ".mp4")
        )
        self.__backend_client.upload_result_video(video_id, result_video_id, video_data)

    def upload_result_video_preview_image(self, video_id: str, result_video_id: str):
        image_data = self.__local_data_manager.read_binary(
            os.path.join("results", video_id + ".png")
        )
        self.__backend_client.upload_result_video_preview_image(
            video_id, result_video_id, image_data
        )

    def cleanup_result_video_files(self, video_id: str):
        self.__local_data_manager.delete_file(
            os.path.join("results", video_id + ".mp4")
        )
        self.__local_data_manager.delete_file(
            os.path.join("results", video_id + ".png")
        )
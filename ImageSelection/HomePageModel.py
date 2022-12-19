import os

from Utils.CycleManager import CycleManager


class HomePageModel:

    MINIATURE_FOLDER = r".\.Miniatures"

    def __init__(self) -> None:
        self._current_folder = self.MINIATURE_FOLDER
        self._folder_content_map = {}
        self._folder_content_count = None

    def add_folder_content(self, folder: str, content: list) -> None:
        self._folder_content_map[folder] = content

    def get_folder_content(self, folder: str) -> list:
        return self._folder_content_map[folder]
    
    def set_current_folder(self, folder: str) -> None:
        self._current_folder = folder

    def get_current_folder(self) -> str:
        return self._current_folder

    def get_full_path_current_folder(self) -> str:
        return os.path.abspath(self.get_current_folder())

    def reset_file_count(self) -> None:
        self._folder_content_count = None

    def get_file(self):
        file = []
        for item in os.listdir(self._current_folder):
            if item.lower().endswith(("jpg", 'png')):
                file.append(item)
        self._folder_content_count = len(file)
        return file

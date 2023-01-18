import os

from Core.AppModel import AppModel


class HomePageModel:

    LOADED = "loaded"
    COUNT = "count"

    def __init__(self) -> None:
        self._current_folder = ".\\" + AppModel.MINIATURE_FOLDER
        self._folder_loading_state = {}
        self._folder_content_count = None
        self._selected_images = set()

        self.set_current_folder(self.get_full_path_current_folder())
    
    def set_current_folder(self, folder: str) -> None:
        self._current_folder = folder
        if self.get_full_path_current_folder() not in self._folder_loading_state:
            self._folder_loading_state[self.get_full_path_current_folder()] = {self.LOADED: False, self.COUNT: 0}

    def update_image_selection_state(self, path: str, state: bool) -> None:
        if state:
            self._selected_images.add(path)
        else:
            try:
                self._selected_images.remove(path)
            except Exception:
                pass

    def get_selected_images(self) -> list:
        return self._selected_images

    def get_current_folder(self) -> str:
        return self._current_folder

    def get_folder_loading_state(self) -> dict:
        return self._folder_loading_state[self.get_full_path_current_folder()]

    def set_current_folder_as_loaded(self) -> None:
        self._folder_loading_state[self.get_full_path_current_folder()][self.LOADED] = True

    def increment_current_folder_loaded_file_count(self) -> None:
        self._folder_loading_state[self.get_full_path_current_folder()][self.COUNT] += 1

    def get_full_path_current_folder(self) -> str:
        return os.path.abspath(self.get_current_folder())

    def get_full_resource_path_current_folder(self) -> str:
        return self.get_full_path_current_folder().replace(AppModel.MINIATURE_FOLDER, AppModel.RESOURCES_FOLDER)

    def reset_file_count(self) -> None:
        self._folder_content_count = None

    def get_file(self):
        file = []
        for item in os.listdir(self._current_folder):
            if item.lower().endswith(("jpg", 'png')):
                file.append(item)
        self._folder_content_count = len(file)
        return file

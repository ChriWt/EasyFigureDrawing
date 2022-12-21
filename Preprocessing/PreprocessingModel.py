from __future__ import annotations
import os
import shutil
import typing
from pathlib import Path 

from PIL import Image, ImageTk
from Utils.CycleManager import CycleManager

if typing.TYPE_CHECKING:
    from Preprocessing.PreprocessingController import PreprocessingController

class PreprocessingModel:

    VERTICAL_PHOTO_WIDTH = 160 
    VERTICAL_PHOTO_HEIGHT = 240

    HORIZONTAL_PHOTO_WIDTH = 240
    HORIZONTAL_PHOTO_HEIGHT = 360

    def __init__(self, controller: PreprocessingController) -> None:
        self._controller = controller
        self._view = self._controller.get_view()

        self._app_model = self._controller.get_core().get_model()
        
        self._file_to_add = []
        self._file_to_remove = []
        self._folder_to_add = []
        self._folder_to_remove = []

    def calculate_differences_in_folders(self) -> None:
        resource_folder_walk = os.walk(self._app_model.RESOURCES_FOLDER)
        cycle_manager = CycleManager.get_instance()
        
        def cycle():
            self._view.increase_progressbar()
            try:
                resources_folder, resources_subfolder, resources_content = next(resource_folder_walk)
                resource_content = set(resources_content)
                resources_subfolder = set(resources_subfolder)

                miniature_path = self.get_miniature_path(resources_folder)
                
                try:
                    miniature_folder, miniature_subfolder, miniature_content = next(os.walk(miniature_path))
                    miniature_content = set(miniature_content)
                    miniature_subfolder = set(miniature_subfolder)

                    if res := resource_content - miniature_content:
                        self._file_to_add += [os.path.join(self.get_resource_path(miniature_path), x) for x in res]
                    
                    if res := miniature_content - resource_content:
                        self._file_to_remove += [os.path.join(miniature_path, x) for x in res]

                    if res := resources_subfolder - miniature_subfolder:
                        self._folder_to_add += [os.path.join(miniature_folder, x) for x in res]

                    if res := miniature_subfolder - resources_subfolder:
                        self._folder_to_remove += [os.path.join(miniature_folder, x) for x in res]

                except StopIteration:
                    self._folder_to_add.append(miniature_path)
                    self._file_to_add += [os.path.join(self.get_resource_path(resources_folder), x) for x in resources_content]
                
                cycle_manager.after(1, cycle)

            except StopIteration:
                self._view.set_label_text("Done!")
                self._controller.on_calculate_item_differences()
                
        cycle()

    def start_processing(self):
        self.remove_folders()

    def remove_folders(self):
        cycle_manager = CycleManager.get_instance() 

        def cycle(i: int=0):
            if i == len(self._folder_to_remove):
                self._controller.on_folder_remove_complete()
                return
            self._view.increase_progressbar()
            shutil.rmtree(self._folder_to_remove[i])
            cycle_manager.after(1, lambda: cycle(i + 1))
        
        cycle()

    def create_missing_folder(self) -> None:
        cycle_manager = CycleManager.get_instance() 

        def cycle(i: int=0):
            if i == len(self._folder_to_add):
                self._controller.on_folder_creation_complete()
                return
            self._view.increase_progressbar()
            Path(self._folder_to_add[i]).mkdir(parents=True, exist_ok=True)
            cycle_manager.after(1, lambda: cycle(i + 1))
        
        cycle()

    def delete_files(self) -> None:
        cycle_manager = CycleManager.get_instance() 

        def cycle(i: int=0):
            if i == len(self._file_to_remove):
                self._controller.on_file_delete_complete()
                return
            self._view.increase_progressbar()
            os.remove(self._file_to_remove[i])
            cycle_manager.after(1, lambda: cycle(i + 1))
        
        cycle()

    def copy_files(self) -> None:
        cycle_manager = CycleManager.get_instance() 
        item_count = len(self._file_to_add)
        self._view.set_progressbar_type(self._view.DETERMINATED)

        def cycle(i: int=0):
            if i == item_count:
                self._controller.on_file_copy_complete()
                return
            self._view.set_progressbar_value((i + 1) / item_count * 100)
            self._view.set_label_text(f"Croping images... {i + 1}/{item_count}")

            file = self._file_to_add[i]
            self._crop_and_save_image(file, self.get_miniature_path(file))
            cycle_manager.after(1, lambda: cycle(i + 1))
        
        cycle()

    def _crop_and_save_image(self, image: str, destination: str) -> None:
        image = Image.open(image)
        width, height = image.size

        if height > width:
            image.thumbnail(size=(self.VERTICAL_PHOTO_WIDTH, self.VERTICAL_PHOTO_HEIGHT))
        else:
            image.thumbnail(size=(self.HORIZONTAL_PHOTO_WIDTH, self.HORIZONTAL_PHOTO_HEIGHT))

        image.save(destination)

    def get_miniature_path(self, resource_path: str) -> str:
        return os.path.abspath(resource_path).replace(self._app_model.RESOURCES_FOLDER, self._app_model.MINIATURE_FOLDER)

    def get_resource_path(self, miniature_path: str) -> str:
        return miniature_path.replace(self._app_model.MINIATURE_FOLDER, self._app_model.RESOURCES_FOLDER)

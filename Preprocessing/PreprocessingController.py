from __future__ import annotations

import typing
from Preprocessing.PreprocessingModel import PreprocessingModel

from Preprocessing.PreprocessingView import PreprocessingView

if typing.TYPE_CHECKING:
    from Core.AppController import AppController


class PreprocessingController:

    def __init__(self, app_controller: AppController) -> None:
        self._app_controller = app_controller

        self._view = PreprocessingView(self)
        self._model = PreprocessingModel(self)

        self._view.set_progressbar_type(self._view.INDETERMINATED)
        self._view.set_label_text("Calculating differences...")
        self._model.calculate_differences_in_folders()

    def on_calculate_item_differences(self) -> None:
        self._view.set_label_text("Deleting non existing folders...")
        self._model.start_processing()

    def on_folder_remove_complete(self) -> None:
        self._view.set_label_text("Creating missing folders...")
        self._model.create_missing_folder()

    def on_folder_creation_complete(self) -> None:
        self._view.set_label_text("Deleting non existing files...")
        self._model.delete_files()

    def on_file_delete_complete(self) -> None:
        self._view.set_label_text("Croping images... 0/0")
        self._model.copy_files()
    
    def on_file_copy_complete(self) -> None:
        self._app_controller.on_preprocessing_end()

    def get_view(self) -> PreprocessingView:
        return self._view

    def get_core(self) -> AppController:
        return self._app_controller

    
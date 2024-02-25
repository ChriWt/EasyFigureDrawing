from __future__ import annotations
import os
from Core.AppModel import AppModel
from ImageSelection.HomePageModel import HomePageModel
from ImageSelection.HomePageView import HomePageView

import typing

from Utils.CycleManager import CycleManager

if typing.TYPE_CHECKING:
    from Core.AppController import AppController


class HomePageController:

    def __init__(self, core: AppController) -> None:
        self._core = core

        self._view = HomePageView(self)
        self._model = HomePageModel()

        self._init_folder_view()
        self.display_folder_content()

    def _init_folder_view(self) -> None:
        folders = self._get_only_directories()
        
        self._view.set_path(os.path.abspath(self._model.get_current_folder()).replace(self._core.get_model().MINIATURE_FOLDER, self._core.get_model().RESOURCES_FOLDER))
        parent = os.path.basename(self._model.get_current_folder()).replace(AppModel.MINIATURE_FOLDER, AppModel.RESOURCES_FOLDER)
        self._view.insert_folder_content(parent=parent, folders=folders, add_back=False)

    def display_folder_content(self) -> None:
        load_start_index = 0

        folder = self._model.get_full_path_current_folder()
        self._view.hide_current_directory_content()

        if self._view.is_directory_loaded(folder):
            if self._model.get_folder_loading_state()[self._model.LOADED]:
                self._view.show_directory_loaded(folder)
                return
            else:
                load_start_index = self._model.get_folder_loading_state()[self._model.COUNT]
        
        if load_start_index == 0: 
            self._view.new_directory_container(folder)
        else:
            self._view.show_directory_loaded(folder)

        content = self._model.get_file()
        if not content:
            return
        size = len(content)
        manager = CycleManager.get_instance()

        self._view.change_container_size(size)
        self._view.change_progress_bar_state(True)

        def adding_cycle(i=0):
            
            if i == len(content):
                self._model.set_current_folder_as_loaded()
                self._view.change_progress_bar_state(False)
                self._view.update_frame_size(folder)
                return

            path = os.path.abspath(os.path.join(self._model.get_current_folder(), content[i]))
           
            self._view.add_new_element(path)
            self._model.increment_current_folder_loaded_file_count()
            self._view.update_progress_bar(i + 1, size)
            manager.after(1, lambda: adding_cycle(i + 1))

        adding_cycle(load_start_index)

    def on_start_click(self) -> None:
        model = self._core.get_model()
        model.set_references(list(self._model.get_selected_images()))
        model.set_time(int(self._view.get_minutes()) * 60 + int(self._view.get_seconds()))
        CycleManager.get_instance().stop_all()
        self._core.get_core().start_figure_drawing()

    def select_from_current_folder(self, quantity: int) -> None:
        current_folder = self._view.get_directory_loaded()[self._model.get_full_path_current_folder()]
        current_folder.select_random(quantity)

    def _go_to(self, folder: str) -> None:
        self._view.clear_folders()
        self._model.set_current_folder(os.path.join(self._model.get_current_folder(), folder))
        path = os.path.abspath(self._model.get_current_folder())

        parent = os.path.basename(path).replace(AppModel.MINIATURE_FOLDER, AppModel.RESOURCES_FOLDER)
        folders = self._get_only_directories()
        add_back = not os.path.samefile(self._model.get_current_folder(), self._core.get_model().MINIATURE_FOLDER)
        
        self._view.set_path(path.replace(self._core.get_model().MINIATURE_FOLDER, self._core.get_model().RESOURCES_FOLDER))
        self._view.insert_folder_content(parent=parent, folders=folders, add_back=add_back)
        self._view.change_progress_bar_state(False)
        self.display_folder_content()

    def on_open_current_folder_click(self, *_):
        path = self._model.get_full_resource_path_current_folder()
        os.startfile(path)

    def _on_checkbutton_press(self, path: str, state: bool) -> None:
        self._model.update_image_selection_state(path, state)
        selection_count = len(self._model.get_selected_images())
        self._view.update_item_selected_count(selection_count)
        self._view.enable_start_button(selection_count > 0)

    def _get_only_directories(self) -> list:
        basepath = os.path.abspath(self._model.get_current_folder())
        return [content for content in os.listdir(self._model.get_current_folder()) 
                   if os.path.isdir(os.path.join(basepath, content))]

    def on_directory_click(self, item: str) -> None:
        symbol, *folder = item.split(' ')
        CycleManager.get_instance().stop_all()
        self._model.reset_file_count()
        self._view.update_progress_bar(0, 0)
        self._go_to(' '.join(folder))

    def get_model(self) -> HomePageModel:
        return self._model

    def get_view(self) -> HomePageView:
        return self._view

    def get_core(self) -> AppController:
        return self._core
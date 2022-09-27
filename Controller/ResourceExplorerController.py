from __future__ import annotations
import os
import typing
from Controller.PreprocessController import PreprocessController
from Controller.TimelineManager import TimelineManager

from View.NewView import ResourceExplorerView

if typing.TYPE_CHECKING:
    from customtkinter import CTk

from Model.ResourceExplorerModel import ResourceExplorerModel

class ResourceExplorerController:
    
    def __init__(self, root) -> None:
        self._root = root
        self._model = ResourceExplorerModel()
        self._view = ResourceExplorerView(self)

        self._clear_placeholder_files()
        
        self._folder_content_loaded = list()

        self._timeline = TimelineManager.get_instance()
        
        self._view.add_folder_to_tree(self._model.MINIATURE)

    def _add_folder_content(self, path = ""):
        if path in self._folder_content_loaded: 
            self._view.pack_current_folder()
            return

        self._folder_content_loaded.append(path)
        content = os.listdir(path)

        def add_if_folder(i=0):
            if i == len(content): 
                return
            
            element = content[i]
            
            file_path = os.path.join(path, element)

            if os.path.isdir(file_path):
                self._view.add_folder_to_tree(element)
            else:
                self._view.add_folder_content(file_path, file_path.replace(self._model.MINIATURE, self._model.RESOURCES))
            
            self._timeline.after(1, lambda: add_if_folder(i + 1))

        add_if_folder()

    def get_root_window(self) -> CTk:
        return self._root.get_window()

    def on_image_click(self, file):
        if self._model.is_image_already_saved(file):
            self._model.remove_image(file)
        else:
            self._model.add_image(file)

    def add_all(self, path):
        self._model.add_all(path)

    def on_load_request(self, path):
        self._add_folder_content(path)

    def remove_all(self, path):
        self._model.remove_all(path)

    def preprocess_images(self):
        PreprocessController(self._root, self._model)

    def _clear_placeholder_files(self):
     
        def delete(file):
            if os.path.exists(file):
                os.remove(file)

        file = os.path.join(self._model.RESOURCES, ".gitkeep")
        delete(file)
        file = os.path.join(self._model.MINIATURE, ".gitkeep")
        delete(file)
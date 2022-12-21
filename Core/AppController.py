from __future__ import annotations

import typing
from Core.AppModel import AppModel

from Utils.CycleManager import CycleManager

if typing.TYPE_CHECKING:
    from Utils.SizeChangeListener import SizeChangeListener

from Core.AppView import AppView


class AppController:

    def __init__(self, core) -> None:
        self._core = core

        self._view = AppView(self)
        self._model = AppModel()
        self._cycle_manager = CycleManager.get_instance()
        self._cycle_manager.set_root(self._view.get_root())
        
        self._size_change_listeners = []

    def add_size_change_listener(self, listener: SizeChangeListener) -> None:
        if listener not in self._size_change_listeners:
            self._size_change_listeners.append(listener)
    
    def remove_size_change_listener(self, listener: SizeChangeListener) -> None:
        if listener in self._size_change_listeners:
            self._size_change_listeners.remove(listener)

    def on_size_change(self) -> None:
        size = self._view.get_size()
        for listener in self._size_change_listeners:
            listener.update(size)

    def get_view(self) -> AppView:
        return self._view
    
    def get_model(self) -> AppModel:
        return self._model

    def on_preprocessing_end(self):
        self._core.start_home_page()

    def start(self):
        self._view.start()
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from Core.AppController import AppController

from DrawingSession.FigureDrawingModel import FigureDrawingModel
from DrawingSession.FigureDrawingView import FigureDrawingView


class FigureDrawingController:

    def __init__(self, core: AppController) -> None:
        self._core = core
        self._view = FigureDrawingView(self)
        self._model = FigureDrawingModel(self._core.get_model())

        self._view.set_selected_count(self._model.get_reference_count())
        self._view.set_image(self._model.get_reference(0))
        self._view.set_current_image(self._model.get_current_image_index())
        self._view.start_timer(self._model.get_timer())
        self._view.start()
    
    def on_display_next(self):
        image = self._model.get_next()
        if image:
            self._view.stop_timer()
            self._view.set_image(image)
            self._view.set_current_image(self._model.get_current_image_index())
            self._view.start_timer(self._model.get_timer())

    def on_timer_end(self):
        self.on_display_next()

    def update_random_flag(self, flag: bool):
        self._model.set_random_flag(flag)

    def on_display_previous(self):
        image = self._model.get_previous()
        if image:
            self._view.stop_timer()
            self._view.set_image(image)
            self._view.set_current_image(self._model.get_current_image_index())
            self._view.start_timer(self._model.get_timer())
    
    def on_size_update(self) -> None:
        self._view.set_image(self._model.get_current_reference())

    def get_core(self):
        return self._core
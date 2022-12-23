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
        self._model = FigureDrawingModel(self._core.get_model().get_references())

        self._view.set_image(self._model.get_reference(0))
        self._view.start()
    
    def on_display_next(self):
        image = self._model.get_next()
        if image:
            self._view.set_image(image)

    def on_display_previous(self):
        image = self._model.get_previous()
        if image:
            self._view.set_image(image)

    def get_core(self):
        return self._core
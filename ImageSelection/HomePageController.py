from __future__ import annotations
from ImageSelection.HomePageModel import HomePageModel
from ImageSelection.HomePageView import HomePageView

import typing

if typing.TYPE_CHECKING:
    from Core.AppController import AppController


class HomePageController:

    def __init__(self, core: AppController) -> None:
        self._core = core

        self._view = HomePageView(self)
        self._model = HomePageModel()


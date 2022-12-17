from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from ImageSelection.HomePageController import HomePageController


class HomePageView:

    def __init__(self, controller: HomePageController) -> None:
        self._controller = controller
        
        self._folder_explorer = None
        self._folder_content = None
        self._options = None
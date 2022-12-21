from __future__ import annotations

import typing

from Utils.Position import Position
from ttkbootstrap import Progressbar, Label, Frame, StringVar
from ttkbootstrap.constants import TOP, X, LEFT, DETERMINATE, INDETERMINATE, SUCCESS, STRIPED

if typing.TYPE_CHECKING:
    from Preprocessing.PreprocessingController import PreprocessingController    


class PreprocessingView:

    DETERMINATED = 1
    INDETERMINATED = 0

    def __init__(self, controller: PreprocessingController) -> None:
        self._controller = controller
        
        self._label_text = StringVar()

        self._progressbar = None

        self._init_body()

    def _init_body(self) -> None:
        view = self._controller.get_core().get_view()
        view.hide(Position.LEFT)
        view.hide(Position.RIGHT)

        main_container = view.new_frame(Position.CENTER)
        
        top_container = Frame(main_container)
        bot_container = Frame(main_container)

        top_container.pack(side=TOP, fill=X)
        bot_container.pack(side=TOP, fill=X)
        main_container.pack(side=TOP, pady=18)

        Label(top_container, textvariable=self._label_text).pack(side=LEFT)
        self._progressbar = Progressbar(bot_container, length=280, bootstyle=(SUCCESS, STRIPED))
        self._progressbar.pack(side=LEFT)
                            
    def set_label_text(self, text) -> None:
        self._label_text.set(text)

    def set_progressbar_value(self, value: float) -> None:
        self._progressbar["value"] =  f"{value: .2f}"

    def set_progressbar_type(self, value: int) -> None:
        mode = INDETERMINATE
        if value == self.DETERMINATED:
            mode=DETERMINATE
        self._progressbar.configure(mode=mode)

    def increase_progressbar(self) -> None:
        self._progressbar['value'] += 5

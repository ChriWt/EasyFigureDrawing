from __future__ import annotations

from customtkinter import CTk, CTkFrame, Y, X, BOTH , TOP, BOTTOM, LEFT
from Utils.Position import Position

import typing

if typing.TYPE_CHECKING:
    from Utils.Position import Position

class AppView:

    def __init__(self) -> None:
        self._root = CTk()
        self._top = CTkFrame(self._root)
        self._middle = CTkFrame(self._root)
        self._left = CTkFrame(self._middle)
        self._center = CTkFrame(self._middle)
        self._right = CTkFrame(self._middle)
        self._bottom = CTkFrame(self._root)

        self._pack_frames()

    def _pack_frames(self) -> None:
        self._top.pack(side=TOP, fill=X, padx=5, pady=(5, 0))
        self._middle.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self._bottom.pack(side=BOTTOM, fill=X, padx=5, pady=(0, 5))

        self._left.pack(side=LEFT, fill=Y, padx=(0, 5))
        self._center.pack(side=LEFT, fill=BOTH, expand=True)
        self._right.pack(side=LEFT, fill=Y, padx=(5, 0))

    def clear(self, position: Position = Position.ALL) -> None:
        if position == Position.TOP:
            self._clear_top()
        elif position == Position.LEFT:
            self._clear_left()
        elif position == Position.CENTER:
            self._clear_center()
        elif position == Position.RIGHT:
            self._clear_right()
        elif position == Position.BOTTOM:
            self._clear_bottom()
        elif position == Position.ALL:
            self._clear_all()

    def _clear_all(self) -> None:
        self._clear_top()
        self._clear_left()
        self._clear_center()
        self._clear_right()
        self._clear_bottom()

    def _clear_top(self) -> None:
        self._clear(self._top)

    def _clear_left(self) -> None:
        self._clear(self._left)

    def _clear_center(self) -> None:
        self._clear(self._center)

    def _clear_right(self) -> None:
        self._clear(self._right)

    def _clear_bottom(self) -> None:
        self._clear(self._bottom)

    def _clear(self, container: CTkFrame) -> None:
        [element.destroy() for element in container.winfo_children()]

    def new_frame(self, position: Position) -> CTkFrame:
        if position == Position.TOP:
            return CTkFrame(self._top)
        elif position == Position.LEFT:
            return CTkFrame(self._left)
        elif position == Position.CENTER:
            return CTkFrame(self._center)
        elif position == Position.RIGHT:
            return CTkFrame(self._right)
        elif position == Position.BOTTOM:
            return CTkFrame(self._bottom)
        else:
            raise Exception(f"Position {position} not valid")

    def get_root(self) -> CTk:
        return self._root

    def start(self) -> None:
        self._root.mainloop()

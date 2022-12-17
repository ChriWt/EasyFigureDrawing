from __future__ import annotations

from customtkinter import CTk, CTkFrame, Y, X, BOTH , TOP, BOTTOM, LEFT, RIGHT
from Utils.Position import Position


import typing

if typing.TYPE_CHECKING:
    from Utils.Position import Position

class AppView:
    
    _COMPONENT = "component"
    _CONFIGURATION = "configs"
    _VISIBLE = "visible"

    def __init__(self) -> None:
        self._root = CTk()

        self._middle = CTkFrame(self._root)
        self._components = {
            Position.TOP: {
                self._COMPONENT: CTkFrame(self._root), 
                self._CONFIGURATION: {"side":TOP, "fill":X, "padx":5, "pady":(5, 0)},
                self._VISIBLE: True
            },

            Position.MIDDLE: {
                self._COMPONENT: self._middle, 
                self._CONFIGURATION: {"side":TOP, "fill":BOTH, "expand":True, "padx":5, "pady":5},
                self._VISIBLE: True
            },

            Position.BOTTOM: {
                self._COMPONENT: CTkFrame(self._root), 
                self._CONFIGURATION: {"side":BOTTOM, "fill":X, "padx":5, "pady":(0, 5)},
                self._VISIBLE: True
            },

            Position.LEFT: {
                self._COMPONENT: CTkFrame(self._middle),
                self._CONFIGURATION: {"side":LEFT, "fill":Y, "padx":(0, 5)},
                self._VISIBLE: True
            },

            Position.CENTER: {
                self._COMPONENT: CTkFrame(self._middle),
                self._CONFIGURATION: {"side":LEFT, "fill":BOTH, "expand":True},
                self._VISIBLE: True
            },

            Position.RIGHT: {
                self._COMPONENT: CTkFrame(self._middle),
                self._CONFIGURATION: {"side":RIGHT, "fill":Y, "padx":(5, 0)},
                self._VISIBLE: True
            }
        }

        self._pack_frames()

    def _pack_frames(self) -> None:
        for position, widget in self._components.items():
            widget[self._COMPONENT].pack(**widget[self._CONFIGURATION])


    def clear(self, position: Position = Position.ALL) -> None:
        if position not in self._components and position != Position.ALL:
            raise Exception(f"Position {position} not valid!")

        if position == Position.ALL:
            self._clear_all()
        else:
            self._clear(self._components[position][self._COMPONENT])

    def _clear_all(self) -> None:
        [self.clear(position) for position in self._components if position != Position.MIDDLE]

    def _clear(self, container: CTkFrame) -> None:
        [element.destroy() for element in container.winfo_children()]


    def new_frame(self, position: Position) -> CTkFrame:
        if position not in self._components:
            raise Exception(f"Position {position} not valid!")

        root = self._components[position][self._COMPONENT]
        return CTkFrame(root)


    def hide(self, position: Position) -> None:
        if position not in self._components:
            raise Exception(f"Position {position} not valid!")

        self._components[position][self._COMPONENT].pack_forget()
        self._components[position][self._VISIBLE] = False


    def show(self, position: Position) -> None:
        if position not in self._components:
            raise Exception(f"Position {position} not valid!")

        self._components[position][self._VISIBLE] = True
        self._hide_visible_frames()
        self._show_frames_with_visible_status()

    def _hide_visible_frames(self) -> None:
        for _, widget in self._components.items():
            if widget[self._VISIBLE]:
                widget[self._COMPONENT].pack_forget() 

    def _show_frames_with_visible_status(self) -> None:
        for _, widget in self._components.items():
            if widget[self._VISIBLE]:
                widget[self._COMPONENT].pack(**widget[self._CONFIGURATION]) 


    def configure(self, position: Position, **keyargs) -> None:
        if position not in self._components:
            raise Exception(f"Position {position} not valid!")

        self._components[position][self._COMPONENT].configure(**keyargs)


    def get_root(self) -> CTk:
        return self._root


    def start(self) -> None:
        self._root.mainloop()

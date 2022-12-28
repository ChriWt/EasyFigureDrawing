from __future__ import annotations

from Utils.Position import Position
from ttkbootstrap import Frame
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import typing

if typing.TYPE_CHECKING:
    from Utils.Position import Position
    from Core.AppController import AppController


class AppView:
    
    _COMPONENT = "component"
    _CONFIGURATION = "configs"
    _VISIBLE = "visible"

    def __init__(self, controller: AppController) -> None:
        self._width = 1280
        self._height = 700
        self._controller = controller

        self._root = ttk.Window(title="Figure Drawing", 
                                size=(self._width, self._height), 
                                themename="superhero")
        self._root.place_window_center()
        self._root.bind("<Configure>", self._on_configure_event)

        self._middle = Frame(self._root)
        self._components = {
            Position.TOP: {
                self._COMPONENT: Frame(self._root), 
                self._CONFIGURATION: {"side":TOP, "fill":X, "padx":5, "pady":(5, 0)},
                self._VISIBLE: True
            },

            Position.MIDDLE: {
                self._COMPONENT: self._middle, 
                self._CONFIGURATION: {"side":TOP, "fill":BOTH, "expand":True, "padx":5, "pady":5},
                self._VISIBLE: True
            },

            Position.BOTTOM: {
                self._COMPONENT: Frame(self._root), 
                self._CONFIGURATION: {"side":BOTTOM, "fill":X, "padx":5, "pady":(0, 5)},
                self._VISIBLE: True
            },

            Position.LEFT: {
                self._COMPONENT: Frame(self._middle),
                self._CONFIGURATION: {"side":LEFT, "fill":Y, "padx":(0, 5)},
                self._VISIBLE: True
            },

            Position.CENTER: {
                self._COMPONENT: Frame(self._middle),
                self._CONFIGURATION: {"side":LEFT, "fill":BOTH, "expand":True},
                self._VISIBLE: True
            },

            Position.RIGHT: {
                self._COMPONENT: Frame(self._middle),
                self._CONFIGURATION: {"side":RIGHT, "fill":Y, "padx":(5, 0)},
                self._VISIBLE: True
            }
        }

        self._pack_frames()

    def change_app_size(self, size: tuple) -> None:
        self._root.geometry(f"{size[0]}x{size[1]}")
        self._root.position_center()

    def _on_configure_event(self, _):
        event_width, event_height = self.get_size()
        if event_width != self._width or event_height != self._height:
            self._width, self._height = event_width, event_height
            self._controller.on_size_change()

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

    def _clear(self, container: Frame) -> None:
        [element.destroy() for element in container.winfo_children()]


    def new_frame(self, position: Position, **keyargs) -> Frame:
        if position not in self._components:
            raise Exception(f"Position {position} not valid!")

        root = self._components[position][self._COMPONENT]
        return Frame(root, **keyargs)


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


    def get_root(self) -> ttk.Window:
        return self._root

    def get_size(self) -> tuple:
        return self._root.winfo_width(), self._root.winfo_height()

    def start(self) -> None:
        self._root.mainloop()

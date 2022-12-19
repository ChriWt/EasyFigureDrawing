from __future__ import annotations
from ttkbootstrap import Canvas, Checkbutton
from ttkbootstrap.constants import NW
from PIL import Image, ImageTk

import typing

if typing.TYPE_CHECKING:
    from ttkbootstrap.scrolled import ScrolledFrame


class Preview:

    VERTICAL_PHOTO_HEIGHT = 240

    HORIZONTAL_PHOTO_WIDTH = 240

    def __init__(self, master: ScrolledFrame, path: str) -> None:
        self._master = master
        self._path = path

        self._canvas = None
        self._checkbutton = None
        self._image = None
        self._size = ()

        self._load_image()
        self._init_body()

    def _load_image(self) -> None:
        self._image = Image.open(self._path)
        self._size = self._image.size
        self._image = ImageTk.PhotoImage(self._image)

    def _init_body(self) -> None:
        width, height = self._size
        self._canvas = Canvas(self._master, width=width, height=height)
        self._canvas.create_image(0, 0, anchor=NW, image=self._image, tags="image")

        self._checkbutton = Checkbutton(self._canvas, text='')
        self._checkbutton.place(x=width - 24, y=height - 24)

    def get_size(self) -> tuple:
        return self._size

    def grid(self, **keyargs) -> None:
        self._canvas.grid(**keyargs)
    
    def place(self, **keyargs) -> None:
        self._canvas.place(**keyargs)

    
from __future__ import annotations
from ttkbootstrap import Canvas, Checkbutton, BooleanVar
from ttkbootstrap.constants import NW
from PIL import Image, ImageTk
from ImageSelection.HomePageModel import HomePageModel
from ImageSelection.ImageMagnifier import newImageMagnifier

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
        self._value = BooleanVar()

        self._load_image()
        self._init_body()
        
        newImageMagnifier(self._canvas, path.replace(HomePageModel.MINIATURE_FOLDER, HomePageModel.RESOURCES_FOLDER))

    def _load_image(self) -> None:
        self._image = Image.open(self._path)
        self._size = self._image.size
        self._image = ImageTk.PhotoImage(self._image)

    def _init_body(self) -> None:
        width, height = self._size
        self._canvas = Canvas(self._master, width=width, height=height)
        self._canvas.create_image(0, 0, anchor=NW, image=self._image, tags="image")

        self._checkbutton = Checkbutton(self._canvas, variable=self._value, bootstyle="success-toolbutton", text='')
        self._checkbutton.place(x=width - 24, y=height - 24)

    def add_trace(self, callback) -> None:
        self._value.trace("w", lambda *_: callback(self._path, self._value.get()))

    def get_size(self) -> tuple:
        return self._size

    def grid(self, **keyargs) -> None:
        self._canvas.grid(**keyargs)
    
    def place(self, **keyargs) -> None:
        self._canvas.place(**keyargs)

    def get_value(self) -> bool:
        return self._value.get()

    def set_value(self, value: bool):
        self._value.set(value)
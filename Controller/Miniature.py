from threading import Thread
from tkinter import NW, BooleanVar
from customtkinter import CTkCanvas, CTkCheckBox

from PIL import Image, ImageTk

from View.ImageMagnifier import newImageMagnifier


# class Miniature(Thread):
class Miniature:

    VERTICAL_PHOTO_WIDTH = 160 
    VERTICAL_PHOTO_HEIGHT = 240

    HORIZONTAL_PHOTO_WIDTH = 240
    HORIZONTAL_PHOTO_HEIGHT = 360

    def __init__(self, root, controller, path: str, original: str) -> None:
        self._path = path
        self._original = original
        self._image = None
        self._size = ()
        self._root = root

        self._body = None
        self._check_box = None

        self._value = BooleanVar()
        self._value.trace('w', lambda *args : controller.on_image_selected(self))

    def pack(self):
        self._load_image()
        self._init_body()
        newImageMagnifier(self._body, self._original)

    def _load_image(self):
        self.load_image()
        # self.crop()
        self._size = self._image.size
        self._image = ImageTk.PhotoImage(self._image)

    def _init_body(self):
        width, height = self._size

        self._body = CTkCanvas(self._root, 
                                width=width, 
                                bg="#2a2d2e",
                                highlightthickness=1,
                                highlightbackground="#2a2d2e",
                                height=height)

        self._body.create_image(0, 0, anchor=NW, image=self._image, tags="image")

        self._check_box = CTkCheckBox(self._body, text="", variable=self._value)
        self._check_box.place(x=width - 24, y=height - 24)

    def get_path(self) -> str:
        return self._path

    def get_check_box_state(self) -> bool:
        return self._value.get()

    def select(self):
        self._check_box.select()

    def deselect(self):
        self._check_box.deselect()

    def get_body(self):
        return self._body

    def get_image_size(self):
        return self._size

    def crop(self):
        width, height = self._image.size
        
        if height > width:
            self._image.thumbnail(size=(self.VERTICAL_PHOTO_WIDTH, self.VERTICAL_PHOTO_HEIGHT))
        else:
            self._image.thumbnail(size=(self.HORIZONTAL_PHOTO_WIDTH, self.HORIZONTAL_PHOTO_HEIGHT))

    def load_image(self):
        self._image = Image.open(self._path)

    def get_image(self):
        return self._image

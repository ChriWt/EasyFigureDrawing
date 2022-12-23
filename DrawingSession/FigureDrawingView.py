from __future__ import annotations

import typing

from PIL import Image,ImageTk
from ttkbootstrap import Toplevel, Frame, Button, IntVar, Progressbar, SUCCESS, STRIPED, Canvas, N, Checkbutton, OUTLINE, TOOLBUTTON
from ttkbootstrap import TOP, BOTH


if typing.TYPE_CHECKING:
    from DrawingSession.FigureDrawingController import FigureDrawingController

class FigureDrawingView:

    def __init__(self, controller: FigureDrawingController) -> None:
        self._controller = controller

        root = self._controller.get_core().get_view().get_root()
        self._core = Toplevel(root)
        self._core.title("Drawing Session")
        self._core.state("zoomed")

        self._photo_canvas = Canvas(self._core)
        self._photo_canvas.pack(side=TOP, fill=BOTH, expand=True)

        self._button_frame = Frame(self._core)
        self._button_frame.place(x=5, y=5)

        self._is_black_white = False

        self.black_white_flag = IntVar()
        self.black_white_flag.trace('w', lambda *x: self.change_black_white_flag())

        self._black_white = Image.open(r".\Assets\Black_white.png")
        self._black_white = self._black_white.resize((20, 20), Image.ANTIALIAS)
        self._black_white = ImageTk.PhotoImage(self._black_white)
        Checkbutton(self._button_frame, image=self._black_white, variable=self.black_white_flag, bootstyle=(SUCCESS, TOOLBUTTON, OUTLINE)).pack(side=TOP)

        self._random = Image.open(r".\Assets\Random.png")
        self._random = self._random.resize((20, 20), Image.ANTIALIAS)
        self._random = ImageTk.PhotoImage(self._random)
        Checkbutton(self._button_frame, image=self._random, bootstyle=(SUCCESS, TOOLBUTTON, OUTLINE)).pack(side=TOP, pady=5)

        self._core.update()
        self._previous = Image.open(r".\Assets\Previous.png")
        self._previous = self._previous.resize((10, 20), Image.ANTIALIAS)
        self._previous = ImageTk.PhotoImage(self._previous)
        Button(self._core, image=self._previous, bootstyle=SUCCESS, command=self._controller.on_display_previous).place(x=10, y=(self._core.winfo_height() / 2 - 10))

        self._next = Image.open(r".\Assets\Next.png")
        self._next = self._next.resize((10, 20), Image.ANTIALIAS)
        self._next = ImageTk.PhotoImage(self._next)
        Button(self._core, image=self._next, bootstyle=SUCCESS, command=self._controller.on_display_next).place(x=self._core.winfo_width() - 45, y=(self._core.winfo_height() / 2 - 10))

        self._timer = Progressbar(self._core, 
                                    length=self._core.winfo_width(), 
                                    bootstyle=(STRIPED, SUCCESS)).place(x=0, y=self._core.winfo_height() - 20)

        self._image = None
        self._grayscale_image = None
        self._photoimage = None

    def set_image(self, image_path: str) -> None:
        self._image = Image.open(image_path)
        
        width, height = self._image.size

        aspect_ratio = min(self._core.winfo_width() / width, self._core.winfo_height() / height)

        new_width, new_height = (int(width * aspect_ratio), int(height * aspect_ratio))
        self._image = self._image.resize((new_width, new_height), Image.ANTIALIAS)
        self._grayscale_image = self._image.convert("L")
        
        self._draw_image()

    def change_black_white_flag(self) -> None:
        self._is_black_white = not self._is_black_white
        self._draw_image()

    def _draw_image(self) -> None:
        image = None

        if self._is_black_white:
            image = self._grayscale_image
        else:
            image = self._image

        self._photoimage = ImageTk.PhotoImage(image)
        self._photo_canvas.delete("all")
        self._photo_canvas.create_image(self._core.winfo_width() / 2, 0, image=self._photoimage, anchor=N)

    def start(self) -> None:
        self._core.mainloop()
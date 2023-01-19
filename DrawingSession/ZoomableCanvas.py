from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from PIL import Image

from ttkbootstrap import Canvas, N
from PIL import Image, ImageTk


class ZoomableCanvas:

    DELTA_ZOOM = 1.3

    def __init__(self, parent) -> None:
        self.body = Canvas(parent)
        self.body.bind("<MouseWheel>", self.on_scroll)
        self.body.bind("<B1-Motion>", self.on_drag)
        self.body.bind("<ButtonRelease-1>", self.on_drag_stop)
        
        self._size = None, None
        self._image = None
        self._zoomed_image = None
        self._zoomed_grayscale = None
        self._grayscale_image = None
        self._photo_image = None
        self._current_item_id = -1
        self._is_black_white = False
        self._cursor_last_position = None

    def on_drag(self, event) -> None:
        if self._cursor_last_position is None:
            self._cursor_last_position = (event.x, event.y)
            return

        direction_x = event.x - self._cursor_last_position[0]
        direction_y = event.y - self._cursor_last_position[1]

        self._cursor_last_position = (event.x, event.y)
        self.body.move(self._current_item_id, direction_x, direction_y)

    def on_drag_stop(self, *_) -> None:
        self._cursor_last_position = None

    def on_scroll(self, event) -> None:
        x, y = event.x, event.y
        if event.delta / 120 > 0:
            self._zoom_in(x, y)
        else:
            self._zoom_out(x, y)

    def _zoom_in(self, x: int, y: int) -> None:
        width, height = self._size
        self._size = (width * self.DELTA_ZOOM, height * self.DELTA_ZOOM)

        self._zoomed_image = self._image.resize((int(x) for x in self._size), Image.BILINEAR)
        self._zoomed_grayscale = self._zoomed_image.convert("L")

        image = self._zoomed_image
        if self._is_black_white:
            image = self._zoomed_grayscale
        
        self._photo_image = ImageTk.PhotoImage(image)

        old_box = self.body.bbox(self._current_item_id)

        self._draw()

        new_box = self.body.bbox(self._current_item_id)
        
        self._move_image_after_zoom(old_box, new_box, x, y)

    def _zoom_out(self, x: int, y: int) -> None:
        width, height = self._size
        self._size = (width / self.DELTA_ZOOM, height / self.DELTA_ZOOM)

        self._zoomed_image = self._image.resize((int(x) for x in self._size), Image.BILINEAR)
        self._zoomed_grayscale = self._zoomed_image.convert("L")

        image = self._zoomed_image
        if self._is_black_white:
            image = self._zoomed_grayscale
        
        self._photo_image = ImageTk.PhotoImage(image)

        old_box = self.body.bbox(self._current_item_id)

        self._draw()

        new_box = self.body.bbox(self._current_item_id)
        self._move_image_after_zoom(old_box, new_box, x, y)

    def _move_image_after_zoom(self, old_box: tuple, new_box: tuple, x_cursor: int, y_cursor: int) -> None:
        old_cursor_position_x = x_cursor - old_box[0]
        old_cursor_position_y = y_cursor - old_box[1]
        old_size = self._calculate_box_size(old_box)
        new_size = self._calculate_box_size(new_box)

        new_cursor_position_x = old_cursor_position_x * new_size[0] / old_size[0] + new_box[0]
        new_cursor_position_y = old_cursor_position_y * new_size[1] / old_size[1] + new_box[1]

        new_x = old_cursor_position_x - new_cursor_position_x
        new_y = old_cursor_position_y - new_cursor_position_y 

        self.body.move(self._current_item_id, old_box[0] + new_x, old_box[1] + new_y)

    def _calculate_box_size(self, box: tuple) -> tuple:
        return self._calculate_box_width(box), self._calculate_box_height(box)

    def _calculate_box_width(self, box: tuple) -> int:
        return box[2] - box[0]

    def _calculate_box_height(self, box: tuple) -> int:
        return box[3] - box[1]

    def delete(self, type: str) -> None:
        self.body.delete(type)

    def new_image(self, path: str) -> None:
        self._image = Image.open(path)
        
        width, height = self._image.size
        aspect_ratio = min(self.body.winfo_width() / width, self.body.winfo_height() / height)
        self._size = (int(width * aspect_ratio), int(height * aspect_ratio))

        self._image = self._image.resize(self._size, Image.ANTIALIAS)
        self._zoomed_image = self._image
        self._grayscale_image = self._image.convert("L")
        self._zoomed_grayscale = self._grayscale_image
        
    def draw(self, grayscale: bool, **keyargs) -> None:
        self._is_black_white = grayscale
        if grayscale:
            self._photo_image = ImageTk.PhotoImage(self._grayscale_image)
        else:
            self._photo_image = ImageTk.PhotoImage(self._image)

        self._draw(**keyargs)

    def _draw(self, position: str = N, **keyargs) -> None:
        if "anchor" in keyargs:
            position = keyargs["anchor"]
            del keyargs["anchor"]

        self.delete("all")
        self._current_item_id = self.body.create_image(self.body.winfo_width() / 2, 0, image=self._photo_image, anchor=position, **keyargs)

    def enable_grayscale_image(self, state: bool) -> None:
        self._is_black_white = state

        image = self._zoomed_image
        if state:
            image = self._zoomed_grayscale
        self._photo_image = ImageTk.PhotoImage(image)

        x, y, *_ = self.body.bbox(self._current_item_id)

        self.delete("all")
        self._current_item_id = self.body.create_image(self.body.winfo_width() / 2, 0, image=self._photo_image, anchor=N)
        
        new_x, new_y, *_ = self.body.bbox(self._current_item_id)
        self.body.move(self._current_item_id, x - new_x, y - new_y)
            
    def pack(self, **keyargs) -> None:
        self.body.pack(**keyargs)
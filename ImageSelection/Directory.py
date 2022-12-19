from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from ttkbootstrap.scrolled import ScrolledFrame
    from Preview.Preview import Preview

class Directory:

    _PADX = 5

    def __init__(self, frame: ScrolledFrame) -> None:
        self._frame = frame
        self._content = []
        self._row = 0
        self._current_row_size = 0

    def get_frame(self) -> ScrolledFrame:
        return self._frame

    def add_content(self, preview: Preview) -> None:
        self._content.append(preview)

    def get_preview(self, index: int) -> Preview:
        return self._content[index]

    def get_count(self) -> int:
        return len(self._content)

    def get_row(self) -> int:
        return self._row

    def increment_row(self) -> None:
        self._row += 1

    def reset_row(self) -> None:
        self._row = 0

    def get_current_row_size(self) -> int:
        return self._current_row_size

    def add_to_current_row_size(self, size: int) -> None:
        self._current_row_size += size + self._PADX

    def reset_current_row_size(self) -> None:
        self._current_row_size = 0

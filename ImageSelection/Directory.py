from __future__ import annotations
import random
import typing

from Utils.CycleManager import CycleManager

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

    def select_all(self, state: bool=True) -> None:
        for preview in self._content:
            preview.set_value(state)

    def select_random(self, quantity: int) -> None:
        non_selected = []
        for preview in self._content:
            if not preview.get_value():
                non_selected.append(preview)
        
        if not non_selected:
            return

        manager = CycleManager.get_instance()
        
        def select_new_random(quantity: int) -> None:
            if quantity == 0:
                return
            
            index = random.randrange(0, len(non_selected))
            non_selected[index].set_value(True)
            del non_selected[index]
            manager.after(1, lambda: select_new_random(quantity - 1))

        select_new_random(quantity)

    def deselect_all(self) -> None:
        self.select_all(False)

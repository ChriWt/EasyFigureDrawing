from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from tkinter import Tk


class TimelineManager:

    _root = None
    _instance = None
    _timelines = list()

    def __init__(self) -> None:
        pass

    def set_root(self, root: Tk) -> None:
        self._root = root

    def after(self, time: int, callback: callable) -> int:
        lista = [callback]
        key = self._root.after(time, lambda : self._on_animation_end(*lista))
        self._timelines.append(key)
        lista.append(key)
        return key

    def _on_animation_end(self, callback: list, animation_id: int) -> None:
        try:
            self._timelines.remove(animation_id)
            callback()
        except Exception:
            pass

    def stop(self, animation_id: int) -> None:
        self._root.after_cancel(animation_id)

    def stop_all(self) -> None:
        
        for key in self._timelines:
            self.stop(key)
        self._timelines.clear()

    def get_instance():
        if TimelineManager._instance is None:
            TimelineManager._instance = TimelineManager()
        return TimelineManager._instance
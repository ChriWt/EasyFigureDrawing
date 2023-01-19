from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from tkinter import Tk


class CycleManager:

    DEFAULT = 0

    _root = None
    _instance = None
    _timelines = {DEFAULT: []}

    def __init__(self) -> None:
        pass

    def set_root(self, root: Tk) -> None:
        self._root = root

    def after(self, time: int, callback: callable, channel: int = DEFAULT) -> int:
        lista = [callback]

        key = self._root.after(time, lambda : self._on_animation_end(channel, *lista))

        if channel not in self._timelines:
            self._timelines[channel] = []
        
        self._timelines[channel].append(key)

        # this is done to pass to _on_animation_end the animation_id
        lista.append(key)
        return key

    def _on_animation_end(self, channel: int, callback: list, animation_id: int) -> None:
        try:
            self._timelines[channel].remove(animation_id)
            callback()
        except Exception:
            pass

    def stop(self, animation_id: int) -> None:
        self._root.after_cancel(animation_id)

    def stop_all(self) -> None:
        for channel in self._timelines:
            self.stop_all_in_channel(channel)
        self._timelines = {self.DEFAULT: []}

    def stop_all_in_channel(self, channel: int) -> None:
        for key in self._timelines[channel]:
            self.stop(key)

    def get_instance():
        if CycleManager._instance is None:
            CycleManager._instance = CycleManager()
        return CycleManager._instance
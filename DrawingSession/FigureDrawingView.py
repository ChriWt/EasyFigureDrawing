from __future__ import annotations

import typing

from PIL import Image,ImageTk
from ttkbootstrap import Toplevel, Frame, Button, IntVar, Progressbar, Canvas, N, Checkbutton, Label, STRIPED, DANGER, PRIMARY, TOOLBUTTON, OUTLINE
from ttkbootstrap import TOP, BOTH
from DrawingSession.ZoomableCanvas import ZoomableCanvas

from Utils.CycleManager import CycleManager

if typing.TYPE_CHECKING:
    from DrawingSession.FigureDrawingController import FigureDrawingController

class FigureDrawingView:

    def __init__(self, controller: FigureDrawingController) -> None:
        self._controller = controller

        root = self._controller.get_core().get_view().get_root()
        self._core = Toplevel(root)
        self._core.title("Drawing Session")
        self._core.state("zoomed")
        self._core.minsize(700, 400)

        self._photo_canvas = ZoomableCanvas(self._core) # Canvas(self._core)
        self._photo_canvas.pack(side=TOP, fill=BOTH, expand=True)

        self._button_frame = Frame(self._core)
        self._button_frame.place(x=5, y=5)

        self._is_black_white = False
        self._is_random = False

        self.black_white_flag = IntVar()
        self.black_white_flag.trace('w', lambda *x: self.change_black_white_flag())

        self._black_white = Image.open(r".\Assets\Black_white.png")
        self._black_white = self._black_white.resize((20, 20), Image.ANTIALIAS)
        self._black_white = ImageTk.PhotoImage(self._black_white)
        Checkbutton(self._button_frame, image=self._black_white, variable=self.black_white_flag, bootstyle=(PRIMARY, TOOLBUTTON, OUTLINE)).pack(side=TOP)

        self.random_flag = IntVar()
        self.random_flag.trace('w', lambda *x: self.change_random_flag())

        self._random = Image.open(r".\Assets\Random.png")
        self._random = self._random.resize((20, 20), Image.ANTIALIAS)
        self._random = ImageTk.PhotoImage(self._random)
        Checkbutton(self._button_frame, image=self._random, variable=self.random_flag, bootstyle=(PRIMARY, TOOLBUTTON, OUTLINE)).pack(side=TOP, pady=5)

        self._core.update()
        self._previous = Image.open(r".\Assets\Previous.png")
        self._previous = self._previous.resize((10, 20), Image.ANTIALIAS)
        self._previous = ImageTk.PhotoImage(self._previous)
        self._previous_button = Button(self._core, image=self._previous, command=self._controller.on_display_previous)
        self._previous_button.place(x=10, y=(self._core.winfo_height() / 2 - 10))

        self._next = Image.open(r".\Assets\Next.png")
        self._next = self._next.resize((10, 20), Image.ANTIALIAS)
        self._next = ImageTk.PhotoImage(self._next)
        self._next_button = Button(self._core, image=self._next, command=self._controller.on_display_next)
        self._next_button.place(x=self._core.winfo_width() - 45, y=(self._core.winfo_height() / 2 - 10))

        self._timer = Label(self._core, text="00:00 / 00:00", font=("TkDefaultFont", 13))
        self._timer.place(x=self._core.winfo_width() / 2 - self._core.winfo_width() / 4 - 110, y=self._core.winfo_height() - 35)

        self._timer_bar = Progressbar(self._core, 
                                    length=self._core.winfo_width() / 2, 
                                    mode='determinate',
                                    bootstyle=(PRIMARY, STRIPED),
                                    maximum=100)
        self._timer_bar.place(x=self._core.winfo_width() / 2 - self._core.winfo_width() / 4, y=self._core.winfo_height() - 30)
        
        self._pause_button = Button(self._core, text="Pause", width=9, command=self._on_pause_click)
        self._pause_button.place(x=self._core.winfo_width() / 2 + self._core.winfo_width() / 4 + 20, y=self._core.winfo_height() - 40)

        self._total_image_selected_label = Label(self._core, text="Selected:", font=("TkDefaultFont", 14))
        self._total_image_selected_label.place(x=self._core.winfo_width() - 130, y=5)

        self._current_image_index = Label(self._core, text="0/0", font=("TkDefaultFont", 14))
        self._current_image_index.place(x=self._core.winfo_width() - 60, y=30)

        self._current_time = 0
        self._max_time = 0
        self._stop_timer = False
        self._manager = CycleManager.get_instance()

        self._core.bind("<Configure>", self._scale_ui)

    def set_image(self, image_path: str) -> None:
        self._photo_canvas.new_image(image_path)
        self._photo_canvas.draw(self._is_black_white)

    def start_timer(self, time: int) -> None:
        self._max_time = time
        self._current_time = time

        self._timer["text"] = f"00:00 / {self._format_time(self._max_time)}"
        
        self._continue_timer()

    def _continue_timer(self) -> None:
        if self._current_time < 0:
            self._controller.on_timer_end()
            return

        if not self._stop_timer:
            self.update_timer_bar(self._current_time, self._max_time)
            self.update_timer(self._current_time)
            self._current_time -= 1

        if not self._stop_timer:
            self._manager.after(1000, self._continue_timer, channel=2)

    def _format_time(self, seconds: int) -> str:
        _minutes = int(seconds / 60)
        _seconds = int(seconds % 60)
        _minutes = "" + str(_minutes) if _minutes >= 10 else "0" + str(_minutes)
        _seconds = "" + str(_seconds) if _seconds >= 10 else "0" + str(_seconds)
        return _minutes + ":" + _seconds
    
    def update_timer(self, current_time: int) -> None:
        self._timer["text"] = f"{self._format_time(current_time)} / {self._format_time(self._max_time)}"

    def stop_timer(self) -> None:
        CycleManager.get_instance().stop_all()

    def update_timer_bar(self, current_time: int, time: int) -> None:
        self._timer_bar["value"] = int(current_time / time * 100)

    def change_black_white_flag(self) -> None:
        self._is_black_white = not self._is_black_white
        self._photo_canvas.enable_grayscale_image(self._is_black_white)
    
    def change_random_flag(self) -> None:
        self._is_random = not self._is_random
        self._controller.update_random_flag(self._is_random)

    def start(self) -> None:
        self._core.mainloop()

    def _on_pause_click(self) -> None:
        self._stop_timer = not self._stop_timer
        self._update_timer_button()

    def _update_timer_button(self) -> None:
        self._pause_button["text"] = "Pause" if not self._stop_timer else "Continue"
        self._pause_button.configure(bootstyle=PRIMARY if not self._stop_timer else DANGER)
        if not self._stop_timer:
            self._continue_timer()

    def set_selected_count(self, count: int) -> None:
        self._total_image_selected_label["text"] = f"Selected: {count}"

        current = self._current_image_index["text"].split('/')[0]
        self._current_image_index["text"] = f"{current}/{count}"

    def set_current_image(self, index: int) -> None:
        total = self._current_image_index["text"].split('/')[1]
        self._current_image_index["text"] = f"{index}/{total}"

    def _scale_ui(self, *_) -> None:
        instance = CycleManager.get_instance()

        def scale():
            instance.stop_all_in_channel(1)
            self._core.update()
            window_width = self._core.winfo_width()
            window_height = self._core.winfo_height()

            self._previous_button.place(x=10, y=window_height / 2 - 10)
            self._next_button.place(x=window_width - 45, y=window_height / 2 - 10)

            self._timer.place(x=window_width / 2 - window_width / 4 - 110, y=window_height - 35)

            self._timer_bar.place(x=window_width / 2 - window_width / 4, y=window_height - 30)
            self._timer_bar.configure(length=window_width / 2)

            self._pause_button.place(x=window_width / 2 + window_width / 4 + 20, y=window_height - 40)

            self._total_image_selected_label.place(x=window_width - 130, y=5)
            self._current_image_index.place(x=window_width - 60, y=30)

            self._controller.on_size_update()

        instance.after(60, scale, channel=1)
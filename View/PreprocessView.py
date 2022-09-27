from tkinter import LEFT, RIGHT, TOP, X
from customtkinter import CTkToplevel, CTkProgressBar, CTkButton, CTkFrame, CTkLabel

class PreprocessView:

    def __init__(self, root, controller) -> None:
        self._body = CTkToplevel(root)
        self._body.title("Preprocess Images")
        self._body.geometry("400x190")  

        self._frame = CTkFrame(self._body)

        self._label_frame = CTkFrame(self._frame)
        self._prefix = CTkLabel(self._label_frame, text="Calculating depth... ")
        self._label = CTkLabel(self._label_frame)

        self._progress_bar = CTkProgressBar(self._frame)
        self._progress_bar.set(0)

        self._button_frame = CTkFrame(self._frame)
        self._start = CTkButton(self._button_frame, text="Start", command=controller.start)
        self._cancel = CTkButton(self._button_frame, text="Cancel", command=controller.cancel)

        self._frame.pack(side=TOP, fill=X, expand=True, padx=10, pady=10)
        self._label_frame.pack(fill=X, pady=10)
        self._prefix.pack(side=LEFT, padx=(85, 0), pady=10)
        self._label.pack(side=RIGHT, padx=(0, 100))
        self._progress_bar.pack(pady=(10, 0))
        self._button_frame.pack(pady=(20, 20))
        self._start.pack(side=LEFT, padx=20, pady=10)
        self._cancel.pack(side=LEFT, padx=20)

    def update_progress_bar(self, progress):
        self._progress_bar.set(progress)
        self._progress_bar.update()
        self._body.update()

    def set_prefix(self, text):
        self._prefix.configure(text=text)

    def update_label(self, progress):
        self._label.configure(text=str(round(progress, 2)) + "%")
        self._label.update()
        self._body.update()

    def set_label(self, text):
        self._label.configure(text=text)

    def get_body(self):
        return self._body

    def open(self):
        self._body.mainloop()
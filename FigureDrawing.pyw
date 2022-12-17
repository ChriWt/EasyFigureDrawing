from Core.AppController import AppController
from Utils.Position import Position

from customtkinter import CTkButton

class Main:

    def __init__(self) -> None:
        self.application = AppController()

    def start(self) -> None:
        self.application.start()

if __name__ == "__main__":
    application = AppController()

    # f = application.get_view().new_frame(Position.TOP)
    # f.pack()

    # b = CTkButton(f, text="TOP")
    # b.pack()

    # f = application.get_view().new_frame(Position.CENTER)
    # f.pack()

    # b = CTkButton(f, text="CENTER", command=lambda: application.get_view().clear())
    # b.pack()

    # f = application.get_view().new_frame(Position.TOP)
    # f.pack(side="right")

    # b = CTkButton(f, text="TOP BOT")
    # b.pack()

    application.start()    

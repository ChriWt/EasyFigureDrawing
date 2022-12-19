from Core.AppController import AppController
from ImageSelection.HomePageController import HomePageController


class Main:

    def __init__(self) -> None:
        self._application = AppController()
        self._current_view_controller = None

    def start(self) -> None:
        self._current_view_controller = HomePageController(self._application)
        self._application.add_size_change_listener(self._current_view_controller.get_view())
        self._application.start()
        

if __name__ == "__main__":
    application = Main()
    application.start()

    # application = AppController()

    # from Utils.Position import Position

    # from customtkinter import CTkButton

    # from ttkbootstrap import Button
    # f = application.get_view().new_frame(Position.TOP)
    # f.pack()

    # b = Button(f, text="TOP")
    # b.pack()

    # f = application.get_view().new_frame(Position.CENTER)
    # f.pack()

    # b = Button(f, text="CENTER", command=lambda: application.get_view().clear())
    # b.pack()

    # f = application.get_view().new_frame(Position.RIGHT)
    # f.pack()

    # b = Button(f, text="RIGHT BOT")
    # b.pack()

    # f = application.get_view().new_frame(Position.BOTTOM)
    # f.pack()

    # b = Button(f, text="BOTTOM BOT")
    # b.pack()

    # f = application.get_view().new_frame(Position.LEFT)
    # f.pack()

    # b = Button(f, text="LEFT BOT")
    # b.pack()

    # application.get_view().configure(Position.BOTTOM, bootstyle="primary")

    # application.start()    

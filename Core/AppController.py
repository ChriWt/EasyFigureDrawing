from Core.AppView import AppView


class AppController:

    def __init__(self) -> None:
        self.view = AppView()
        
    def get_view(self) -> AppView:
        return self.view

    def start(self):
        self.view.start()
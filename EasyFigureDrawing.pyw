from customtkinter import CTk

from Controller.ResourceExplorerController import ResourceExplorerController
from Controller.TimelineManager import TimelineManager

from View.View import View


class EasyFigureDrawing:

    def __init__(self) -> None:
        self._loaded_controller = None
        self._window = None
        self.size = (1081, 500)
        self._initialize_app()
    
    def _initialize_app(self):
        self._window = CTk()
        self._window.minsize(self.size[0], self.size[1])
        TimelineManager.get_instance().set_root(self._window)

    def start(self):
        self._window.mainloop()

    def load_view(self, view: View) -> None:
        if view == View.RESOURCE_EXPLORER:
            self._load_resources_explorer_view()

    def _load_resources_explorer_view(self) -> None:
        self._loaded_controller = ResourceExplorerController(self)

    def get_window(self):
        return self._window    

if __name__ == "__main__":
    main = EasyFigureDrawing()
    main.load_view(View.RESOURCE_EXPLORER)
    main.start()

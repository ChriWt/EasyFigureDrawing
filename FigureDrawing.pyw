from Core.AppController import AppController
from DrawingSession.FigureDrawingController import FigureDrawingController
from ImageSelection.HomePageController import HomePageController
from Preprocessing.PreprocessingController import PreprocessingController


class Main:

    NORMAL_APP_SIZE = (1280, 700)
    SMALL_APP_SIZE = (480, 100)

    def __init__(self) -> None:
        self._application = AppController(self)
        self._current_view_controller = None

    def start_preprocessing(self) -> None:
        self._application.get_view().change_app_size(self.SMALL_APP_SIZE)
        self._current_view_controller = PreprocessingController(self._application)

    def start_home_page(self) -> None:
        self._application.get_view().clear()
        self._application.get_view().change_app_size(self.NORMAL_APP_SIZE)
        self._current_view_controller = HomePageController(self._application)
        self._application.add_size_change_listener(self._current_view_controller.get_view())

    def start_figure_drawing(self) -> None:
        self._current_view_controller = FigureDrawingController(self._application)

    def start(self) -> None:
        self.start_preprocessing()
        self._application.start()
        

if __name__ == "__main__":
    application = Main()
    application.start()
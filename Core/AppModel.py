

class AppModel:

    MINIATURE_FOLDER = r".Miniatures"
    RESOURCES_FOLDER = r"Resources"

    def __init__(self) -> None:
        self._references = []
        self._time = None

    def set_references(self, reference: list) -> None:
        self._references = reference
    
    def get_references(self) -> list:
        return self._references

    def set_time(self, time: int) -> None:
        self._time = time

    def get_time(self) -> int:
        return int(self._time)
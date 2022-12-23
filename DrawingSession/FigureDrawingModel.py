import random

from Core.AppModel import AppModel


class FigureDrawingModel:

    def __init__(self, references) -> None:
        self._references = references
        self._is_random = False
        self._previous_references = []
        self._index = 0

    def get_next(self) -> str:
        if len(self._references) - 1 == self._index:
            return None
        
        if self._is_random:
            return self._get_resource_file(self._get_random())
        
        self._index += 1
        image = self._get_resource_file(self._references[self._index])
        return image

    def get_previous(self) -> str:
        if self._index == 0:
            return None
        
        if self._is_random:
            return self._get_resource_file(self._get_random())

        self._index -= 1
        image = self._get_resource_file(self._references[self._index])
        
        return image

    def get_reference(self, index: int) -> str:
        return self._get_resource_file(self._references[index])

    def _get_random(self) -> int:
        return random.randrange(0, len(self._references))

    def _get_resource_file(self, image: str) -> str:
        return image.replace(AppModel.MINIATURE_FOLDER, AppModel.RESOURCES_FOLDER)
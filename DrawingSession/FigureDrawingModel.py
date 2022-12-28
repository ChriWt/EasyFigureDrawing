import random

from Core.AppModel import AppModel


class FigureDrawingModel:

    def __init__(self, model) -> None:
        self._references = model.get_references()
        self._timer = model.get_time()
        self._is_random = False
        self._previous_references = []
        self._index = 0

    def set_random_flag(self, flag: bool) ->None:
        self._is_random = flag

    def get_next(self) -> str:
        if len(self._references) - 1 == self._index:
            return None
        
        if self._is_random:
            return self._get_resource_file(self._references[self._get_random()])
        
        self._index += 1
        image = self._get_resource_file(self._references[self._index])
        return image

    def get_previous(self) -> str:
        if self._is_random:
            return self._get_resource_file(self._references[self._get_random()])

        if self._index == 0:
            return None

        self._index -= 1
        image = self._get_resource_file(self._references[self._index])
        
        return image

    def get_timer(self) -> int:
        return self._timer

    def get_reference(self, index: int) -> str:
        return self._get_resource_file(self._references[index])
    
    def get_current_reference(self) -> str:
        return self.get_reference(self._index)

    def _get_random(self) -> int:
        return random.randrange(0, len(self._references))

    def _get_resource_file(self, image: str) -> str:
        return image.replace(AppModel.MINIATURE_FOLDER, AppModel.RESOURCES_FOLDER)
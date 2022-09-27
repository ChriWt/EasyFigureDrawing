
import os

from Controller.TimelineManager import TimelineManager


class ResourceExplorerModel:
    
    RESOURCES = "./Resources/"

    MINIATURE = "./.Miniatures/"

    MINIATURE_TEMP = "./.Miniatures_temp/"

    def __init__(self) -> None:
        self._images = list()
        self._insertion_id = None
        self._delete_id = None
        self._timeline = TimelineManager.get_instance()

    def add_image(self, image: str) -> None:
        self._images.append(image)

    def is_image_already_saved(self, image: str) -> bool:
        return image in self._images 

    def remove_image(self, image: str) -> None:
        self._images.remove(image)
    
    def add_all(self, path: str) -> None:
        content = os.listdir(path)

        if self._delete_id is not None:
            self._timeline.stop(self._delete_id)
            self._delete_id = None

        def add(i=0):
            if i == len(content):
                self._insertion_id = None
                return
            
            if not self.is_image_already_saved(content[i]):
                self._images.append(os.path.join(path, content[i]))

            self._insertion_id = self._timeline.after(1, lambda: add(i+1))

        add()

    def remove_all(self, path: str) -> None:
        content = os.listdir(path)

        if self._insertion_id is not None:
            self._timeline.stop(self._insertion_id)
            self._insertion_id = None

        def delete(i=0):
            if i < 0:
                self._delete_id = None
                return
            
            try:
                self._images.remove(os.path.join(path, content[i]))
            except ValueError:
                pass
            self._timeline.after(1, lambda: delete(i - 1))
            
        delete(len(content) - 1)
        




import os
import shutil
import sys
from Controller.Miniature import Miniature
from Controller.TimelineManager import TimelineManager
from View.PreprocessView import PreprocessView

if sys.platform == "win32":
    print("windows")
    import ctypes

elif sys.platform == "darwin":
    print("macos")


class PreprocessController:

    def __init__(self, root, model) -> None:
        self._model = model

        self.id = None
        self.stop = False

        self._depth = self.calculate_dept(self._model.RESOURCES)
        
        self._elements_processed = 0
        self._view = PreprocessView(root.get_window(), self)
        self._view.set_label(str(self._depth))
        self._view.set_prefix("Total elements:")

        self._view.open()

    def start(self):
        self.stop = False
        self._view.set_prefix("Operation status:")
        os.mkdir(self._model.MINIATURE_TEMP)
        if sys.platform == "win32":
            ctypes.windll.kernel32.SetFileAttributesW(self._model.MINIATURE_TEMP, 0x02)
        self.miniaturize_image()

    def calculate_dept(self, path):
        dept = 0
        for element in os.listdir(path):
            file = os.path.join(path, element)
            if os.path.isdir(file):
                dept += self.calculate_dept(file)
            else: 
                dept += 1
        return dept

    def miniaturize_image(self):
        self.filter_out_files(self._model.RESOURCES, os.listdir(self._model.RESOURCES), self._model.MINIATURE_TEMP)

    def cancel(self):
        self.stop = True
        self._view.get_body().after_cancel(self.id)
        shutil.rmtree(self._model.MINIATURE_TEMP, ignore_errors=True)
        self._view.get_body().after(600, lambda: self._view.set_label("Operation cancelled"))
        self._view.get_body().after(600, lambda: self._view.update_progress_bar(0))

    def filter_out_files(self, folder, element, base):
        def next_item(i=0):
            if i == len(element):
                return 
            
            item = os.path.join(folder, element[i])
            if os.path.isdir(item):
                self.increment_elements()
                path = os.path.join(base, os.path.basename(item))
                try:
                    os.mkdir(path)
                except Exception:
                    pass
                resources = path.replace(self._model.MINIATURE_TEMP, self._model.RESOURCES)
                self.filter_out_files(resources, os.listdir(resources), path)
            else:
                self.increment_elements()
                path = item.replace(self._model.RESOURCES, self._model.MINIATURE_TEMP)
                miniature = Miniature(None, None, item, None)
                try:
                    miniature.load_image()
                    miniature.crop()
                    miniature.get_image().save(path)
                except Exception:
                    pass

            if not self.stop:
                try:
                    self.id = self._view.get_body().after(120, lambda: next_item(i + 1))
                except Exception:
                    pass

        next_item()

    def increment_elements(self):
        self._elements_processed += 1
        self._view.update_progress_bar(float(self._elements_processed / self._depth))
        self._view.update_label(self._elements_processed / self._depth * 100)

        if self._elements_processed == self._depth:
            self._view.set_label("Done!")
            self._view.get_body().after_cancel(self.id)
            shutil.rmtree(self._model.MINIATURE, ignore_errors=True)
            os.rename(self._model.MINIATURE_TEMP, self._model.MINIATURE)
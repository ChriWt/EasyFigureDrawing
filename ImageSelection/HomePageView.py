from __future__ import annotations
import os

import typing
from ImageSelection.Directory import Directory
from Preview.Preview import Preview
from Utils.CycleManager import CycleManager


from Utils.Position import Position
from ttkbootstrap import Frame, Treeview, Label, Progressbar
from ttkbootstrap.constants import END, BOTTOM, X, LEFT, Y, BOTH, RIGHT, HORIZONTAL, DETERMINATE
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap.style import *

from Utils.SizeChangeListener import SizeChangeListener

if typing.TYPE_CHECKING:
    from ImageSelection.HomePageController import HomePageController


class HomePageView(SizeChangeListener):
    
    _FRAME = "frame"
    _CONTENT = "content"
    _COL = "col"
    _ROW = "row"
    _ROW_SIZE = "row-size"

    _BACK = "↵ "
    _ARROW = "↦ "

    def __init__(self, controller: HomePageController) -> None:
        self._controller = controller
        
        view = self._controller.get_core().get_view()
        view.hide(Position.TOP)
        view.hide(Position.RIGHT)
        self._left_frame = view.new_frame(Position.LEFT)
        self._bottom_frame = view.new_frame(Position.BOTTOM)
        self._center_frame = view.new_frame(Position.CENTER)

        bottom_style = SECONDARY
        self._bottom_bar = Frame(self._bottom_frame, bootstyle=bottom_style)
        self._path_label = Label(self._bottom_bar, bootstyle="inverse-" + bottom_style)
        self._loading_state = Label(self._bottom_bar, bootstyle="inverse-" + bottom_style)
        self._progress_bar = Progressbar(self._bottom_bar, 
                                        bootstyle=(STRIPED, SUCCESS),
                                        orient=HORIZONTAL,
                                        mode=DETERMINATE,
                                        length=200,
                                        value=0)                                  

        self._directory_treeview = Treeview(self._left_frame)
        self._directory_treeview.bind("<Double-1>", self.on_directory_double_click)

        self._directory_loaded = {}
        self._current_visible = None

        self.directory_width = 0

        self._pack()

    def _pack(self) -> None:
        self._left_frame.pack(fill=Y, expand=True)
        self._bottom_frame.pack(fill=X, expand=True)
        self._center_frame.pack(fill=BOTH, expand=True)

        self._bottom_bar.pack(side=BOTTOM, fill=X, expand=True)
        self._path_label.pack(side=LEFT)
        self._progress_bar.pack(side=RIGHT, padx=(0,5))
        self._loading_state.pack(side=RIGHT, padx=(0, 5))
        self._directory_treeview.pack(fill=Y, expand=True)

    def insert_folder_content(self, parent: str, folders: list, add_back: bool=True) -> None:
        self._directory_treeview.heading('#0', text=parent, anchor='w')
        if add_back:
            self._directory_treeview.insert('', END, text=self._BACK + "..", open=False)
        for folder in folders:
            self._directory_treeview.insert('', END, text=self._ARROW + folder, open=False)

    def on_directory_double_click(self, _) -> None:
        if self._directory_treeview.selection():
            item = self._directory_treeview.selection()[0]
            self._controller.on_directory_click(self._directory_treeview.item(item,"text"))
    
    def clear_folders(self) -> None:
        for item in self._directory_treeview.get_children():
            self._directory_treeview.delete(item)

    def set_path(self, path: str) -> None:
        self._path_label.configure(text=path)

    def update(self, size: tuple) -> None:
        self._current_visible.update()
        self.directory_width = self._current_visible.winfo_width()
        CycleManager.get_instance().stop_all()
        self.optimize_image_spacing()

    def is_directory_loaded(self, folder: str) -> bool:
        return folder in self._directory_loaded

    def new_directory_container(self, folder: str) -> None:
        frame = ScrolledFrame(self._center_frame, autohide=True)
        self._directory_loaded[folder] = Directory(frame)
        frame.pack(fill=BOTH, expand=True)
        self._current_visible = frame

        frame.update()
        self.directory_width = frame.winfo_width() - 20 # Approximated Scrollbar's width

    def add_new_element(self, path: str) -> None:
        directory_frame = self._directory_loaded[os.path.dirname(path)]
        preview = Preview(directory_frame.get_frame(), path)
        
        self._place_preview(directory_frame, preview)
        directory_frame.get_frame().configure(height=(directory_frame.get_row() + 1) * Preview.VERTICAL_PHOTO_HEIGHT + (directory_frame.get_row() + 1) * 5)

        directory_frame.add_content(preview)

    def update_frame_size(self, path: str) -> None:
        directory_frame = self._directory_loaded[path]
        directory_frame.get_frame().configure(height=(directory_frame.get_row() + 1) * Preview.VERTICAL_PHOTO_HEIGHT + (directory_frame.get_row() + 1) * 5)

    def optimize_image_spacing(self):
        path = self._controller.get_model().get_full_path_current_folder()
        directory_frame = self._directory_loaded[path]
        directory_frame.reset_row()
        directory_frame.reset_current_row_size()
        manager = CycleManager.get_instance()
        size = directory_frame.get_count()

        def cycle(i=0):
            preview = directory_frame.get_preview(i)
            self._place_preview(directory_frame, preview)
            directory_frame.get_frame().configure(height=(directory_frame.get_row() + 1) * Preview.VERTICAL_PHOTO_HEIGHT + (directory_frame.get_row() + 1) * 5)
            self.update_progress_bar(i + 1, size)
            manager.after(1, lambda: cycle(i + 1))
        cycle()

    def update_progress_bar(self, current: int, total: int) -> None:
        if total == 0: return
        percentage = current / total * 100
        self._progress_bar['value'] = percentage
        self._loading_state['text'] = f"{current}/{total} ({percentage: .2f}%)"

    def change_progress_bar_state(self, state: bool) -> None:
        if state:
            self._progress_bar.pack(side=RIGHT, padx=(0,5))
            self._loading_state.pack(side=RIGHT, padx=(0,5))
        else: 
            self._progress_bar.pack_forget()
            self._loading_state.pack_forget()

    def _place_preview(self, directory_frame: Directory, preview: Preview) -> None:
        width, height = preview.get_size()

        if directory_frame.get_current_row_size() + width > self.directory_width:
            directory_frame.increment_row()
            directory_frame.reset_current_row_size()

        x = directory_frame.get_current_row_size()
        directory_frame.add_to_current_row_size(width)

        y = directory_frame.get_row() * Preview.VERTICAL_PHOTO_HEIGHT + directory_frame.get_row() * 5
        y += Preview.VERTICAL_PHOTO_HEIGHT / 2 - height / 2

        preview.place(x=x, y=y)

    def hide_current_directory_content(self) -> None:
        if self._current_visible is not None:
            self._current_visible.pack_forget()
    
    def show_directory_loaded(self, folder: str) -> None:
        if folder in self._directory_loaded:
            self._current_visible = self._directory_loaded[folder].get_frame()
            self._current_visible.pack(fill=BOTH, expand=True)
from __future__ import annotations
import os
import typing
from Controller.Miniature import Miniature
from Controller.TimelineManager import TimelineManager

from View.ImageMagnifier import newImageMagnifier

if typing.TYPE_CHECKING:
    from Controller.ResourceExplorerController import ResourceExplorerController

from customtkinter import CTkFrame, CTkLabel, CTkCheckBox, CTkButton, CTkProgressBar, CTkScrollbar, CTkCanvas
from tkinter import NW, RIGHT, Y, X, W, BOTH, BOTTOM, LEFT, TOP, WORD, END, Canvas,  Text, BooleanVar
from tkinter.ttk import Treeview, Separator
from PIL import Image, ImageTk


class ResourceExplorerView:

    VERTICAL_PHOTO_WIDTH = 160 
    VERTICAL_PHOTO_HEIGHT = 240

    HORIZONTAL_PHOTO_WIDTH = 240
    HORIZONTAL_PHOTO_HEIGHT = 360
    
    def __init__(self, controller: ResourceExplorerController) -> None:

        self._controller = controller
        self._window = self._controller.get_root_window()

        self._nodes = dict()
        self._photos = list()
        self._folder_content = list()
        self._area_used = 0
        self._file_index = 0
        self._current_folder_path = ""
        self._load_all_state = BooleanVar()
        self._load_more_button = None
        self._select_all = False
        self._timeline_manager = TimelineManager.get_instance()

        self._main_frame = CTkFrame(self._window)
        self._main_frame.pack(fill=BOTH, expand=True)

        self._top_frame = CTkFrame(self._main_frame)
        self._top_frame.pack(fill=BOTH, expand=True)

        self._file_explorer = CTkFrame(self._top_frame)
        self._file_explorer.pack(side=LEFT, fill=Y, anchor=W, pady=5, padx=(5, 0))

        self._content_explorer = CTkFrame(self._top_frame)
        self._content_explorer.pack(side=LEFT, fill=BOTH, expand=True, padx=(5, 5), pady=5)

        self._content_container = Text(self._content_explorer, wrap=WORD, borderwidth=0, state="disable", bg="#2a2d2e", cursor="arrow")
        self._content_container.pack(side=BOTTOM, fill=BOTH, expand=True, padx=5, pady=(0, 5))

        self._vertical_content_container_scrollbar = CTkScrollbar(self._top_frame, command=self._content_container.yview)
        self._vertical_content_container_scrollbar.pack(side=LEFT, fill=Y, anchor='e')

        self._content_config_container = CTkFrame(self._top_frame)
        self._content_config_container.pack(side=TOP, fill=Y, expand=True, padx=5, pady=(5, 5))

        self._bottom_bar_container = CTkFrame(self._main_frame)
        self._bottom_bar_container.pack(side=BOTTOM, fill=X)

        self._current_folder_label = CTkLabel(self._bottom_bar_container, text="", width=10)
        self._current_folder_label.pack(side=LEFT, padx=(5, 0))
        
        Separator(self._bottom_bar_container, orient="vertical").pack(side=LEFT, fill=Y, padx=10)

        self._loading_percentage = CTkLabel(self._bottom_bar_container)
        self._loading_progress_bar = CTkProgressBar(self._bottom_bar_container)

        self.folder_info = CTkLabel(self._bottom_bar_container, text="Files: 0", width=10)
        self.folder_info.pack(side=LEFT)

        Separator(self._bottom_bar_container, orient="vertical").pack(side=LEFT, fill=Y, padx=10)

        CTkButton(self._content_config_container, text="Select all", command=self._on_select_all_click).pack(side=TOP)
        
        CTkButton(self._content_config_container, text="Deselect all", command=self._on_deselect_all_click).pack(side=TOP)

        self._content_container.configure(yscrollcommand=self._vertical_content_container_scrollbar.set)

        CTkLabel(self._file_explorer, text="Resorces").pack(side=TOP, anchor=W)

        self._file_explorer_frame = CTkFrame(self._file_explorer)
        self._file_explorer_frame.pack(side=TOP, fill=Y, expand=True, pady=(0, 20), padx=5)

        self._file_system_tree = Treeview(self._file_explorer_frame, show="tree")
        self._file_system_tree.pack(side=LEFT, fill=Y)

        self._vertical_file_system_scrollbar = CTkScrollbar(self._file_explorer_frame, command=self._file_system_tree.yview)
        self._vertical_file_system_scrollbar.pack(side=LEFT, fill=Y)

        self.load_all = CTkCheckBox(self._bottom_bar_container, text="Load all", variable=self._load_all_state)
        self.load_all.pack(side=RIGHT, padx=5)

        self._file_system_tree.configure(yscroll=self._vertical_file_system_scrollbar.set)
        self._file_system_tree.bind('<<TreeviewOpen>>', self._open_node)
        self._file_system_tree.bind('<ButtonRelease>', self._open_node)

    def _on_select_all_click(self):
        self._controller.add_all(self._current_folder_path)
        for x in self._content_container.winfo_children():
            for y in x.winfo_children():
                if type(y) == CTkCheckBox:
                    y.select()

    def _on_deselect_all_click(self):
        self._controller.remove_all(self._current_folder_path)
        for x in self._content_container.winfo_children():
            for y in x.winfo_children():
                if type(y) == CTkCheckBox:
                    y.deselect()

    # def _on_select_all_click(self):
    #     self._controller.add_all(self._current_folder_path)
    #     content = self._content_container.winfo_children()
    #     def add(j = 0):
    #         if j == len(content):
    #             return
    #         children = content[j].winfo_children()
    #         def add_child(i = 0):
    #             if i == len(children):
    #                 self._timeline_manager.after(1, lambda: add(j + 1))
    #                 return
    #             widget = children[i]
    #             if type(widget) == CTkCheckBox:
    #                 widget.select()
    #             self._timeline_manager.after(1, lambda: add_child(i + 1))
    #         add_child()
    #     add()

    # def _on_deselect_all_click(self):
    #     self._controller.remove_all(self._current_folder_path)

    #     content = self._content_container.winfo_children()
    #     def remove(j = 0):
    #         if j == len(content):
    #             return
    #         children = content[j].winfo_children()
    #         def remove_child(i = 0):
    #             if i == len(children):
    #                 self._timeline_manager.after(1, lambda: remove(j + 1))
    #                 return
    #             widget = children[i]
    #             if type(widget) == CTkCheckBox:
    #                 widget.deselect()
    #             self._timeline_manager.after(1, lambda: remove_child(i + 1))
    #         remove_child()
    #     remove()

    def display_resource_folder(self, path: str) -> None:
        self._current_folder_path = path
        self._current_folder_label.configure(text="Folder: " + path)

        self._get_file_count(path, self._set_file_count)

        for folder in os.listdir(path):
            self._insert_tree_node('', folder, os.path.join(path, folder))

    def _insert_tree_node(self, parent: str, text: str, path: str) -> None:
        node = self._file_system_tree.insert(parent, "end", text=text, open=False)
        self._nodes[node] = path
        self._file_system_tree.insert(node, "end")
    
    def _open_node(self, event) -> None:
        node = self._file_system_tree.focus()
        abspath = self._nodes[node]

        def delete_children(content, i=0):
            try:
                self._file_system_tree.delete(content[i])
            except Exception:
                self._timeline_manager.stop_all()
                return
            self._timeline_manager.after(1, lambda: delete_children(content, i + 1))

        delete_children(self._file_system_tree.get_children(node))

        self._current_folder_label.configure(text="Folder: " + abspath)
        self._get_file_count(abspath, self._set_file_count)

        self._loading_progress_bar.pack(side=LEFT)
        self._loading_progress_bar.set(0)
        self._loading_percentage.pack(side=LEFT)
        self._loading_percentage.configure(text="0%", width=10)

        self._current_folder_path = abspath
        self._display_folder_content()

        if abspath and len(os.listdir(abspath)) < 10:
            for element in os.listdir(abspath):
                if not os.path.isfile(os.path.join(abspath, element)):
                    self._insert_tree_node(node, element, os.path.join(abspath, element))
        
    def _set_file_count(self, count):
        self.folder_info.configure(text=f"Files: {count}")

    def _display_folder_content(self) -> None:
        self.clear_container()
        self._photos = list()
        self._loading_progress_bar.pack(side=LEFT)
        self._loading_progress_bar.set(0)
        self._loading_percentage.pack(side=LEFT)
        self._loading_percentage.configure(text="0%", width=10)
        
        self._folder_content = os.listdir(self._current_folder_path)
      
        self._file_index = 0
        self._area_used = 0
        self._start_display() 

    def clear_container(self) -> None:
        self._content_container.configure(state="normal")
        self._content_container.delete("1.0", END)
        self._content_container.configure(state="disable")
        children = self._content_container.winfo_children()

        def destroy_children(children):
            if len(children) == 0:
                return
            
            # TODO da eliminare sto scempio
            try:
                children[0].destroy()
                children.remove(0)
            except Exception:
                pass

            self._timeline_manager.after(1, lambda: destroy_children(children))
        
        destroy_children(children)

    def _file_container_area(self) -> int:
        area = self._content_container.winfo_width() * self._content_container.winfo_height()
        return area + area / 2

    def _vert_base_area(self):
        return self.VERTICAL_PHOTO_HEIGHT * self.VERTICAL_PHOTO_WIDTH

    def _display_file(self) -> None:
        filename = self._folder_content[self._file_index]
        filepath = os.path.join(self._current_folder_path, filename)

        if os.path.isdir(filepath) or (not filename.endswith(".png") and not filename.endswith(".jpg") and not filename.endswith(".JPG") and not filename.endswith(".PNG")):
            return

        # photo, size = self._create_new_ImageTk(filepath)
        # self._photos.append(photo)
        # container = self._create_new_photo_container(photo, size, filepath)
        # newImageMagnifier(container, filepath)
        # self._area_used += size[0] * size[1]
        # self._content_container.window_create(END, window=container)
        container = Miniature(self._content_container, self, filepath)
        size = container.get_image_size()

        self._area_used += size[0] * size[1]
        self._content_container.window_create(END, window=container.get_body())

    def on_image_selected(self, canvas):
        print(canvas.get_path(), canvas.get_check_box_state())

    def _create_new_ImageTk(self, filepath: str):
        img = Image.open(filepath)

        width, height = img.size
        
        if height > width:
            img.thumbnail(size=(self.VERTICAL_PHOTO_WIDTH, self.VERTICAL_PHOTO_HEIGHT))
        else:
            img.thumbnail(size=(self.HORIZONTAL_PHOTO_WIDTH, self.HORIZONTAL_PHOTO_HEIGHT))

        return ImageTk.PhotoImage(img), img.size

    def _create_new_photo_container(self, photo, size, filepath):
        width, height = size

        canvas = CTkCanvas(self._content_container, 
                            width=width, 
                            bg="#2a2d2e", 
                            highlightthickness=1,
                            highlightbackground="#2a2d2e",
                            height=height)

        canvas.create_image(0, 0, anchor=NW, image=photo, tags="image")

        CTkCheckBox(canvas, text="", command=lambda: self._controller.on_image_click(filepath)).place(x=width - 24, y=height - 24)

        return canvas

    def _on_loading_finished(self, more_file):
        if more_file:
            self._display_load_more_button()
        else:
            if self._load_more_button is not None:
                self._load_more_button.destroy()
                self._load_more_button = None

        self._loading_progress_bar.pack_forget()
        self._loading_percentage.pack_forget()

    def _display_load_more_button(self):
        content = "\n" + " " * int(self._content_container.winfo_width() / 10 / 2)

        self._content_container.configure(state="normal")
        self._content_container.insert(END, content)
        self._load_more_button = CTkButton(self._content_container, text="Load more", command=lambda: self._remove_load_button_and_continue(len(content)))
        self._content_container.window_create(END, window=self._load_more_button)
        self._content_container.configure(state="disabled")

    def _remove_load_button_and_continue(self, space_size):
        self._load_more_button.destroy()
        self._content_container.configure(state="normal")
        self._content_container.delete("end-" + str(space_size + 1) + "c", END)
        self._content_container.configure(state="disabled")
        self._continue_loading()

    def _continue_loading(self):
        self._loading_progress_bar.pack(side=LEFT)
        self._loading_progress_bar.set(0)
        self._loading_percentage.pack(side=LEFT)
        self._loading_percentage.configure(text="0%", width=10)
        self._area_used = 0
        self._start_display()

    def _start_display(self):
        if self._file_index == len(self._folder_content):
            self._timeline_manager.stop_all()
            self._on_loading_finished(False)
            return 

        self._display_file()
        if self.load_all.get():
            self._loading_progress_bar.set(self._file_index / len(self._folder_content))
            self._loading_percentage.configure(text=f"{int(self._file_index / len(self._folder_content) * 100)}%")
        else:
            self._loading_progress_bar.set(self._file_index / (self._file_container_area() / self._vert_base_area()))
            perc = int(float((self._file_index / (self._file_container_area() / self._vert_base_area()))) * 100)
            self._loading_percentage.configure(text=f"{perc}%")
        self._file_index += 1

        if self._area_used > self._file_container_area() and not self.load_all.get():
            self._timeline_manager.stop_all()
            self._on_loading_finished(self._file_index != len(self._folder_content))
            return 
        
        self._timeline_manager.after(70, self._start_display)
        # self._id = self._timeline_manager.after(70, self._start_display)
        
    def _get_file_count(self, path, callback):
        content = os.listdir(path)
        abspath = os.path.abspath(path)

        if len(content) == 0: 
            callback(0)
            return 

        def check_if_file(i, count=0):
            if i == len(content):
                callback(count)
                return

            file = content[i]
            count += 1 if os.path.isfile(os.path.join(abspath, file)) else 0
            self._timeline_manager.after(1, lambda: check_if_file(i + 1, count))
        
        check_if_file(0)

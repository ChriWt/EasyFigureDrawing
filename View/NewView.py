from tkinter import BOTH, BOTTOM, END, LEFT, RIGHT, TOP, WORD, Y, Text, Menu
from customtkinter import CTkFrame
from Controller.Miniature import Miniature
from Controller.TimelineManager import TimelineManager
from View.CustomTreeView import CustomTreeview


class ResourceExplorerView:

    def __init__(self, controller) -> None:
        self._controller = controller
        self._timeline = TimelineManager.get_instance()

        self._loaded_folder = dict()
        self._current_path = ""

        self._main_frame, self._left_frame, self._right_frame = CTkFrame, CTkFrame, CTkFrame
        self._upper_left_frame, self._lower_left_frame = CTkFrame, CTkFrame

        self._folder_explorer_frame, self._folder_config_frame = CTkFrame, CTkFrame

        self._folder_explorer_tree = CustomTreeview

        self._menu_bar = Menu(self._controller.get_root_window())
        self._menu_bar.option_add('*tearOff', False)
        self._controller.get_root_window().config(menu=self._menu_bar)

        self._file_menu = Menu(self._menu_bar)
        self._file_menu.add_command(label="Process images", command=self._controller.preprocess_images)

        self._menu_bar.add_cascade(label="File", menu=self._file_menu)

        self._init()
        self._pack()

    def _init(self) -> None:
        self._main_frame = CTkFrame(self._controller.get_root_window())
        self._left_frame = CTkFrame(self._main_frame)
        self._right_frame = CTkFrame(self._main_frame)

        self._init_left_side()

    def _init_left_side(self):
        self._upper_left_frame = CTkFrame(self._left_frame)
        self._folder_explorer_tree = CustomTreeview(self._upper_left_frame, self)

        self._lower_left_frame = CTkFrame(self._left_frame)

    def _pack(self) -> None:
        self._main_frame.pack(fill=BOTH, expand=True)
        self._left_frame.pack(side=LEFT, fill=Y, expand=False, padx=5, pady=5)
        self._right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(0, 5), pady=5)

        self._upper_left_frame.pack(side=TOP, fill=Y, expand=True)
        self._folder_explorer_tree.pack(side=TOP, fill=Y, expand=True)

        self._lower_left_frame.pack(side=BOTTOM, fill=Y, expand=True)

    def add_folder_to_tree(self, folder_name):
        self._folder_explorer_tree.add_node(folder_name)

    def add_folder_content(self, miniature, original):
        container = self._loaded_folder[self._current_path]
        miniature = Miniature(container, self, miniature, original)
        miniature.pack()
        container.window_create(END, window=miniature.get_body())

    def on_load_request(self, path):
        self._timeline.stop_all()
        if self._current_path != "":
            self._loaded_folder[self._current_path].pack_forget()

        self._current_path = path
        
        if self._current_path not in self._loaded_folder:
            self._loaded_folder[self._current_path] = self._create_new_image_container()
            self.pack_current_folder()

        self._controller.on_load_request(path)

    def pack_current_folder(self):
        if self._current_path != "":
            self._loaded_folder[self._current_path].pack(side=LEFT, fill=BOTH, expand=True)

    def get_current_folder_content_container(self):
        return self._loaded_folder[self._current_path]

    def _create_new_image_container(self):
        return Text(self._right_frame, 
                    wrap=WORD, 
                    borderwidth=0, 
                    state="disable", 
                    bg="#2a2d2e", 
                    cursor="arrow")
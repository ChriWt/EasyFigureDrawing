

import os
from tkinter.ttk import Treeview

from customtkinter import CTkFrame, CTkScrollbar
from tkinter import END, LEFT, Y

from Controller.TimelineManager import TimelineManager
from Model.ResourceExplorerModel import ResourceExplorerModel

class CustomTreeview:

    def __init__(self, master, controller):
        self._controller = controller

        self._body = CTkFrame(master)
        self._treeview = Treeview(self._body, show="tree")
        self._scrollbar = CTkScrollbar(self._body, command=self._treeview.yview)
        
        self._timeline = TimelineManager.get_instance()

        self._nodes = dict()

        self._configure_tree()

    def _configure_tree(self):
        self._treeview.configure(yscrollcommand=self._scrollbar.set)
        self._treeview.bind('<<TreeviewOpen>>', self._open_node)

    def _open_node(self, _):

        def go_up(node, path = ""):
            if self._treeview.item(node)["text"] == "":
                return path

            child = node
            parent = self._treeview.parent(child)
            path = os.path.join(self._treeview.item(child)["text"], path) 

            return go_up(parent, path)

        path = go_up(self._treeview.selection()[0])
        path = path.replace(ResourceExplorerModel.RESOURCES, ResourceExplorerModel.MINIATURE)
        self._controller.on_load_request(path)

    def add_node(self, text):
        parent = self._treeview.focus()
        
        for iid in self._treeview.tag_has("empty"):
            if self._treeview.parent(iid) == parent:
                self._treeview.delete(iid)

        self._nodes[parent] = []
        node = self._treeview.insert(parent, END, text=text, open=False)
        
        # Used to make the inserted node expandable
        self._treeview.insert(node, END, tags="empty")

    def pack(self, **kwargs):
        self._treeview.pack(side=LEFT, fill=Y)
        self._scrollbar.pack(side=LEFT, fill=Y)
        self._body.pack(**kwargs)
    
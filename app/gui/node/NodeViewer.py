#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit, QTabWidget

from app.storage import smanager, sevents

from .NodeView import NodeViewe
from .NodeEdit import NodeEdit
from .NodeFiles import NodeFiles





class NodeViewer(QGroupBox):
	def __init__(self, parent=None):
		super(NodeViewer, self).__init__(parent)
		self.setTitle("viewer")
		self.main_layout = QVBoxLayout(self)


		self.storage = smanager.get_storage()


		self.__make_gui()


		sevents.eon("project_updated", self.__reload_data)
		sevents.eon("node_selected", self.__reload_data)





	def __make_gui(self):


		tabs = QTabWidget()
		self.main_layout.addWidget(tabs)


		node_view = NodeViewe()
		node_edit = NodeEdit()
		node_files = NodeFiles()

		tabs.addTab(node_view, "Просмотр")
		tabs.addTab(node_edit, "Редактирование")
		tabs.addTab(node_files, "Файлы")






	def __reload_data(self):


		title = "{}[{}]".format(self.storage.pnode.name, self.storage.pnode.ntype)
		self.setTitle(title)













#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit, QTabWidget

# from app.storage import smanager, sevents
from app.storage import storage

from .NodeView import NodeViewe
from .NodeEdit import NodeEdit
from .NodeFiles import NodeFiles





class NodeViewer(QGroupBox):
	def __init__(self, parent=None):
		super(NodeViewer, self).__init__(parent)
		self.setTitle("viewer")
		self.main_layout = QVBoxLayout(self)


		# self.storage = smanager.get_storage()


		tabs = QTabWidget()
		self.main_layout.addWidget(tabs)


		self.node_view = NodeViewe()
		self.node_edit = NodeEdit()
		self.node_files = NodeFiles()

		tabs.addTab(self.node_view, "Просмотр")
		tabs.addTab(self.node_edit, "Редактирование")
		tabs.addTab(self.node_files, "Файлы")


		# sevents.eon("project_updated", self.__reload_data)


		storage.s_selected.connect(self.__reload_data)

		self.node_edit.s_updated.connect(self.node_view.update_data)






	def __reload_data(self):


		title = "{}[{}]".format(storage.pnode.name, storage.pnode.ntype)
		self.setTitle(title)

		self.node_view.update_data()
		self.node_edit.update_data()
		self.node_files.update_data()













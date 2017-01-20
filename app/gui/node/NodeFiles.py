#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QPushButton
from .. import events

class NodeFiles(QGroupBox):
	def __init__(self, parent=None):
		super(NodeFiles, self).__init__(parent)
		self.setTitle("files")
		self.main_layout = QGridLayout(self)

		self.node = None
		# self.node_items = ("ntype", "uuid", "name", "ctime", "mtime", "path")
		# self.node_labels = {}

		self.label_files_len = QLabel()
		self.main_layout.addWidget(QLabel("files:"), 0, 0)
		self.main_layout.addWidget(self.label_files_len, 0, 1)

		btn_show = QPushButton("show")
		btn_show.clicked.connect(self.__show_files_modal)
		self.main_layout.addWidget(btn_show, 1, 0)
		# for index, item in enumerate(self.node_items):
		# 	self.main_layout.addWidget(QLabel(item), index, 0)

		# 	label = QLabel()
		# 	self.main_layout.addWidget(label, index, 1)
		# 	self.node_labels[item] = label


		#--- events
		events.on("update_current_node", self.__update_current)



	def update_node(self, node):
		self.node = node
		self.__update_current()
		


	def __update_current(self):

		node_files = self.node.files

		self.label_files_len.setText( str(len(node_files.files)) )
		

	def __show_files_modal(self):

		events.show_edit_files(self.node)
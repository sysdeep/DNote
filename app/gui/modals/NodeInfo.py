#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QTextEdit, QFormLayout, QLineEdit
from PyQt5.QtGui import QFont
from app.storage import storage
# from app.storage import smanager


class NodeInfo(QDialog):
	def __init__(self, parent=None):
		super(NodeInfo, self).__init__(parent)

		self.setWindowTitle("Node info")
		self.setMinimumHeight(400)
		self.setMinimumWidth(500)


		# self.main_layout = QGridLayout(self)
		self.main_layout = QVBoxLayout(self)


		# self.storage = smanager.get_storage()
		
		self.pnode = storage.pnode
		self.nnode = storage.nnode
		self.node_items = ("ntype", "uuid", "name", "ctime", "mtime", "path")
		self.node_labels = {}



		grid = QGridLayout()
		self.main_layout.addLayout(grid)

		#--- main data
		for index, item in enumerate(self.node_items):
			grid.addWidget(QLabel(item), index, 0)

			label = QLabel()
			grid.addWidget(label, index, 1)
			self.node_labels[item] = label

		#--- files
		index += 1
		node_files = self.nnode.files
		grid.addWidget(QLabel("Files:"), index, 0)
		grid.addWidget(QLabel( str(len(node_files.files)) ), index, 1)




		self.main_layout.addStretch()



		#--- controls
		c_box = QHBoxLayout()
		self.main_layout.addLayout(c_box)

		btn_close = QPushButton("Close")
		btn_close.clicked.connect(self.close)

		c_box.addStretch()
		c_box.addWidget(btn_close)

		self.__update_current()


	def __update_current(self):
		self.node_labels["ntype"].setText(self.pnode.ntype)
		self.node_labels["uuid"].setText(self.pnode.uuid)
		self.node_labels["name"].setText(self.pnode.name)
		# self.node_labels["path"].setText(self.node.meta.path)
		# self.node_labels["ctime"].setText(self.node.meta.get_ctime())
		# self.node_labels["mtime"].setText(self.node.meta.get_mtime())
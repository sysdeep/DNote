#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel
from .. import events

class NodeInfo(QGroupBox):
	def __init__(self, parent=None):
		super(NodeInfo, self).__init__(parent)
		self.setTitle("info meta")
		self.main_layout = QGridLayout(self)

		self.node = None
		self.node_items = ("ntype", "uuid", "name", "ctime", "mtime", "path")
		self.node_labels = {}




		for index, item in enumerate(self.node_items):
			self.main_layout.addWidget(QLabel(item), index, 0)

			label = QLabel()
			self.main_layout.addWidget(label, index, 1)
			self.node_labels[item] = label


		#--- events
		events.on("update_current_node", self.__update_current)



	def update_node(self, node):
		self.node = node
		self.__update_current()
		


	def __update_current(self):
		self.node_labels["ntype"].setText(self.node.meta.ntype)
		self.node_labels["uuid"].setText(self.node.meta.uuid)
		self.node_labels["name"].setText(self.node.meta.name)
		self.node_labels["path"].setText(self.node.meta.path)
		self.node_labels["ctime"].setText(self.node.meta.get_ctime())
		self.node_labels["mtime"].setText(self.node.meta.get_mtime())
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel


class NodeInfo(QGroupBox):
	def __init__(self, parent=None):
		super(NodeInfo, self).__init__(parent)
		self.setTitle("info meta")
		self.main_layout = QGridLayout(self)


		self.node_items = ("ntype", "uuid", "name", "ctime", "mtime", "atime", "path")
		self.node_labels = {}




		for index, item in enumerate(self.node_items):
			self.main_layout.addWidget(QLabel(item), index, 0)

			label = QLabel()
			self.main_layout.addWidget(label, index, 1)
			self.node_labels[item] = label


	def update_node(self, node):
		# print(dir(node))
		for item in self.node_items:
			value = getattr(node.meta, item)

			label = self.node_labels[item]
			label.setText(str(value))
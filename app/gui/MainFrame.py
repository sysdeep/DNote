#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
# from .Tree import Tree

from app.storage import get_controller

from .tree.Tree import Tree
from .node.NodeInfo import NodeInfo
from .node.NodeEditor import NodeEditor


class MainFrame(QWidget):
	def __init__(self, parent=None):
		super(MainFrame, self).__init__(parent)

		self.main_layout = QHBoxLayout()
		self.setLayout(self.main_layout)

		# label = QLabel("Tree")
		# self.main_layout.addWidget(label)
		# self.tree_view = Tree()
		# self.main_layout.addWidget(self.tree_view)

		self.storage = get_controller()

		# self.main_layout.addStretch()
		self.__make_tree_side()
		self.__make_node_side()




	def __make_tree_side(self):
		tree_side = QVBoxLayout()
		self.main_layout.addLayout(tree_side)
		

		self.tree_view = Tree()
		self.tree_view.select_cb = self.__on_select_node
		tree_side.addWidget(self.tree_view)

		# self.tree_stat = TreeStat()
		# tree_side.addWidget(self.tree_stat)


		# self.main_layout.addStretch()


	def __make_node_side(self):
		node_side = QVBoxLayout()
		self.main_layout.addLayout(node_side)

		

		self.node_info = NodeInfo()
		node_side.addWidget(self.node_info)
		# self.node_stat = NodeStat()
		# node_side.addWidget(self.node_stat)

		self.node_editor = NodeEditor()
		node_side.addWidget(self.node_editor)


		# node_side.addStretch()




	def __on_select_node(self, uuid):
		# print("---->", uuid)


		node = self.storage.get_node(uuid)
		# print(node)

		self.node_info.update_node(node)
		self.node_editor.update_node(node)

		# self.node_stat.update_node(node_id)

	# def update_tree(self):
	# 	self.tree_view.update_tree()


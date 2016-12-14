#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
# from .Tree import Tree

from app.storage import get_storage

from .tree.Tree import Tree
from .node.NodeInfo import NodeInfo
from .node.NodeEditor import NodeEditor

from .modal_create import ModalCreate


class MainFrame(QWidget):
	def __init__(self, parent=None):
		super(MainFrame, self).__init__(parent)

		self.main_layout = QHBoxLayout()
		self.setLayout(self.main_layout)

		# label = QLabel("Tree")
		# self.main_layout.addWidget(label)
		# self.tree_view = Tree()
		# self.main_layout.addWidget(self.tree_view)

		self.storage = get_storage()
		self.current_node = None

		# self.main_layout.addStretch()
		self.__make_tree_side()
		self.__make_node_side()




	def __make_tree_side(self):
		tree_side = QVBoxLayout()
		self.main_layout.addLayout(tree_side)
		

		self.tree_view = Tree()
		self.tree_view.select_cb = self.__on_select_node
		tree_side.addWidget(self.tree_view)


		tmp_btn_refresh = QPushButton("refresh")
		tmp_btn_refresh.clicked.connect(lambda: self.tree_view.update_tree())
		tree_side.addWidget(tmp_btn_refresh)


		# self.tree_stat = TreeStat()
		# tree_side.addWidget(self.tree_stat)


		# self.main_layout.addStretch()


	def __make_node_side(self):
		node_side = QVBoxLayout()
		self.main_layout.addLayout(node_side)

		
		btn_new_node = QPushButton("create")
		btn_new_node.clicked.connect(self.__create_node)
		node_side.addWidget(btn_new_node)


		self.node_info = NodeInfo()
		node_side.addWidget(self.node_info)
		# self.node_stat = NodeStat()
		# node_side.addWidget(self.node_stat)

		self.node_editor = NodeEditor()
		node_side.addWidget(self.node_editor)


		# node_side.addStretch()




	def __on_select_node(self, uuid):
		# print("---->", uuid)


		self.current_node = self.storage.get_node(uuid)
		# print(node)

		self.node_info.update_node(self.current_node)
		self.node_editor.update_node(self.current_node)

		# self.node_stat.update_node(node_id)

	# def update_tree(self):
	# 	self.tree_view.update_tree()






	def __create_node(self):



		# parent_node = self.current_node
		# print(parent_node)
		parent_project_node = self.storage.project.find_node_by_uuid(self.current_node.uuid)
		# print(self.current_node.uuid)
		# print(parent_project_node)


		modal = ModalCreate(parent_node=parent_project_node, parent=self)
		modal.show()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
# from .Tree import Tree
from app import log
from app.storage import storage
# from app.storage import get_storage, smanager, storage
from app import shared

from .tree.Tree import Tree
# from .node.NodeInfo import NodeInfo
# from .node.NodeEditor import NodeEditor
from .node.NodeViewer import NodeViewer
from .node.NodeFiles import NodeFiles
from .node.NodeControls import NodeControls

from . import events



class MainFrame(QWidget):
	def __init__(self, parent=None):
		super(MainFrame, self).__init__(parent)

		self.main_layout = QHBoxLayout()
		self.setLayout(self.main_layout)

		# label = QLabel("Tree")
		# self.main_layout.addWidget(label)
		# self.tree_view = Tree()
		# self.main_layout.addWidget(self.tree_view)

		# self.storage = smanager.get_storage()
		# self.storage = get_storage()
		self.current_node = None

		#--- make
		self.__make_tree_side()
		self.__make_node_side()


		# self.storage.eon("node_selected", self.__on_node_selected)
		# self.storage.eon("node_updated", self.__on_node_updated)

		#--- start
		self.start()





	def __make_tree_side(self):
		tree_side = QVBoxLayout()
		self.main_layout.addLayout(tree_side)
		

		self.tree_view = Tree()
		# self.tree_view.select_cb = self.__on_select_node
		# self.tree_view.update_tree()
		tree_side.addWidget(self.tree_view)


		tmp_btn_refresh = QPushButton("refresh")
		tmp_btn_refresh.clicked.connect(lambda: self.tree_view.update_tree())
		tree_side.addWidget(tmp_btn_refresh)


		# tmp_btn_save = QPushButton("save")
		# tmp_btn_save.clicked.connect(self.__force_save)
		# tree_side.addWidget(tmp_btn_save)


		# self.tree_stat = TreeStat()
		# tree_side.addWidget(self.tree_stat)


		# self.main_layout.addStretch()


	def __make_node_side(self):
		node_side = QVBoxLayout()
		self.main_layout.addLayout(node_side)


		#--- toolbar
		self.node_controls = NodeControls()
		node_side.addWidget(self.node_controls)

		# self.node_info = NodeInfo()
		# node_side.addWidget(self.node_info)
		# self.node_stat = NodeStat()
		# node_side.addWidget(self.node_stat)

		

		#--- edit text
		# self.node_editor = NodeEditor()
		# node_side.addWidget(self.node_editor)

		self.node_viewer = NodeViewer()
		node_side.addWidget(self.node_viewer)



		#--- node files
		# self.node_files = NodeFiles()
		# node_side.addWidget(self.node_files)

		# node_side.addStretch()



	def start(self):
		"""запуск"""
		# self.tree_view.update_tree()
		pass





	def __on_select_node(self, uuid):
		"""select node from tree..."""

		if uuid is None:
			log.warning("uuid = None")
			return


		log.debug("on select: " + uuid)


		# storage = smanager.get_storage()

		#--- show node data
		self.current_node = storage.get_node(uuid)
		# print(self.current_node)
		
		# shared.set_current_flag(self.current_node)
		
		# self.node_info.update_node(self.current_node)
		# self.node_editor.update_node(self.current_node)
		# self.node_files.update_node(self.current_node)

		#--- update tree node(in project.json)
		storage.project.set_current_flag(self.current_node.uuid)





	# def __on_node_selected(self):
	# 	"""from storage"""
	# 	node = self.storage.get_current_node()
	# 	self.label_node_name.setText(node.name)

	# def __on_node_updated(self):
	# 	"""from storage"""
	# 	# node = self.storage.get_current_node()
	# 	self.label_node_name.setText(self.current_node.name)





	#
	# def __force_save(self):
	# 	log.debug("force save - not implement")
	# 	# self.storage.project.write_file()
	#


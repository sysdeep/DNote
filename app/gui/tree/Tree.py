#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeView, QLabel, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

from app import log
from app.storage import get_storage

# from app.logic import get_tree
# from app.rc import get_icon_path
# from . import events, qicon


class Tree(QTreeView):
	def __init__(self, parent=None):
		super(Tree, self).__init__(parent)

		self.model = QStandardItemModel()
		self.model.setHorizontalHeaderLabels(['name'])
		self.setModel(self.model)
		self.setUniformRowHeights(True)
		self.setHeaderHidden(True)
		self.setFixedWidth(300)

		self.storage = get_storage()
		self.tree = self.storage.project.get_tree()
		self.select_cb = None


		self.current_index = None								# элемент с флагом current = True

		#--- menu
		self.setContextMenuPolicy(Qt.ActionsContextMenu)
		file_create_action = QAction("New catalog", self)
		self.addAction(file_create_action)

		# events.on("update_tree", self.__update_tree)
		# self.__make_tree()


		self.clicked.connect(self.__select)


	def __update_tree(self):
		self.current_index = None
		self.model.clear()
		self.__make_tree()


	def update_tree(self):
		self.__update_tree()






	def __make_tree(self):
		"""строим дерево"""

		#--- все элементы корня
		root_items = self.tree.get_nodes_level(1)		

		#--- запуск обхода дерева(рекурсия)
		for item in root_items:
			self.__wnode(item, self.model)


		#--- выбираем элемент у которого флаг current
		if self.current_index:
			self.setCurrentIndex(self.current_index)
			self.__select(self.current_index)
		#--- если текущего нет - первый
		else:
			index = self.model.index(0, 0)
			self.setCurrentIndex(index)
			self.__select(index)





	def __wnode(self, node, parent):
			"""
				рекурсивный обход элементов и добавление их на форму
			"""
			# if node.ntype == "f":
			# 	# icon = QIcon(get_icon_path("document-properties.png"))
			# 	icon = qicon("empty.png")
			# elif node.ntype == "d":
			# 	icon = qicon("folder.png")
			# 	# icon = QIcon(get_icon_path("document-open.png"))
			# 	# icon = QIcon(get_icon_path("document-open.png"))
			# else:
			# 	icon = QIcon(get_icon_path("list-remove.png"))



			row = QStandardItem(node.name)				# элемент строки
			# row.setIcon(icon)				# icon
			row.setEditable(False)							# editable - false

			row.setData(node.uuid, Qt.UserRole+1)


			


			
			parent.appendRow(row)							# добавляем

			if node.current:
				self.current_index = self.model.indexFromItem(row)
			# print(index)

			#--- ищем всех деток на уровень ниже(не дальше)
			# child_items = [node for node in simple_obj_list
			# 			   if (node["tree_lk"] > node_lk) and (node["tree_rk"] < node_rk) and(node["tree_level"] == node_level+1)]

			child_items = self.tree.get_childrens(node)
			# child_items = node.childrens


			#--- для каждого из деток вызываем рекурсию
			for node in child_items:
				self.__wnode(node, row)



			



	def __select(self, index):
		
		uuid = index.data(Qt.UserRole+1)
		# print(uuid)

		if self.select_cb:
			self.select_cb(uuid)
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeView, QLabel, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

from app import log
from app.rc import get_icon_path
from app.storage import get_storage

from ..modal_create import ModalCreate
from .. import events, qicon


class Tree(QTreeView):
	def __init__(self, parent=None):
		super(Tree, self).__init__(parent)

		self.tmodel = QStandardItemModel()
		self.tmodel.setHorizontalHeaderLabels(['name'])
		self.setModel(self.tmodel)
		self.setUniformRowHeights(True)
		self.setHeaderHidden(True)
		self.setFixedWidth(300)

		self.storage = get_storage()
		self.tree = self.storage.project.get_tree()
		self.select_cb = None


		self.current_uuid 	= None			# текущий uuid элемента
		self.current_index 	= None			# элемент с флагом current = True - для автоматического выбора(modelIndex)
		self.expand_indexes = []			# список элементов, которые необходимо раскрыть

		#--- menu
		self.__make_cmenu()



		events.on("update_tree", self.__update_tree)
		# self.__make_tree()



		#--- signals
		self.pressed.connect(self.__on_select)
		self.expanded.connect(self.__on_expanded)
		self.collapsed.connect(self.__on_collapsed)


	def __update_tree(self):
		self.current_index = None
		self.tmodel.clear()
		self.__make_tree()


	def update_tree(self):
		self.__update_tree()


	def __make_cmenu(self):
		"""контекстное меню"""
		self.setContextMenuPolicy(Qt.ActionsContextMenu)
		create_new_root 	= QAction("Новая корневая запись", self)
		create_new_parent 	= QAction("Новая запись для данного элемента", self)
		create_new_level 	= QAction("Новая запись такого же уровня", self)
		remove_item 		= QAction("Удалить запись", self)

		separator = QAction(self)
		separator.setSeparator(True)
		
		self.addAction(create_new_root)
		self.addAction(create_new_parent)
		self.addAction(create_new_level)
		self.addAction(separator)
		self.addAction(remove_item)
		# self.addSeparetor()


		create_new_root.setIcon(qicon("filesystems", "folder_blue.png"))
		create_new_parent.setIcon(qicon("filesystems", "folder_green.png"))
		create_new_level.setIcon(qicon("filesystems", "folder_orange.png"))
		remove_item.setIcon(qicon("actions", "remove.png"))

		create_new_root.triggered.connect(self.__act_create_new_root)
		create_new_parent.triggered.connect(self.__act_create_new_parent)
		create_new_level.triggered.connect(self.__act_create_new_level)
		remove_item.triggered.connect(self.__act_remove_item)




	def __make_tree(self):
		"""строим дерево"""
		self.blockSignals(True)

		#--- все элементы корня
		root_items = self.tree.get_nodes_level(1)		

		#--- запуск обхода дерева(рекурсия)
		for item in root_items:
			self.__wnode(item, self.tmodel)


		#--- выбираем элемент у которого флаг current
		if self.current_index:
			self.setCurrentIndex(self.current_index)
			self.__on_select(self.current_index)
		#--- если текущего нет - первый
		else:
			index = self.tmodel.index(0, 0)
			self.setCurrentIndex(index)
			self.__on_select(index)


		#--- разворачиваем элементы, у которых стоит флаг expanded
		for i in self.expand_indexes:
			self.expand(i)
		self.expand_indexes = []

		self.blockSignals(False)



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

			if node.ipack and node.icon:
				icon = QIcon(get_icon_path(node.ipack, node.icon))
			else:
				icon = QIcon(get_icon_path("empty.svg"))



			row = QStandardItem(node.name)				# элемент строки
			row.setIcon(icon)				# icon
			row.setEditable(False)							# editable - false

			row.setData(node.uuid, Qt.UserRole+1)


			


			
			parent.appendRow(row)							# добавляем

			if node.current:
				self.current_index = self.tmodel.indexFromItem(row)


			if node.expanded:
				index = self.tmodel.indexFromItem(row)
				self.expand_indexes.append(index)
			# print(index)

			#--- ищем всех деток на уровень ниже(не дальше)
			# child_items = [node for node in simple_obj_list
			# 			   if (node["tree_lk"] > node_lk) and (node["tree_rk"] < node_rk) and(node["tree_level"] == node_level+1)]

			child_items = self.tree.get_childrens(node)
			# child_items = node.childrens


			#--- для каждого из деток вызываем рекурсию
			for node in child_items:
				self.__wnode(node, row)



			



	def __on_select(self, index):
		"""событие от дерева о выбранном элементе"""		
		self.current_uuid = index.data(Qt.UserRole+1)

		if self.select_cb:
			self.select_cb(self.current_uuid)


	def __on_expanded(self, model_index):
		uuid = model_index.data(Qt.UserRole+1)
		self.storage.project.set_node_expanded(uuid, True)

	def __on_collapsed(self, model_index):
		uuid = model_index.data(Qt.UserRole+1)
		self.storage.project.set_node_expanded(uuid, False)




	#--- user actions ---------------------------------------------------------
	def __act_create_new_root(self):
		modal = ModalCreate(parent_node=None, parent=self)
		modal.exec_()
		self.update_tree()


	def __act_create_new_parent(self):
		"""выбранная нода - является родительской"""
		parent_pnode = self.storage.project.find_node_by_uuid(self.current_uuid)
		modal = ModalCreate(parent_node=parent_pnode, parent=self)
		modal.exec_()
		self.update_tree()

	def __act_create_new_level(self):
		"""выбранная нода - находится у родителя"""
		parent_pnode = self.storage.project.find_parent_node(self.current_uuid)
		print(parent_pnode)

		#--- если родитель - корень, то вызываем модал как и у __act_create_new_root
		if parent_pnode.tree_lk == 0:
			parent_pnode = None

		modal = ModalCreate(parent_node=parent_pnode, parent=self)
		modal.exec_()
		self.update_tree()


	def __act_remove_item(self):
		"""удаление ноды"""
		self.storage.remove_node(self.current_uuid)
		self.update_tree()
	#--- user actions ---------------------------------------------------------
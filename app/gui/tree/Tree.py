#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeView, QLabel, QAction, QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

from app import log
from app.rc import get_icon_path
from app.storage import get_storage, smanager, sevents

from .. import events, qicon

from .. import actions

from ..modals.ModalIcons import ModalIcons








class Tree(QTreeView):
	def __init__(self, parent=None):
		super(Tree, self).__init__(parent)

		self.tmodel = QStandardItemModel()
		self.tmodel.setHorizontalHeaderLabels(['name'])
		self.setModel(self.tmodel)
		self.setUniformRowHeights(True)
		self.setHeaderHidden(True)
		self.setFixedWidth(300)

		# self.storage = get_storage()
		self.storage = smanager.get_storage()
		self.tree = self.storage.get_tree()
		self.select_cb = None


		self.current_uuid 	= None			# текущий uuid элемента
		self.current_index 	= None			# элемент с флагом current = True - для автоматического выбора(modelIndex)
		self.expand_indexes = []			# список элементов, которые необходимо раскрыть



		#--- dnd
		# self.setDragDropMode(QAbstractItemView.InternalMove)
		# self.setDragEnabled(True)
		# self.viewport().setAcceptDrops(True)
		# self.setDropIndicatorShown(True)


		self.modal_icons = None



		#--- menu
		self.__make_cmenu()




		sevents.eon("storage_opened", self.__remake_tree)
		sevents.eon("project_updated", self.__update_tree)



		#--- signals
		self.pressed.connect(self.__on_select)
		self.expanded.connect(self.__on_expanded)
		self.collapsed.connect(self.__on_collapsed)


		# self.__remake_tree()


	# def dropEvent(self, ev):
	# 	print("drop")
	# 	print(ev)

	# 	ev.accept()

	def __remake_tree(self):
		print("remake tree")

		self.storage = smanager.get_storage()
		self.tree = self.storage.project.get_tree()

		# print(self.storage)

		self.current_uuid 	= None			# текущий uuid элемента
		self.current_index 	= None			# элемент с флагом current = True - для автоматического выбора(modelIndex)
		self.expand_indexes = []			# список элементов, которые необходимо раскрыть


		# print(self.storage.project_path)
		self.__update_tree()




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
		# create_new_level 	= QAction("Новая запись такого же уровня", self)
		
		edit_name 			= QAction("Изменить название", self)
		edit_icon 			= QAction("Изменить иконки", self)
		show_info 			= QAction("Информация", self)
		act_copy 			= QAction("Копировать", self)

		move_up				= QAction("Выше", self)
		move_down			= QAction("Ниже", self)

		remove_item 		= QAction("Удалить запись", self)

		separator1 = QAction(self)
		separator1.setSeparator(True)

		separator2 = QAction(self)
		separator2.setSeparator(True)

		separator3 = QAction(self)
		separator3.setSeparator(True)
		
		self.addAction(create_new_root)
		self.addAction(create_new_parent)
		# self.addAction(create_new_level)
		self.addAction(separator1)
		self.addAction(edit_name)
		self.addAction(edit_icon)
		self.addAction(show_info)
		self.addAction(act_copy)

		self.addAction(separator2)
		
		self.addAction(move_up)
		self.addAction(move_down)

		self.addAction(separator3)

		self.addAction(remove_item)
		# self.addSeparetor()


		create_new_root.setIcon(qicon("filesystems", "folder_blue.png"))
		create_new_parent.setIcon(qicon("filesystems", "folder_green.png"))
		# create_new_level.setIcon(qicon("filesystems", "folder_orange.png"))
		edit_name.setIcon(qicon("actions", "edit.png"))
		edit_icon.setIcon(qicon("actions", "frame_image.png"))
		show_info.setIcon(qicon("actions", "kdeprint_printer_infos.png"))
		act_copy.setIcon(qicon("actions", "editcopy.png"))
		remove_item.setIcon(qicon("actions", "remove.png"))

		move_up.setIcon(qicon("actions", "arrow_up.png"))
		move_down.setIcon(qicon("actions", "arrow_down.png"))

		create_new_root.triggered.connect(self.__act_create_new_root)
		create_new_parent.triggered.connect(self.__act_create_new_parent)
		# create_new_level.triggered.connect(self.__act_create_new_level)
		edit_name.triggered.connect(self.__act_edit_name)
		edit_icon.triggered.connect(self.__act_edit_icon)
		show_info.triggered.connect(self.__act_show_info)
		act_copy.triggered.connect(self.__act_copy)

		move_up.triggered.connect(self.__act_move_up)
		move_down.triggered.connect(self.__act_move_down)

		remove_item.triggered.connect(self.__act_remove_item)




	def __make_tree(self):
		"""строим дерево"""
		self.blockSignals(True)

		#--- все элементы корня
		root_items = self.tree.get_nodes_level(1)
		root_items.sort(key=lambda node: node.tree_lk)

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
				self.current_uuid = node.uuid


			if node.expanded:
				index = self.tmodel.indexFromItem(row)
				self.expand_indexes.append(index)
			# print(index)

			#--- ищем всех деток на уровень ниже(не дальше)
			# child_items = [node for node in simple_obj_list
			# 			   if (node["tree_lk"] > node_lk) and (node["tree_rk"] < node_rk) and(node["tree_level"] == node_level+1)]

			# child_items = self.tree.get_childrens(node)
			child_items = self.tree.find_childrens(node.uuid)
			# child_items = node.childrens


			#--- для каждого из деток вызываем рекурсию
			for node in child_items:
				self.__wnode(node, row)



			









	#--- user actions ---------------------------------------------------------
	def __on_select(self, index):
		"""
			событие от дерева о выбранном элементе
			прилетает сразу при построении дерева
			причём current_uuid == uuid
		"""
		#--- get selected uuid
		uuid = index.data(Qt.UserRole + 1)


		smanager.storage.select_node(uuid)

		# #--- get node from storage
		# node = smanager.storage.get_node(uuid)
		#
		# #--- set current node + emit
		# smanager.storage.set_current_node(node)
		#
		#
		# if uuid == self.current_uuid:
		# 	return False
		#
		self.current_uuid = uuid
		#
		# #--- update tree node(in project.json)
		# smanager.storage.project.set_current_flag(node.uuid)






	def __on_expanded(self, model_index):
		"""раскрытие узла"""
		uuid = model_index.data(Qt.UserRole + 1)
		self.storage.pmanager.set_node_expanded(uuid, True)

	def __on_collapsed(self, model_index):
		"""закрытие узла"""
		uuid = model_index.data(Qt.UserRole + 1)
		self.storage.pmanager.set_node_expanded(uuid, False)






	def __act_create_new_root(self):
		"""запрос на создание ноды от корня"""
		actions.show_modal_create_node(None)
		

	def __act_create_new_parent(self):
		"""выбранная нода - является родительской"""
		actions.show_modal_create_node(self.current_uuid)
		

	def __act_create_new_level(self):
		"""выбранная нода - находится у родителя - пока отключено!!!!!"""
		pass
		# parent_pnode = self.storage.project.find_parent_node(self.current_uuid)
		#
		# #--- если родитель - корень, то вызываем модал как и у __act_create_new_root
		# if parent_pnode.tree_lk == 0:
		# 	parent_pnode = None
		#
		# # events.show_modal_create_node(parent_node=parent_pnode)
		# actions.show_modal_create_node(parent_node=parent_pnode)
		





	def __act_remove_item(self):
		"""удаление ноды"""
		actions.show_modal_remove_node()


	def __act_edit_name(self):
		"""редактирование названия"""
		actions.show_modal_edit_name()

	def __act_edit_icon(self):
		"""редактирование иконки"""

		# events.show_edit_icon(self.current_uuid)
		self.modal_icons = ModalIcons(self.__on_icon_selected, parent=self)
		self.modal_icons.show()


	def __act_show_info(self):
		"""информация о ноде"""
		actions.show_modal_node_info()



	def __act_copy(self):
		"""копирование ветки"""

		log.debug("copy node: " + self.current_uuid)

		# self.storage.set_copy_node(self.current_uuid)



	def __act_move_up(self):
		result = self.storage.pmanager.move_node_up(self.current_uuid)
		if result:
			self.storage.update_project_file()


	def __act_move_down(self):
		result = self.storage.pmanager.move_node_down(self.current_uuid)
		if result:
			self.storage.update_project_file()
	#--- user actions ---------------------------------------------------------




	def __on_icon_selected(self, ipack, icon):

		node = smanager.storage.pnode
		node.ipack = ipack
		node.icon = icon

		self.modal_icons.set_close()
		self.modal_icons = None

		smanager.storage.update_project_file()
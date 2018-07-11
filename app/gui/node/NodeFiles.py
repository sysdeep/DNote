#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import time
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem, QFileDialog, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from .. import events
from app.storage import get_storage, smanager, sevents











class NodeFiles(QWidget):
	def __init__(self, parent=None):
		super(NodeFiles, self).__init__(parent)
		

		self.main_layout = QVBoxLayout(self)

		# self.node = None
		# self.storage = smanager.get_storage()
		# self.storage = get_storage()
		

		edit_box = QHBoxLayout()
		self.main_layout.addLayout(edit_box)

		self.clist = QListWidget()
		self.clist.itemClicked.connect(self.__on_select_item)
		edit_box.addWidget(self.clist)


		actions_box = QVBoxLayout()
		edit_box.addLayout(actions_box)

		btn_add = QPushButton("add")
		btn_add.clicked.connect(self.__on_add_action)

		self.btn_remove = QPushButton("remove")
		self.btn_remove.clicked.connect(self.__on_remove_action)
		self.btn_remove.setDisabled(True)

		actions_box.addWidget(btn_add)
		actions_box.addWidget(self.btn_remove)
		actions_box.addStretch()



		self.current_file = None


		sevents.eon("node_selected", self.__update_node_data)
		#--- events
		# events.on("update_current_node", self.__update_current)

	# def update_node(self, node):
	# 	self.node = node
	# 	self.__update_current()
	# 	self.__load_files()
		

	def keyPressEvent(self, QKeyEvent):
		"""обработка сочетаний клавиш"""

		#--- вставка
		if QKeyEvent.matches(QKeySequence.Paste):

			clipboard = QApplication.clipboard()
			mime = clipboard.mimeData()

			if mime.hasImage():
				print("image")
				image = clipboard.image()

				node = smanager.get_storage().nnode
				file_path = os.path.join(node.files.path, "pasted_{}.png".format(time.time()))
				print(file_path)
				image.save(file_path)
				node.reload_files()


				self.__load_files()

			if mime.hasText():
				print("Text")

				print(clipboard.text())
			# print(mime)


	def __update_node_data(self):
		# self.node = smanager.storage.get_current_node()
		self.__load_files()
		

	def __show_files_modal(self):

		events.show_edit_files(self.node)


	def __load_files(self):
		# self.current_ipack = ICON_PACKS[index]

		self.clist.clear()

		storage = smanager.get_storage()
		files = storage.nnode.files.files

		# self.clist.clear()
		for f in files:

			# icon = QIcon(get_icon_path(self.current_ipack, f))
			# item = QListWidgetItem(icon, f)
			item = QListWidgetItem(f)
			item.setData(Qt.UserRole+1, f)
			self.clist.addItem(item)

	



	def __on_add_action(self):
		fname = QFileDialog.getOpenFileName(self, "Open")			# (file_name, file_filter)

		# print(fname)

		if fname[0]:
			storage = smanager.get_storage()
			storage.nnode.create_file(fname[0])

			#--- send events
			# events.update_current_node()				# update_tree - вызовет и это

		self.__load_files()


	def __on_remove_action(self):
		storage = smanager.get_storage()
		storage.nnode.remove_file(self.current_file)

		self.__load_files()


	def __on_select_item(self, list_item):
		self.current_file = list_item.data(Qt.UserRole+1)
		

		if not self.btn_remove.isEnabled():
			self.btn_remove.setDisabled(False)



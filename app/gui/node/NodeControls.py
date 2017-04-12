#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QToolBar

from app import shared
from app.storage import smanager


from ..modals.ModalIcons import ModalIcons
from .. import events, qicon
from .. import actions


class NodeControls(QWidget):
	def __init__(self, parent=None):
		super(NodeControls, self).__init__(parent)

		# self.storage = get_storage()


		self.modal_icons = None

		self.main_layout = QHBoxLayout(self)

		self.bar = QToolBar("tools")
		action_create = self.bar.addAction(qicon("filesystems", "folder_green.png"), "Create")
		action_create.triggered.connect(self.__create_node)

		action_remove = self.bar.addAction(qicon("actions", "remove.png"), "Remove")
		action_remove.triggered.connect(self.__remove_node)

		action_icon = self.bar.addAction(qicon("actions", "frame_image.png"), "Icon")
		action_icon.triggered.connect(self.__show_icons)

		action_ch_name = self.bar.addAction(qicon("actions", "edit.png"), "ch name")
		action_ch_name.triggered.connect(self.__show_ch_name)

		action_info = self.bar.addAction(qicon("actions", "kdeprint_printer_infos.png"), "Info")
		action_info.triggered.connect(self.__show_node_info)

		

		# btn_create = QPushButton("Create")
		# btn_create.clicked.connect(self.__create_node)

		# btn_remove = QPushButton("Remove")
		# btn_remove.clicked.connect(self.__remove_node)

		# btn_icon = QPushButton("Icon")
		# btn_icon.clicked.connect(self.__show_icons)

		# btn_ch_name = QPushButton("ch name")
		# btn_ch_name.clicked.connect(self.__show_ch_name)

		# btn_info = QPushButton("Info")
		# btn_info.clicked.connect(self.__show_node_info)

		# self.main_layout.addWidget(btn_create)
		# self.main_layout.addWidget(btn_remove)
		# self.main_layout.addWidget(btn_icon)
		# self.main_layout.addWidget(btn_ch_name)
		# self.main_layout.addWidget(btn_info)

		self.main_layout.addWidget(self.bar)




	def __create_node(self):
		"""создание новой ноды от родителя"""
		actions.show_modal_create_node(smanager.storage.pnode.uuid)


	def __remove_node(self):
		"""удаление ноды от родителя"""
		actions.show_modal_remove_node()


	def __show_icons(self):
		self.modal_icons = ModalIcons(self.__on_icon_selected, parent=self)
		self.modal_icons.show()


	def __show_node_info(self):
		actions.show_modal_node_info()


	def __show_ch_name(self):
		actions.show_modal_edit_name()



	def __on_icon_selected(self, ipack, icon):

		node = smanager.storage.pnode
		node.ipack = ipack
		node.icon = icon

		self.modal_icons.set_close()
		self.modal_icons = None

		smanager.storage.update_project_file()

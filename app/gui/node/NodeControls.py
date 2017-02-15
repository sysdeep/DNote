#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QToolBar

from app import shared
from app.storage import get_storage

from .. import events, qicon


class NodeControls(QWidget):
	def __init__(self, parent=None):
		super(NodeControls, self).__init__(parent)

		self.storage = get_storage()

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
		node = shared.get_current_node()
		parent_project_node = self.storage.project.find_node_by_uuid(node.uuid)
		events.show_modal_create_node(parent_node=parent_project_node)

	def __remove_node(self):
		"""удаление ноды от родителя"""
		node = shared.get_current_node()
		events.show_remove_node(node.uuid)

	def __show_icons(self):

		node = shared.get_current_node()
		events.show_edit_icon(node.uuid)


	def __show_node_info(self):
		# node = shared.get_current_node()
		# events.show_node_info(node.uuid)
		events.show_current_node_info()


	def __show_ch_name(self):
		events.show_edit_name()
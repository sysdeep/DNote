#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	Controller - обслуживает все евенты
"""


# import json
# import os
from . import events
from app import log
from app.storage import get_storage

from .modal_create import ModalCreate
from .modal_remove import ModalRemove
from .modal_edit_name import ModalEditName
from .modal_icons import ModalIcons
from .modal_files import ModalFiles


class Controller(object):
	def __init__(self, parent):
		self.parent 	= parent
		self.storage 	= get_storage()
		self.current_uuid	= None

		#--- events
		events.on("show_modal_create_node", self.__on_show_modal_create_node)
		events.on("show_remove_node", self.__on_show_remove_node)
		events.on("show_edit_name", self.__on_show_edit_name)
		events.on("show_edit_icon", self.__on_show_edit_icon)
		events.on("show_edit_files", self.__on_show_edit_files)

		events.on("selected_icon", self.__on_selected_icon)


	
	def __on_show_modal_create_node(self, parent_node):
		"""отображение модального окна создания новой записи"""
		modal = ModalCreate(parent_node=parent_node, parent=self.parent)
		modal.exec_()

		# events.update_tree()



	def __on_show_remove_node(self, node_uuid):
		"""отображение модального окна удаления записи"""

		modal = ModalRemove(node_uuid=node_uuid, parent=self.parent)
		modal.exec_()

		# events.update_tree()


	def __on_show_edit_name(self, node_uuid):
		"""отображение модального окна изменения названия"""

		
		modal = ModalEditName(node_uuid=node_uuid, parent=self.parent)
		modal.exec_()



	#--- icons ----------------------------------------------------------------
	def __on_show_edit_icon(self, node_uuid):
		"""отображение модального окна изменения иконки"""
		
		self.current_uuid = node_uuid
		modal = ModalIcons(parent=self.parent)
		modal.exec_()


	def __on_selected_icon(self, ipack, icon):
		"""событие о выбранной иконке"""

		project_node = self.storage.project.find_node_by_uuid(self.current_uuid)

		project_node.ipack = ipack
		project_node.icon = icon

		self.storage.project.write_file()
		events.update_tree()
	#--- icons ----------------------------------------------------------------


	def __on_show_edit_files(self, node):
		"""отображение модального окна изменения иконки"""
		
		# self.current_uuid = node_uuid
		modal = ModalFiles(node, parent=self.parent)
		modal.exec_()



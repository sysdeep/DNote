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


class Controller(object):
	def __init__(self, parent):
		self.parent 	= parent
		self.storage 	= get_storage()


		#--- events
		events.on("show_modal_create_node", self.__on_show_modal_create_node)
		events.on("show_remove_node", self.__on_show_remove_node)
		events.on("show_edit_name", self.__on_show_edit_name)


	
	def __on_show_modal_create_node(self, parent_node):
		"""отображение модального окна создания новой записи"""
		modal = ModalCreate(parent_node=parent_node, parent=self.parent)
		modal.exec_()

		# events.update_tree()



	def __on_show_remove_node(self, node_uuid):
		"""отображение модального окна удаления записи"""

		modal = ModalRemove(node_uuid=node_uuid)
		modal.exec_()

		# events.update_tree()


	def __on_show_edit_name(self, node_uuid):
		"""отображение модального окна изменения названия"""

		print("edit name")
		modal = ModalEditName(node_uuid=node_uuid)
		modal.exec_()

		# events.update_tree()


	# def set_save_file(self, path):

	# 	store_tree(path)
	


	# def set_open_file(self, path):
	# 	log.info("open db file: " + path)
	# 	load_tree(path)
	# 	events.update_tree()



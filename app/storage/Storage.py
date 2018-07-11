#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Storage - объект, управляющий нодами и деревом проекта
"""
import uuid
import os

from app import log
from app.lib.EventEmitter import EventEmitter, Signal

from .nodes.Nodes import Nodes, NODE_TYPES
from .project.Project import Project
from . import sevents


# from .SNode import SNode





class Storage(object):
	"""
		Объект хранилища
	"""

	s_opened = Signal()				# storage was opened
	s_selected = Signal()			# node was selected
	s_updated = Signal()

	def __init__(self):

		self.storage_path 	= ""				# полный путь к каталогу хранилища

		self.nmanager 		= Nodes()					# управление нодами
		self.pmanager		= Project()					# управление файлом проекта

		self.nnode = None
		self.pnode = None


		self.__events = EventEmitter()

		# self.copy_node_uuid = None


	# def __init__(self, storage_path):
	#
	# 	self.storage_path 	= storage_path				# полный путь к каталогу хранилища
	#
	# 	self.nmanager 		= Nodes(self.storage_path)					# управление нодами
	# 	self.pmanager		= Project(self.storage_path)					# управление файлом проекта
	#
	# 	self.nnode = None
	# 	self.pnode = None





	def open_storage(self, storage_path):
		"""открытие нового хранилища"""
		log.debug("открытие хранилища: " + storage_path)
		self.storage_path = storage_path

		self.nmanager.setup(storage_path)
		self.pmanager.setup(storage_path)

		log.debug("хранилище открыто")
		self.s_opened.emit()




	def get_tree(self):
		return self.pmanager.get_tree()









	def select_node(self, uuid):
		"""выбор текущих нод"""
		self.nnode = self.nmanager.get_node(uuid)
		self.pnode = self.pmanager.get_node(uuid)
		self.pmanager.set_current_flag(uuid)
		self.s_selected.emit()






	def create_node(self, parent_node_uuid, name, ntype="text", content=""):
		"""создать новую ноду"""
		log.debug("создание новой ноды")

		#--- создание файлов ноды
		self.nnode = self.nmanager.create_node(content)

		#--- создание ноды в файле проекта
		self.pnode = self.pmanager.create_node(parent_node_uuid, self.nnode.uuid, name, ntype)

		sevents.node_created()
		sevents.project_updated()



	
	def remove_node(self, uuid):
		"""удалить заданную ноду или ветвь"""
		log.debug("удаление ноды: " + uuid)

		#--- удаление ноды(ветки) в файле проекта
		remove_nodes = self.pmanager.remove_node(uuid)


		for node in remove_nodes:
			#--- удаление файлов ноды
			self.nmanager.remove_node(node.uuid)



		#--- сброс текущей
		self.nnode = None
		self.pnode = None

		sevents.node_removed()
		sevents.project_updated()





	def update_project_file(self):
		self.pmanager.write_file()

		sevents.project_updated()


	def update_node_event(self):

		sevents.node_updated()



	#--- !!!
	# def copy_node(self, node_uuid, parent_node_uuid):
	# 	log.debug("копирование ноды")
	#
	# 	self.nnode = self.nmanager.copy_node(node_uuid)
	#
	# 	self.pnode = self.pmanager.copy_node(node_uuid)




	def get_node_types(self):
		"""получить список поддерживаемых форматов"""
		return NODE_TYPES


	

	#
	# def set_copy_node(self, node_uuid):
	# 	self.copy_node_uuid = node_uuid





	#--- 2018.07.11 -----------------------------------------------------------
	# def update_page_text(self, text):
	# 	self.nnode.update_page_text(text)
	#
	# 	#--- send event
	# 	storage.update_node_event()
	#--- 2018.07.11 -----------------------------------------------------------




	def eon(self, event, cb):
		self.__events.eon(event, cb)

	def emit(self, event_name, *args, **kwargs):
		self.__events.emit(event_name, *args, **kwargs)




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Storage - объект, управляющий нодами и деревом проекта
"""
import uuid
import os

from app import log
# from app.lib import EventEmitter

from .nodes.Nodes import Nodes, NODE_TYPES
from .project.Project import Project
from . import sevents


# from .SNode import SNode





class Storage(object):
	"""
		Объект хранилища
	"""
	def __init__(self, storage_path):

		self.storage_path 	= storage_path				# полный путь к каталогу хранилища

		self.nmanager 		= Nodes(self.storage_path)					# управление нодами
		self.pmanager		= Project(self.storage_path)					# управление файлом проекта

		# self.current_node	= None						# тек. нода


		# self.snode = None
		# self.copy_node_uuid = None

		self.nnode = None
		self.pnode = None

		# self.__load()




	def get_tree(self):
		return self.pmanager.get_tree()









	def select_node(self, uuid):
		"""выбор текущих нод"""
		self.nnode = self.nmanager.get_node(uuid)
		self.pnode = self.pmanager.get_node(uuid)
		self.pmanager.set_current_flag(uuid)
		sevents.node_selected()






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










	def get_node_types(self):
		"""получить список поддерживаемых форматов"""
		return NODE_TYPES


	


	def set_copy_node(self, node_uuid):
		self.copy_node_uuid = node_uuid








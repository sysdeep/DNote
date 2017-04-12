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

		self.nodes 			= Nodes()					# управление нодами
		self.project		= Project()					# управление файлом проекта

		self.current_node	= None						# тек. нода


		# self.snode = None
		# self.copy_node_uuid = None

		self.__load()




	def __load(self):
		"""загрузить проект по заданному пути"""

		#--- загружаем данные проекта
		self.project.load(self.storage_path)

		#--- настраиваем объект записей
		self.nodes.set_project_path(self.storage_path)





	def get_current_node(self):
		return self.current_node

	def set_current_node(self, node):
		self.current_node = node
		sevents.node_selected()



	def get_node(self, uuid):
		"""получить заданную ноду из хранилища"""
		node = self.nodes.get_node(uuid)
		node.storage = self
		# self.set_current_node(node)


		#--- new test
		# pnode = self.project.get_node(uuid)
		# self.snode = SNode(node, pnode, self.project)

		# print(self.snode.name)
		# print(self.snode.uuid)

		#--- new test



		return node



	def create_node(self, parent_node, name):
		"""создать новую ноду"""
		log.debug("создание новой ноды")

		#--- создание файлов ноды
		node = self.nodes.create_node(name, storage=self)

		#--- создание ноды в файле проекта
		self.project.create_node(parent_node, node.uuid, name)

		#--- выбираем созданную
		self.set_current_node(node)

		sevents.node_created()
		return node



	
	def remove_node(self, uuid):
		"""удалить заданную ноду"""
		log.debug("удаление ноды: " + uuid)

		#--- удаление файлов ноды
		self.nodes.remove_node(uuid)

		#--- удаление ноды в файле проекта
		self.project.remove_node(uuid)

		#--- сброс текущей
		self.current_node = None

		sevents.node_removed()
		return True



	def get_node_types(self):
		"""получить список поддерживаемых форматов"""
		return NODE_TYPES


	


	def set_copy_node(self, node_uuid):
		self.copy_node_uuid = node_uuid








#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Storage - объект, управляющий нодами и деревом проекта
"""
import uuid
import os

from app import log
from app.lib import EventEmitter

from .nodes.Nodes import Nodes, NODE_TYPES
from .project.Project import Project





class Storage(object):
	def __init__(self):
		self.nodes 			= Nodes()					# управление нодами
		self.project		= Project()					# управление файлом проекта
		self.project_path 	= ""						# полный путь к каталогу проекта

		self.current_node	= None						# тек. нода
		self.__emitter		= EventEmitter()


	def load_project(self, project_path):
		"""загрузить проект по заданному пути"""
		self.project_path 	= project_path
		self.project.load(self.project_path)
		self.nodes.set_project_path(self.project_path)


	def get_current_node(self):
		return self.current_node


	def get_node(self, uuid):
		"""получить заданную ноду из хранилища"""
		node = self.nodes.get_node(uuid)
		node.storage = self
		self.current_node = node
		self.emit("node_selected")
		return node



	def create_node(self, parent_node, name):
		"""создать новую ноду"""
		log.debug("создание новой ноды")

		#--- создание файлов ноды
		node = self.nodes.create_node(name)
		node_uuid = node.uuid
		node.storage = self
		self.current_node = node
		self.emit("node_selected")
		#--- создание ноды в файле проекта
		self.project.create_node(parent_node, node_uuid, name)
		self.project.write_file()

		return node



	
	def remove_node(self, uuid):
		"""удалить заданную ноду"""
		log.debug("удаление ноды: " + uuid)

		#--- удаление файлов ноды
		self.nodes.remove_node(uuid)

		#--- удаление ноды в файле проекта
		self.project.remove_node(uuid)
		# self.project.tree.print_nodes()
		
		self.project.write_file()

		self.current_node = None
		return True



	def get_node_types(self):
		return NODE_TYPES


	#--- events ---------------------------------------------------------------
	def eon(self, event_name, cb):
		"""подписаться на события"""
		self.__emitter.eon(event_name, cb)

	def eoff(self, event_name, cb):
		self.__emitter.eoff(event_name, cb)

	def emit(self, event, *args, **kwargs):
		self.__emitter.emit(event, *args, **kwargs)
	#--- events ---------------------------------------------------------------





	










if __name__ == '__main__':
	

	controller = Storage()
	controller.load_project_default()
	# controller.create_node()

	controller.project.tree.print_nodes()


	# controller.create_top_node("test_1")
	# controller.create_top_node("test_2")
	# controller.create_top_node("test_3")



	# controller.project.tree.print_nodes()

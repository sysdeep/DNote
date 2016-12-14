#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Storage - объект, управляющий нодами и деревом проекта
"""
import uuid
import os

from app import log


from .nodes.Nodes import Nodes
from .project.Project import Project





class Storage(object):
	def __init__(self):
		self.nodes 			= Nodes()					# управление нодами
		self.project		= Project()					# управление файлом проекта
		self.project_path 	= ""						# полный путь к каталогу проекта




	def load_project(self, project_path):
		"""загрузить проект по заданному пути"""
		self.project_path 	= project_path
		self.project.load(self.project_path)
		self.nodes.set_project_path(self.project_path)








	def create_node(self, parent_node, name):
		log.debug("создание новой ноды")

		#--- создание файлов ноды
		node_uuid = self.nodes.create_node(name)

		#--- создание ноды в файле проекта
		self.project.create_node(parent_node, node_uuid, name)
		self.project.write_file()

		return True





	def create_node_top(self, name):
		log.debug("создание новой ноды - top")

		#--- создание файлов ноды
		node_uuid = self.nodes.create_node(name)

		#--- создание ноды в файле проекта
		self.project.create_node_top(node_uuid, name)
		self.project.write_file()

		return True



	def get_node(self, uuid):
		# node_path = os.path.join(self.project_path, "nodes", uuid)
		return self.nodes.get_node(uuid)








if __name__ == '__main__':
	

	controller = Storage()
	controller.load_project_default()
	# controller.create_node()

	controller.project.tree.print_nodes()


	# controller.create_top_node("test_1")
	# controller.create_top_node("test_2")
	# controller.create_top_node("test_3")



	# controller.project.tree.print_nodes()
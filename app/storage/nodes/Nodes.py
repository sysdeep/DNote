#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Nodes - объект, контролирующий создание, изменение, получение и удаление нод
"""
import uuid
import os
import shutil

from app import log

from .Node import Node


NODE_TYPES = ("text", "markdown")


class Nodes(object):
	def __init__(self):
		self.nodes_dir		= "nodes"			# каталог с нодами
		self.project_path 	= ""				# полный путь к каталогу проекта
		self.nodes_path		= ""				# полный путь к каталогу с нодами



	def set_project_path(self, project_path):
		"""установить переменные путей"""
		self.project_path = project_path
		self.nodes_path = os.path.join(self.project_path, self.nodes_dir)




	def get_node(self, uuid):
		"""получить объект заданной ноды(загрузка)"""
		node_path = os.path.join(self.nodes_path, uuid)
		node = Node(uuid, node_path)
		node.load()
		# node.load(node_path)
		return node










	def create_node(self, name, storage=None):
		log.debug("создание новой ноды")

		node_uuid = str(uuid.uuid1())
		node_dir_path = os.path.join(self.nodes_path, node_uuid)
		os.mkdir(node_dir_path)

		node = Node(node_uuid, node_dir_path)
		node.name = name
		node.storage = storage

		node.make()

		return node



	

	def remove_node(self, node_uuid):
		"""удаление всех файлов ноды"""
		log.info("удаление всех файлов ноды: " + node_uuid)
		node_dir_path = os.path.join(self.nodes_path, node_uuid)
		# shutil.rmtree(node_dir_path, ignore_errors=True)
		shutil.rmtree(node_dir_path)





	def update_node(self, uuid):
		pass









if __name__ == '__main__':
	

	controller = Nodes()
	controller.create_node()

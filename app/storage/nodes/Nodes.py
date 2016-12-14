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
		node = Node()
		node.load(node_path)
		return node










	def create_node(self, name):
		# log.debug("создание новой ноды")
		node_uuid = str(uuid.uuid1())
		# log.debug(node_uuid)

		node = Node()
		node.set_uuid(node_uuid)
		node.set_name(name)


		node_dir_path = os.path.join(self.nodes_path, node_uuid)
		node.path = node_dir_path

		# log.debug("создание каталога")
		os.mkdir(node_dir_path)

		# log.debug("создание файлов")
		node.write_meta()
		node.write_page()

		return node_uuid



	

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

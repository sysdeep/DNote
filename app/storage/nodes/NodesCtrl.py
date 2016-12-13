#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	NodesCtrl - объект, контролирующий создание, изменение, получение и удаление нод
"""
import uuid
import os

from app import log
from app.rc import DIR_PROJECT_NODES

from .Node import Node





class NodesCtrl(object):
	def __init__(self):
		self.nodes_path = DIR_PROJECT_NODES


	def create_node(self, name):
		# log.debug("создание новой ноды")
		node_uuid = str(uuid.uuid1())
		log.debug(node_uuid)

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



	def get_node(self, node_path):
		node = Node()
		node.load(node_path)
		return node

	def remove_node(self, uuid):
		pass

	def update_node(self, uuid):
		pass









if __name__ == '__main__':
	

	controller = NodesCtrl()
	controller.create_node()

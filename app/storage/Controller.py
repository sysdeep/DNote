#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Controller - объект, контролирующий создание, изменение, получение и удаление нод
"""
import uuid
import os

from app import log
from app.rc import DIR_PROJECT_NODES

from .nodes.Node import Node





class Controller(object):
	def __init__(self):
		self.nodes_path = DIR_PROJECT_NODES


	def create_node(self):
		node_uuid = str(uuid.uuid1())
		print(node_uuid)

		node = Node()
		node.set_uuid(node_uuid)


		node_dir_path = os.path.join(self.nodes_path, node_uuid)
		node.path = node_dir_path

		os.mkdir(node_dir_path)

		node.write_meta()
		node.write_page() 



	def get_node(self, uuid):
		pass

	def remove_node(self, uuid):
		pass

	def update_node(self, uuid):
		pass









if __name__ == '__main__':
	

	controller = Controller()
	controller.create_node()

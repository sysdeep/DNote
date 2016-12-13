#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Controller - объект, управляющий нодами и деревом проекта
"""
import uuid
import os

from app import log
from app.rc import DIR_PROJECT_NODES, DIR_PROJECT

from .nodes.NodesCtrl import NodesCtrl
from .project.Project import Project





class Controller(object):
	def __init__(self):
		self.nodes_ctrl = NodesCtrl()
		self.project	= Project()

		self.project_path = ""



	def load_project_default(self):
		self.load_project(DIR_PROJECT)


	def load_project(self, project_path):
		self.project_path = project_path
		self.project.set_project_dir(self.project_path)
		self.project.load()




	def create_node(self, name):
		log.debug("создание новой ноды")


	def create_top_node(self, name):
		log.debug("создание новой ноды - top")

		self.nodes_ctrl.create_node(name)

		self.project.create_node_top(name)
		self.project.write_file()












if __name__ == '__main__':
	

	controller = Controller()
	controller.load_project_default()
	# controller.create_node()

	controller.project.tree.print_nodes()


	# controller.create_top_node("test_1")
	# controller.create_top_node("test_2")
	# controller.create_top_node("test_3")



	# controller.project.tree.print_nodes()

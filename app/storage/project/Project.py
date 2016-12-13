#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Project - класс описывающий всё дерево проекта

	оперирует данными из заданного каталога след. структуры:

		nodes		- каталог со всеми нодами
		trash		- каталог с удалёнными нодами
		project.json	- файл, описывающий дерево каталогов

"""
import os
import json

from app import log
from app.rc import FILE_PROJECT

from .NSTree import NSTree



class Project(object):
	def __init__(self):
		self.file_name = "project.json"
		self.path = ""

		self.name = ""
		self.tree = NSTree()



	def set_project_dir(self, project_path):
		self.path = os.path.join(project_path, self.file_name)


	def load(self):
		log.debug("загрузка проекта")

		with open(self.path, "r", encoding="utf-8") as fd:
			data_json = fd.read()

		data = json.loads(data_json)
		self.name = data["name"]

		self.tree.load(data["tree"])



	def create_node_top(self, uuid, name):
		root_node = self.tree.root
		node = self.tree.create_node(root_node)
		node.uuid = uuid
		node.name = name





	def write_file(self):
		log.debug("write project: " + self.path)

		tree_data = self.tree.export()

		data = {
			"name"		: self.name,
			"tree"		: tree_data
		}

		data_json = json.dumps(data, indent=4)

		with open(self.path, "w", encoding="utf-8") as fd:
			data = fd.write(data_json)





	def __repr__(self):
		return "{}".format(self.name)




	

if __name__ == '__main__':
	
	from app.rc import DIR_PROJECT

	project = Project()
	project.set_project_dir(DIR_PROJECT)
	project.load()

	print(project)


	project.tree.print_nodes()



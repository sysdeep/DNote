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
		self.file_name 		= "project.json"			# название файла проекта
		self.file_path 		= ""						# полный путь к файлу проекта
		self.project_path	= ""						# полный путь к каталогу проекта

		#--- данные проекта
		self.name 			= ""						# название проекта
		self.tree 			= NSTree()					# дерево проекта



	# def set_project_dir(self, project_path):
	# 	self.file_path = os.path.join(project_path, self.file_name)


	def load(self, project_path):
		"""загрузка данных проекта по указанному пути"""
		self.project_path = project_path
		log.debug("загрузка проекта: " + self.project_path)
		self.file_path = os.path.join(self.project_path, self.file_name)

		with open(self.file_path, "r", encoding="utf-8") as fd:
			data_json = fd.read()

		data = json.loads(data_json)



		self.name = data["name"]

		self.tree.load(data["tree"])


	def get_tree(self):
		return self.tree


	def get_root_node(self):
		return self.tree.root

	def find_node_by_uuid(self, uuid):
		return self.tree.find_node_by_uuid(uuid)


	def create_node(self, parent_node, uuid, name):
		node = self.tree.create_node(parent_node)
		node.uuid = uuid
		node.name = name




	def create_node_top(self, uuid, name):
		root_node = self.tree.root
		node = self.tree.create_node(root_node)
		node.uuid = uuid
		node.name = name





	def write_file(self):
		log.debug("write project: " + self.file_path)

		tree_data = self.tree.export()

		data = {
			"name"		: self.name,
			"tree"		: tree_data
		}

		data_json = json.dumps(data, indent=4)

		with open(self.file_path, "w", encoding="utf-8") as fd:
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



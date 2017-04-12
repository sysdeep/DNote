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

from .NSTree import NSTree

from .. import sevents


class Project(object):
	"""объект проекта - содержит дерево"""
	def __init__(self):
		self.file_name 		= "project.json"			# название файла проекта
		self.file_path 		= ""						# полный путь к файлу проекта
		self.project_path	= ""						# полный путь к каталогу проекта

		#--- данные проекта
		self.name 			= ""						# название проекта
		self.tree 			= NSTree()					# дерево проекта




	def load(self, project_path):
		"""загрузка данных проекта по указанному пути"""
		self.project_path = project_path
		log.debug("загрузка проекта: " + self.project_path)
		self.file_path = os.path.join(self.project_path, self.file_name)

		with open(self.file_path, "r", encoding="utf-8") as fd:
			data_json = fd.read()

		data = json.loads(data_json)

		#--- set data
		self.name = data["name"]
		self.tree.load(data["tree"])


		sevents.project_loaded()




	def create(self, name, path):
		log.debug("создание проекта")
		self.project_path 	= path
		self.name 			= name
		self.file_path 		= os.path.join(self.project_path, self.file_name)

		


	def get_tree(self):
		return self.tree


	def get_root_node(self):
		return self.tree.root




	def get_node(self, uuid):
		return self.tree.get_node(uuid)




	def find_parent_node(self, uuid):
		return self.tree.find_parent_node(uuid)



	def create_node(self, parent_node, uuid, name):
		"""создание нового узла"""
		node = self.tree.create_node(parent_node.uuid, uuid, name)

		#--- установка флага текущего
		self.set_current_flag(uuid)
		sevents.project_node_created()


	def remove_node(self, node_uuid):
		"""удаление ноды"""
		log.info("удаление ноды: " + node_uuid)
		self.tree.remove_node(node_uuid)
		sevents.project_node_removed()



	def set_node_expanded(self, node_uuid, status):
		"""установка состояния раскрытия заданной ноды"""
		node = self.tree.get_node(node_uuid)
		node.expanded = status



	def set_node_name(self, node_uuid, name):
		"""установить новое название ноды"""
		# node = self.get_node(node_uuid)
		node = self.tree.get_node(node_uuid)
		node.name = name


	def set_current_flag(self, node_uuid):
		"""
			установить флаг текущей ноды - у других сбросить
			вызывается при выборе ноды в дереве
		"""
		log.debug("set_current_flag: " + node_uuid)

		for node in self.tree.nodes:
			if node.uuid == node_uuid:
				node.current = True
			else:
				node.current = False

		

	#--- moves ----------------------------------------------------------------
	def move_node_up(self, node_uuid):
		log.debug("move_node_up: " + node_uuid)
		return self.tree.move_node_up(node_uuid)

	def move_node_down(self, node_uuid):
		log.debug("move_node_down: " + node_uuid)
		return self.tree.move_node_down(node_uuid)
	#--- moves ----------------------------------------------------------------




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

		sevents.project_updated()











	

	def __repr__(self):
		return "{}".format(self.name)




	










	

if __name__ == '__main__':
	
	from app.rc import DIR_PROJECT

	project = Project()
	project.set_project_dir(DIR_PROJECT)
	project.load()

	print(project)


	project.tree.print_nodes()



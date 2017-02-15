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
from app.lib import EventEmitter


class Project(object):
	def __init__(self):
		self.file_name 		= "project.json"			# название файла проекта
		self.file_path 		= ""						# полный путь к файлу проекта
		self.project_path	= ""						# полный путь к каталогу проекта

		#--- данные проекта
		self.name 			= ""						# название проекта
		self.tree 			= NSTree()					# дерево проекта

		self.__emitter		= EventEmitter()


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
		self.emit("loaded")



	def get_tree(self):
		return self.tree


	def get_root_node(self):
		return self.tree.root

	def find_node_by_uuid(self, uuid):
		return self.tree.find_node_by_uuid(uuid)

	def find_parent_node(self, uuid):
		return self.tree.find_parent_node(uuid)



	def set_current_node(self, uuid):
		"""установить флаг текущей ноды - у других сбросить"""
		for node in self.tree.nodes:
			if node.uuid == uuid:
				node.current = True
			else:
				node.current = False


	def create_node(self, parent_node, uuid, name):
		node = self.tree.create_node(parent_node)
		node.uuid = uuid
		node.name = name

		self.set_current_node(uuid)
		self.emit("node_created")


	def remove_node(self, node_uuid):
		"""удаление ноды"""
		log.info("удаление ноды: " + node_uuid)
		self.tree.remove_node(node_uuid)
		self.emit("node_removed")



	def set_node_expanded(self, node_uuid, status):
		"""установка состояния раскрытия заданной ноды"""
		node = self.find_node_by_uuid(node_uuid)
		node.expanded = status



	def set_node_name(self, node_uuid, name):
		"""установить новое название ноды"""
		node = self.find_node_by_uuid(node_uuid)
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

		self.emit("updated")


	#--- events ---------------------------------------------------------------
	def eon(self, event_name, cb):
		"""подписаться на события"""
		self.__emitter.eon(event_name, cb)

	def eoff(self, event_name, cb):
		self.__emitter.eoff(event_name, cb)

	def emit(self, event, *args, **kwargs):
		self.__emitter.emit(event, *args, **kwargs)
	#--- events ---------------------------------------------------------------



	def __repr__(self):
		return "{}".format(self.name)




	

if __name__ == '__main__':
	
	from app.rc import DIR_PROJECT

	project = Project()
	project.set_project_dir(DIR_PROJECT)
	project.load()

	print(project)


	project.tree.print_nodes()



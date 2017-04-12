#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Node - объект, описывающий структуру ноды документа

	физически документ хранится в каталоге, название каталога - uuid1
	все ноды хранятся в виде линейного списка в одном каталоге

	каталог ноды содержит:
		__meta.json			- описание ноды
		__page.page			- содержимое текстовых данных ноды

		# __icon.png
"""

# from .Meta import Meta
from .Page import Page
from .Files import Files

from .. import sevents









class Node(object):
	def __init__(self, uuid, node_path):
		self.path = node_path
		self.uuid = uuid

		self.page = Page(self.path)
		self.files = Files(self.path)



	def make(self, content=""):
		"""создание компонентов ноды при создании ноды"""
		self.page.raw_text = content
		self.page.write_file()


	#


	#
	#
	# def write_node(self):
	# 	"""???"""
	# 	self.write_meta()
	# 	self.write_page()
	#
	#
	#
	#
	#
	# def write_meta(self):
	# 	"""???"""
	# 	self.meta.write_file()
	#
	# def write_page(self):
	# 	"""???"""
	# 	self.page.write_file()
	#
	#
	#
	#
	def update_page_text(self, text):
		"""записать данные в страницу"""
		self.page.raw_text = text
		self.page.write_file()
		# self.__event_updated()


	#
	#
	# def update_node_name(self, name):
	# 	"""обновление названия ноды"""
	# 	self.name = name
	# 	self.meta.name = name
	# 	self.meta.write_file()
	# 	self.__event_updated()
	#
	#
	#
	#
	# def __event_updated(self):
	# 	sevents.node_updated()
		# if self.storage:
		# 	self.storage.emit("node_updated")
	#
	#
	#
	# #--- separates
	#
	def create_file(self, src_file_path):
		"""создание файла"""
		#--- создание
		self.files.create_file(src_file_path)

		# #--- обновление метаданных
		# self.meta.write_file()
		# self.__event_updated()


	def remove_file(self, file_name):
		"""удаление заданного файла"""
		#--- удаление
		self.files.remove_file(file_name)

		# #--- обновление метаданных
		# self.meta.write_file()
		# self.__event_updated()







	def __repr__(self):
		return "{} - {}".format(self.meta.uuid, self.meta.name)

















if __name__ == '__main__':
	from app.rc import DIR_TEST_NODE

	node = Node()
	node.load(DIR_TEST_NODE)

	print(node)
	print(node.page.raw_text)
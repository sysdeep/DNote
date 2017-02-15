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

from .Meta import Meta
from .Page import Page
from .Files import Files











class Node(object):
	def __init__(self, uuid, node_path):
		self.path = node_path
		self.uuid = uuid
		self.name = ""

		self.meta = Meta(self.path)
		self.page = Page(self.path)
		self.files = Files(self.path)

		# self.meta.load(self.path)			# meta
		# self.page.load(self.path)			# page
		# self.files.load(self.path)

		#--- update self vars
		# self.name = self.meta.name

	def load(self):
		"""загрузка компонентов ноды"""
		self.meta.load()			# meta
		self.page.load()			# page
		self.files.load()			# files

		#--- update self vars
		self.name = self.meta.name


	def make(self):
		"""создание компонентов ноды при создании ноды"""
		self.meta.name = self.name
		self.meta.uuid = self.uuid
		self.write_meta()
		self.write_page()
		


	# def set_name(self, name):
	# 	self.name = name
	# 	# self.meta.name = name








	def write_node(self):
		"""???"""
		self.write_meta()
		self.write_page()

	



	def write_meta(self):
		"""???"""
		self.meta.write_file()

	def write_page(self):
		"""???"""
		self.page.write_file()

	
	
	# def create_files(self):
	# 	self.files.create_files(self.path)


	#--- separates

	def create_file(self, src_file_path):
		"""создание файла"""
		#--- создание
		self.files.create_file(src_file_path)

		#--- обновление метаданных
		self.meta.write_file()


	def remove_file(self, file_name):
		"""удаление заданного файла"""
		#--- удаление
		self.files.remove_file(file_name)

		#--- обновление метаданных
		self.meta.write_file()







	def __repr__(self):
		return "{} - {}".format(self.meta.uuid, self.meta.name)

















if __name__ == '__main__':
	from app.rc import DIR_TEST_NODE

	node = Node()
	node.load(DIR_TEST_NODE)

	print(node)
	print(node.page.raw_text)
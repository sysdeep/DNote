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
	def __init__(self):
		self.path = ""
		self.uuid = ""
		self.name = ""

		self.meta = Meta()
		self.page = Page()
		self.files = Files()


	def load(self, node_path):
		"""загрузка данных"""
		self.path = node_path
		self.meta.load(self.path)			# meta
		self.page.load(self.path)			# page
		self.files.load(self.path)

		#--- update self vars
		self.name = self.meta.name
		self.uuid = self.meta.uuid




	def set_uuid(self, uuid):
		self.uuid = uuid
		self.meta.uuid = uuid

	def set_name(self, name):
		self.name = name
		self.meta.name = name

	def write_node(self):
		self.write_meta()
		self.write_page()

	



	def write_meta(self):
		self.meta.write_file(self.path)

	def write_page(self):
		self.page.write_file(self.path)

	def create_files(self):
		self.files.create_files(self.path)



	def __repr__(self):
		return "{} - {}".format(self.meta.uuid, self.meta.name)

















if __name__ == '__main__':
	from app.rc import DIR_TEST_NODE

	node = Node()
	node.load(DIR_TEST_NODE)

	print(node)
	print(node.page.raw_text)
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












class Node(object):
	def __init__(self):
		self.path = ""
		self.uuid = ""
		self.meta = Meta()
		self.page = Page()

	def load(self, node_path):
		self.path = node_path
		self.meta.load(self.path)
		self.page.load(self.path)




	def set_uuid(self, uuid):
		self.meta.uuid = uuid



	def write_meta(self):
		self.meta.write_file(self.path)

	def write_page(self):
		self.page.write_file(self.path)


	def __repr__(self):
		return "{} - {}".format(self.meta.uuid, self.meta.name)

















if __name__ == '__main__':
	from app.rc import DIR_TEST_NODE

	node = Node()
	node.load(DIR_TEST_NODE)

	print(node)
	print(node.page.raw_text)
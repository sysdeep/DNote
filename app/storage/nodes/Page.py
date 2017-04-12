#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Page - объект текстовых данных
"""
import json
import os.path
from app import log




class Page(object):
	def __init__(self, node_path):
		self.file 	= "__page.page"		# файл
		self.node_path = node_path
		self.path = os.path.join(self.node_path, self.file) 
		self.raw_text 	= ""

		self.load()


	def load(self):
		"""загрузка данных из файла"""

		if not os.path.exists(self.path):
			self.write_file()
			return False

		self.read_file()


	def read_file(self):
		with open(self.path, "r", encoding="utf-8") as fd:
			self.raw_text = fd.read()





	def write_file(self):

		with open(self.path, "w", encoding="utf-8") as fd:
			fd.write(self.raw_text)



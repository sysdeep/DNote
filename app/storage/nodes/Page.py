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

		# self.load()


	def load(self):
		"""загрузка данных из файла"""
		# self.path = os.path.join(node_path, self.file) 
		# log.debug("загрузка данных из файла: " + self.path)
		with open(self.path, "r", encoding="utf-8") as fd:
			self.raw_text = fd.read()

		

	def write_file(self):
		# self.path = os.path.join(node_path, self.file)
		# log.debug("write page: " + self.path)


		
		with open(self.path, "w", encoding="utf-8") as fd:
			data = fd.write(self.raw_text)

	# def __repr__(self):
	# 	return "{} - {}".format(self.uuid, self.name)


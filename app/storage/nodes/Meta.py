#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Meta - объект метаданных
"""
import json
import os.path
import time

from app import log

class Meta(object):
	def __init__(self, node_path):
		self.meta_file 	= "__meta.json"		# файл метаданных
		self.node_path = node_path
		self.path = os.path.join(self.node_path, self.meta_file) 
		# self.path	= ""

		self.ntype	= "text"			# тип ноды
		self.uuid	= ""				# uuid ноды
		self.name	= ""				# название ноды
		self.ctime	= 0					# время создания
		self.mtime	= 0					# время модификации
		self.atime	= 0					# время последнего доступа(?)
		self.tags	= []				# список тэгов

		# self.load()


	# def load(self, node_path):
	def load(self):
		"""загрузка данных из файла"""


		# if not os.path.exists(self.path):
		# 	self.write_file()
		# self.path = os.path.join(node_path, self.meta_file) 
		# log.debug("загрузка данных из файла: " + self.path)
		with open(self.path, "r", encoding="utf-8") as fd:
			data = fd.read()

		data_json = json.loads(data)

		self.ntype = data_json["ntype"]
		self.uuid = data_json["uuid"]
		self.name = data_json["name"]
		self.ctime = data_json["ctime"]
		self.mtime = data_json["mtime"]
		# self.atime = data_json["atime"]
		self.tags = data_json["tags"]




	def write_file(self):
		# self.path = os.path.join(node_path, self.meta_file)
		# log.debug("write meta: " + self.path)

		now_seconds = time.time()
		if self.ctime == 0:
			self.ctime = now_seconds

		self.mtime = now_seconds

		data = {
			"ntype"		: self.ntype,
			"uuid"		: self.uuid,
			"name"		: self.name,
			"ctime"		: self.ctime,
			"mtime"		: self.mtime,
			"atime"		: self.atime,
			"tags"		: self.tags
		}

		data_json = json.dumps(data, indent=4)

		with open(self.path, "w", encoding="utf-8") as fd:
			data = fd.write(data_json)


	def get_date(self, seconds):
		"""получить дату в читаемом виде"""
		time_tuple = time.localtime(seconds)
		result = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
		return result

	def get_ctime(self):
		return self.get_date(self.ctime)

	def get_mtime(self):
		return self.get_date(self.mtime)



	def __repr__(self):
		return "{} - {}".format(self.uuid, self.name)




if __name__ == '__main__':
	
	import os
	from app.rc import DIR_TEST_NODE


	meta = Meta()
	meta.load(DIR_TEST_NODE)

	print(meta)
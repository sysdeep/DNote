#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Files - объект с каталогом файлов
"""
import json
import os
import time
import shutil

from app import log





class Files(object):
	def __init__(self, node_path):
		self.dir_name 	= "__files"			# каталог для файлов
		# self.path		= ""				# полный путь до каталога с файлами
		self.files 		= []				# список файлов в каталоге
		self.path 		= os.path.join(node_path, self.dir_name)		# полный путь до каталога с файлами

		# self.load()



	def load(self):
		"""первоначальная загрузка объекта"""
		# #--- создаём путь до файлов
		# self.path = os.path.join(node_path, self.dir_name)

		#--- если каталога с файлами нет - создаём
		if not os.path.exists(self.path):
			os.mkdir(self.path)

		#--- читаем список файлов
		self.__read_files()



	def __read_files(self):
		"""читаем список файлов"""
		self.files = os.listdir(self.path)
	


	def create_file(self, src_file_path):
		"""создание файла"""
		#--- имя файла
		file_name = os.path.basename(src_file_path)

		#--- полный путь к результатирующему файлу
		dest_file_path = os.path.join(self.path, file_name)

		#--- копируем
		shutil.copyfile(src_file_path, dest_file_path)

		#--- обновляем список
		self.__read_files()



	def remove_file(self, file_name):
		"""удаление файла"""

		#--- полный путь удаляемого файла
		file_path = os.path.join(self.path, file_name)

		#--- если файл присутствует - удаляем
		if os.path.exists(file_path):
			os.unlink(file_path)
		else:
			log.error("file not exists: {}".format(file_path))
		
		#--- обновляем список
		self.__read_files()


	
	# def create_files(self, node_path):
	# 	self.path = os.path.join(node_path, self.dir_name)
	# 	os.mkdir(self.path)



if __name__ == '__main__':
	
	import os
	from app.rc import DIR_TEST_NODE


	meta = Meta()
	meta.load(DIR_TEST_NODE)

	print(meta)
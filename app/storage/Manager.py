#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
from app import log
from app.rc import DIR_DEFAULTS
from .Storage import Storage
from . import sevents


class Manager(object):
	def __init__(self):

		self.storage = None
		self.storage_path = None

		# self.__event_emitter = EventEmitter()



	def get_storage(self):
		return self.storage

	def open_storage(self, path):
		log.debug("SManager - open storage")
		self.storage_path = path
		self.storage = Storage(self.storage_path)
		# self.storage.open()
		sevents.storage_opened()




	def create_storage(self, name, path):
		log.info("SManager - create new store: {} in {}".format(name, path))
		# self.storage_path = path

		# sevents.storage_created()

		new_storage_path = os.path.join(path, name)

		DIR_DEFAULT_STORAGE_1 = os.path.join(DIR_DEFAULTS, "sdir1")


		shutil.copytree(DIR_DEFAULT_STORAGE_1, new_storage_path)

		self.open_storage(new_storage_path)


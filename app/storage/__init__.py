#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
	2018.08.11 - новая реализация хранилища - singleton
"""
import os.path
import shutil
# from app.rc import DIR_PROJECT
from .Manager import Manager
from .Storage import Storage
from .nodes.Nodes import NODE_TYPES

from app.rc import DIR_DEFAULTS



storage = Storage()


#
#
# from .loader import get_storage, load_default_project, open_storage
#
#
#
# smanager = Manager()
# # smanager.open_storage(DIR_PROJECT)
#
#
# # set_up()




def create_storage(name, path):
	"""
		Создать новое хранилище
	"""
	# log.info("SManager - create new store: {} in {}".format(name, path))
	# self.storage_path = path

	# sevents.storage_created()

	new_storage_path = os.path.join(path, name)

	DIR_DEFAULT_STORAGE_1 = os.path.join(DIR_DEFAULTS, "sdir1")


	shutil.copytree(DIR_DEFAULT_STORAGE_1, new_storage_path)

	# self.open_storage(new_storage_path)
	storage.close_storage()
	storage.open_storage(new_storage_path)
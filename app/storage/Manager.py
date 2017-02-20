#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .Storage import Storage



class Manager(object):
	def __init__(self):

		self.storage = None
		self.storage_path = None

	def get_storage(self):
		return self.storage

	def open_storage(self, path):
		self.storage_path = path
		self.storage = Storage(self.storage_path)

	def create_storage(self, name, path):
		self.storage_path = path
#!/usr/bin/env python3
# -*- coding: utf-8 -*-




class Node(object):
	def __init__(self):

		# self.tree_lk 	= 0
		# self.tree_rk 	= 0
		# self.tree_level = 0

		self.name 		= ""			# название ноды
		self.uuid		= ""			# id
		self.expanded	= False			# открыта нода или нет
		self.current	= False			# флаг текущей ноды
		self.icon		= ""			# название иконки
		self.ipack		= ""			# название пака иконки

		self.childrens = []

	def export(self):
		data = {
			"name"			: self.name,
			"uuid"			: self.uuid,
			"expanded"		: self.expanded,
			"current"		: self.current,
			"icon"			: self.icon,
			"ipack"			: self.ipack,
			"childrens"		: self.childrens
		}

		return data



	def load(self, data):
		self.name 		= data["name"]
		self.uuid 		= data["uuid"]
		self.expanded	= data["expanded"]
		self.current	= data["current"]
		self.icon		= data["icon"]
		self.ipack		= data["ipack"]
		self.childrens 	= data["childrens"]






	def __repr__(self):
		return "{}".format(self.name)
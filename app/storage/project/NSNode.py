#!/usr/bin/env python3
# -*- coding: utf-8 -*-




class NSNode(object):
	def __init__(self):

		self.tree_lk 	= 0
		self.tree_rk 	= 0
		self.tree_level = 0

		self.name 		= ""			# название ноды
		self.uuid		= ""			# id
		self.expanded	= False			# открыта нода или нет
		self.current	= False			# флаг текущей ноды 
		self.icon		= ""			# название иконки
		self.ipack		= ""			# название пака иконки


		#--- from meta
		self.ntype	= "text"			# тип ноды
		self.ctime	= 0					# время создания
		self.mtime	= 0					# время модификации
		self.atime	= 0					# время последнего доступа(?)
		self.tags	= []				# список тэгов




	def export(self):
		data = {
			"tree_lk" 		: self.tree_lk,
			"tree_rk"		: self.tree_rk,
			"tree_level"	: self.tree_level,
			"name"			: self.name,
			"uuid"			: self.uuid,
			"expanded"		: self.expanded,
			"current"		: self.current,
			"icon"			: self.icon,
			"ipack"			: self.ipack,

			"ntype"			: self.ntype
		}

		return data



	def load(self, data):
		self.tree_lk 	= data["tree_lk"]
		self.tree_rk 	= data["tree_rk"]
		self.tree_level = data["tree_level"]
		self.name 		= data["name"]
		self.uuid 		= data["uuid"]
		self.expanded	= data["expanded"]
		self.current	= data.get("current", False)
		self.icon		= data.get("icon", "")
		self.ipack		= data.get("ipack", "")


		self.ntype		= data.get("ntype", "text")





	def __repr__(self):
		return "{} - lk: {}, rk: {}, uuid: {}".format(self.name, self.tree_lk, self.tree_rk, self.uuid)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-




class NSNode(object):
	def __init__(self):
		self.tree_lk 	= 0
		self.tree_rk 	= 0
		self.tree_level = 0
		self.name 		= ""
		
		

	def export(self):
		data = {
			"tree_lk" 		: self.tree_lk,
			"tree_rk"		: self.tree_rk,
			"tree_level"	: self.tree_level,
			"name"			: self.name
		}

		return data



	def load(self, data):
		self.tree_lk 	= data["tree_lk"]
		self.tree_rk 	= data["tree_rk"]
		self.tree_level = data["tree_level"]
		self.name 		= data["name"]

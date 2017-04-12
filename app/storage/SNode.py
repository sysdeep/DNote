#!/usr/bin/env python3
# -*- coding: utf-8 -*-






class SNode(object):
	def __init__(self, node_data, node_project, project):
		self.node_data = node_data
		self.node_project = node_project
		self.project = project




	def save(self):
		self.node_data.write_node()
		self.project.write_file()




	@property
	def name(self):
		return self.node_data.meta.name

	@name.setter
	def name(self, name):
		self.node_data.meta.name = name
		self.node_project.name = name

	@property
	def uuid(self):
		return self.node_data.uuid

	@uuid.setter
	def uuid(self, uuid):
		self.node_data.uuid = uuid
		self.node_project.uuid = uuid


	@property
	def ntype(self):
		return self.node_data.meta.ntype

	@ntype.setter
	def ntype(self, ntype):
		self.node_data.meta.ntype = ntype
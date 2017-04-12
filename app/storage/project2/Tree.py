#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .Node import Node


class Tree(object):
	def __init__(self):
		self.nodes = {}



	def load(self, nodes):

		for ndata in nodes:
			node = Node()
			node.load(ndata)
			self.nodes[node.uuid] = node


	def create(self, parent_uuid, node_uuid, name):
		node = Node()
		node.name = name
		node.uuid = node_uuid
		self.nodes[node_uuid] = node

		parent_node = self.nodes[parent_uuid]
		parent_node.childrens.append(node_uuid)



	# def insert(self):







if __name__ == "__main__":

	import json

	FILE_DATA = "/home/nia/Development/_Python/_DNote/pro.json"

	tree = Tree()



	with open(FILE_DATA, "r", encoding="utf-8") as fd:
		data_json = fd.read()

	data = json.loads(data_json)

	tree.load(data["tree"])

	print(tree.nodes)


	print("---------------------------------")
	tree.create("0", "1", "1")
	print(tree.nodes)
	print("---------------------------------")


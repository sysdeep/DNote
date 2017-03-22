#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import log

from .NSNode import NSNode


class NSTree(object):
	"""nested tree object"""
	def __init__(self):
		self.nodes = []			# список нод
		self.root = None		# основная нода

		#--- инициализируем пустое дерево
		self.__set_new()


	def __set_new(self):
		"""инициализация пустого дерева"""
		root_node 				= NSNode()
		root_node.tree_lk 		= 0
		root_node.tree_rk 		= 1
		root_node.tree_level 	= 0
		root_node.name 			= "root"

		self.nodes = [root_node]
		self.root = root_node




	#--- public ---------------------------------------------------------------
	def load(self, nodes_list):
		"""загрузка данных в дерево"""
		self.nodes = []
		nodes_list.sort(key=lambda a: a["tree_lk"])

		for node_data in nodes_list:
			node = NSNode()
			node.load(node_data)
			self.nodes.append(node)

			#--- ссылка на корень
			if node_data["tree_lk"] == 0:
				self.root = node

	def create_node(self, parent_node):
		"""создание новой ноды от родителя"""
		log.debug("создание новой ноды для родителя: " + parent_node.uuid)
		new_node = NSNode()
		self.__insert(parent_node, new_node)
		return new_node

	# def create_node_file(self, parent_node, new_node_name):
	# 	new_node = NodeFile()
	# 	new_node.name = new_node_name
	# 	self.insert(parent_node, new_node)
	# 	return new_node



	def remove_node(self, node_uuid):
		"""удаление заданной ноды из дерева"""
		log.debug("удаление заданной ноды из дерева: " + node_uuid)
		node = self.find_node_by_uuid(node_uuid)

		if node:
			self.__remove(node)


	def find_node_by_uuid(self, uuid):
		fnode = None
		for node in self.nodes:
			if node.uuid == uuid:
				fnode = node
				break

		if fnode is None:
			log.error("not found node: " + uuid)

		return fnode
	#--- public ---------------------------------------------------------------


	# def set_nodes(self, nodes_list):
	# 	self.nodes = []
	# 	nodes_list.sort(key=lambda a: a["tree_lk"])

	# 	for node_data in nodes_list:
	# 		if node_data["ntype"] == "f":
	# 			node = NodeFile()

	# 		elif node_data["ntype"] == "d":
	# 			node = NodeDir()
	# 		else:
	# 			log.error("set_nodes - неизвестный тип ноды: {}".format(node_data["ntype"]))
	# 			node = None


	# 		if node:
	# 			node.load(node_data)
	# 			self.nodes.append(node)




		# self.nodes = sorted(nodes_list, key=lambda a: a["tree_lk"])
		# self.nodes = nodes_list



	def __insert(self, parent_node, new_node):
		"""добавление новой ноды к родительской ветви"""
		
		parent_rk = parent_node.tree_rk
		parent_lk = parent_node.tree_lk

		#--- 1 - update after
		for node in self.nodes:
			if node.tree_lk > parent_rk:
				node.tree_lk += 2
				node.tree_rk += 2

		#--- 2 - update parent
		for node in self.nodes:
			if node.tree_rk >= parent_rk and node.tree_lk < parent_rk:
				node.tree_rk += 2

		#--- 3 - add node
		new_node.tree_level = parent_node.tree_level + 1
		new_node.tree_lk = parent_rk
		new_node.tree_rk = parent_rk + 1


		self.nodes.append(new_node)
		
	


	def __remove(self, node):
		"""удаление заданной ноды(со всеми потомками)"""

		node_lk = node.tree_lk
		node_rk = node.tree_rk

		#--- 1 - find del nodes
		del_nodes = [n for n in self.nodes if n.tree_lk >= node_lk and n.tree_rk <= node_rk]
		# print(del_nodes)

		#--- 2 - remove nodes from list
		for n in del_nodes:
			self.nodes.remove(n)

		#--- 3 - update nodes before
		for n in self.nodes:
			if n.tree_rk > node_rk and n.tree_lk < node_lk:
				n.tree_rk -= (node_rk - node_lk + 1) 
		
		
		#--- 4 - update nodes after
		for n in self.nodes:
			if n.tree_lk > node_rk:
				n.tree_lk -= (node_rk - node_lk + 1)
				n.tree_rk -= (node_rk - node_lk + 1)
		





		






	def find_parent_node(self, node_uuid):
		"""поиск родителя заданной ноды"""
		snode = self.find_node_by_uuid(node_uuid)

		result = [node for node in self.nodes
					if node.tree_lk < snode.tree_lk 
					and node.tree_rk > snode.tree_rk
					and node.tree_level == snode.tree_level - 1
				]

		if result:
			return result[0]
		else:
			log.error("not found parent for node: " + node_uuid)
			return None






	# def get_node_tree_path(self, path_array):
	# 	# print("----------------------")
	# 	pa = path_array[1:]
	# 	node = self.root
	# 	# print(pa)



	# 	for path_item in pa:
	# 		childrens = self.get_childrens(node)

	# 		nodes = [node for node in childrens if node.name == path_item]

	# 		# print(nodes)
	# 		# print(nodes)
	# 		if len(nodes) > 0:
	# 			node = nodes[0]

	# 	# print("----------------------")
	# 	return node




	# def move_node_up(self, node_uuid):
	# 	pass



	# def __find_ne_nodes(self, snode):
	# 	"""поиск соседей"""

	# 	nodel = [node for node in self.nodes
	# 			if node.tree_level == snode.tree_level
	# 			and
	# 	]


	def get_childrens(self, parent_node):
		childrens = [node for node in self.nodes 
				if node.tree_lk > parent_node.tree_lk 
				and node.tree_rk < parent_node.tree_rk 
				and node.tree_level - 1 == parent_node.tree_level]
		return childrens

	def get_nodes_level(self, level):
		return [node for node in self.nodes if node.tree_level == level]



	def export(self):
		data = []
		for node in self.nodes:
			row = node.export()
			data.append(row)

		return data



	def set_empty(self):
		self.nodes = []
		self.__set_new()



	
	#--- prints ---------------------------------------------------------------
	def print_nodes(self):
		for node in sorted(self.nodes, key=lambda a: a.tree_lk):
			print(self.__fill_tabs(node.tree_level) + node.name + " - " + str(node.tree_lk) + " - " + str(node.tree_rk))

	def __fill_tabs(self, num):
		return "  "*num
	#--- prints ---------------------------------------------------------------


















if __name__ == '__main__':

	tree = NSTree()

	
	

	tree.print_nodes()


	print("-------------------------")
	node = tree.create_node(tree.root)
	node.name = "first 1"

	node = tree.create_node(node)
	node.name = "first 1.1"



	node = tree.create_node(tree.root)
	node.name = "second"
	# new_node1 = Node()
	# new_node1.name = "new 1"
	# tree.insert(root_node, new_node1)


	# new_node2 = Node()
	# new_node2.name = "new 2"
	# tree.insert(root_node, new_node2)

	# new_node1_1 = Node()
	# new_node1_1.name = "new 1.1"
	# tree.insert(new_node1, new_node1_1)

	tree.print_nodes()


	# ch = tree.get_childrens(root_node)
	# print(ch)


	
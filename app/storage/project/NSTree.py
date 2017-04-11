#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import log

from .NSNode import NSNode


class NSTree(object):
	"""nested tree object"""
	def __init__(self):
		self.nodes 		= []		# список нод
		self.root 		= None		# основная нода
		self.nodes_map 	= {}		# {node_uuid: node}

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
			self.nodes_map[node.uuid] = node

			#--- ссылка на корень
			if node_data["tree_lk"] == 0:
				self.root = node



	def create_node(self, parent_node_uuid):
		"""создание новой ноды от родителя"""
		log.debug("создание новой ноды для родителя: " + parent_node_uuid)
		parent_node = self.nodes_map[parent_node_uuid]
		new_node = NSNode()
		self.__insert(parent_node, new_node)
		return new_node



	def remove_node(self, node_uuid):
		"""удаление заданной ноды из дерева"""
		log.debug("удаление заданной ноды из дерева: " + node_uuid)
		node = self.get_node(node_uuid)

		if node:
			return self.__remove(node)
		else:
			return False


	def get_node(self, node_uuid):

		node = self.nodes_map.get(node_uuid)
		if node is None:
			log.error("get_node - no node found with uuid: " + node_uuid)

		return node


	# def find_node_by_uuid(self, uuid):
	# 	fnode = None
	# 	for node in self.nodes:
	# 		if node.uuid == uuid:
	# 			fnode = node
	# 			break
	#
	# 	if fnode is None:
	# 		log.error("not found node: " + uuid)
	#
	# 	return fnode
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
		self.nodes_map[new_node.uuid] = new_node
		
	


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
			del(self.nodes_map[n.uuid])

		#--- 3 - update nodes before
		for n in self.nodes:
			if n.tree_rk > node_rk and n.tree_lk < node_lk:
				n.tree_rk -= (node_rk - node_lk + 1) 
		
		
		#--- 4 - update nodes after
		for n in self.nodes:
			if n.tree_lk > node_rk:
				n.tree_lk -= (node_rk - node_lk + 1)
				n.tree_rk -= (node_rk - node_lk + 1)
		





		





	#--- tree finds -----------------------------------------------------------
	def find_parent_node(self, node_uuid):
		"""поиск родителя заданной ноды"""
		snode = self.get_node(node_uuid)
		if snode is None:
			return None

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



	def find_childrens(self, node_uuid):
		"""поиск детёнышей заданной ноды след. уровня"""
		parent_node = self.get_node(node_uuid)
		if parent_node is None:
			return []

		childrens = [node for node in self.nodes
				if node.tree_lk > parent_node.tree_lk
				and node.tree_rk < parent_node.tree_rk
				and node.tree_level - 1 == parent_node.tree_level]

		childrens.sort(key=lambda row: row.tree_lk)
		return childrens





	def find_parent_branch(self, node_uuid):
		"""получить полный путь от корня до заданной ноды(включая)"""
		snode = self.get_node(node_uuid)
		if snode is None:
			return []


		nodes = [node for node in self.nodes
				 if node.tree_lk <= snode.tree_lk
				 and node.tree_rk >= snode.tree_rk]

		nodes.sort(key=lambda row: row.tree_lk)
		return nodes




	def find_branch(self, node_uuid):
		"""получить полную ветку нод, включая родительскую"""

		snode = self.get_node(node_uuid)
		if snode is None:
			return []

		nodes = [node for node in self.nodes
				 if node.tree_lk >= snode.tree_lk
				 and node.tree_rk <= snode.tree_rk]

		nodes.sort(key=lambda row: row.tree_lk)
		return nodes

	#--- tree finds -----------------------------------------------------------





	def get_childrens(self, parent_node):
		childrens = [node for node in self.nodes 
				if node.tree_lk > parent_node.tree_lk 
				and node.tree_rk < parent_node.tree_rk 
				and node.tree_level - 1 == parent_node.tree_level]

		childrens.sort(key=lambda row: row.tree_lk)
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




	def move_node_up(self, node_uuid):
		"""перемещение ноды вверх
			!!!! не реализовано перемещение поддерева !!!!
		"""

		parent_node = self.find_parent_node(node_uuid)
		childrens = self.get_childrens(parent_node)
		childrens_uuid = [node.uuid for node in childrens]


		index = childrens_uuid.index(node_uuid)

		node_a = childrens[index]
		if node_a.tree_rk - node_a.tree_lk > 1:
			log.warning("невозможно переместить ноду - она имеет потомков!!!")
			return False

		if index > 0:

			node_b = childrens[index - 1]

			self.__swap_nodes(node_a, node_b)



			return True

		return False




	def move_node_down(self, node_uuid):
		"""перемещение ноды вверх
			!!!! не реализовано перемещение поддерева !!!!
		"""
		parent_node = self.find_parent_node(node_uuid)
		childrens = self.get_childrens(parent_node)
		childrens_uuid = [node.uuid for node in childrens]


		index = childrens_uuid.index(node_uuid)

		node_a = childrens[index]
		if node_a.tree_rk - node_a.tree_lk > 1:
			log.warning("невозможно переместить ноду - она имеет потомков!!!")
			return False

		if index + 1 < len(childrens_uuid):

			node_b = childrens[index + 1]

			self.__swap_nodes(node_a, node_b)

			return True

		return False




	def __swap_nodes(self, node_1, node_2):

		#--- очерёдность
		if node_1.tree_lk < node_2.tree_lk:
			node_a = node_1
			node_b = node_2
		else:
			node_a = node_2
			node_b = node_1


		#--- получаем ветки нод
		branch_a = self.find_branch(node_a.uuid)
		branch_b = self.find_branch(node_b.uuid)



		# print(branch_a)
		# print(branch_b)


		#--- вычисляем различия
		lk_diff = node_b.tree_lk - node_a.tree_lk
		rk_diff = node_b.tree_rk - node_a.tree_rk

		#--- обновляем ветки
		for node in branch_b:
			#--- уменьшаем ключи для нижней ветки на разницу в lk
			node.tree_lk -= lk_diff
			node.tree_rk -= lk_diff

		for node in branch_a:
			#--- увеличиваем ключи для верхней ветки на разницу в rk
			node.tree_lk += rk_diff
			node.tree_rk += rk_diff


		# lk_a = node_a.tree_lk
		# rk_a = node_a.tree_rk
		#
		# node_a.tree_lk = node_b.tree_lk
		# node_a.tree_rk = node_b.tree_rk
		#
		# node_b.tree_lk = lk_a
		# node_b.tree_rk = rk_a


	
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


	
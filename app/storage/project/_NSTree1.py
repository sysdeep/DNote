#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
http://www.getinfo.ru/article610.html
"""

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
		root_node.uuid			= "0"

		self.nodes = [root_node]
		self.nodes_map[root_node.uuid] = root_node
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



	def create_node(self, parent_node_uuid, node_uuid, name=""):
		"""создание новой ноды от родителя"""
		log.debug("создание новой ноды для родителя: " + parent_node_uuid)
		parent_node = self.nodes_map[parent_node_uuid]
		new_node = NSNode()
		new_node.uuid = node_uuid
		new_node.name = name
		self.__insert_node(parent_node, new_node)
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




	def __insert_node(self, parent_node, new_node):
		"""добавление новой ноды к родительской ветви"""
		
		parent_rk = parent_node.tree_rk
		# parent_lk = parent_node.tree_lk

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
		



	def __insert_branch(self, parent_node, new_branch):
		"""
			добавление новой ветви к родительской ноде
			новая ветвь вставляется первой в списке потомков

			Args:
			    parent_node		[node]
			    new_branch		[list(node)]
		"""

		parent_rk = parent_node.tree_rk
		parent_lk = parent_node.tree_lk
		parent_level = parent_node.tree_level

		#--- смещение от новых нод
		diff = len(new_branch) * 2


		#--- обновляем список после вставки вместе с детёнышами
		for node in self.nodes:
			#--- все ноды после родительской
			if node.tree_lk > parent_lk:
				node.tree_lk += diff
				node.tree_rk += diff



		#--- обновляем правые ключи до родителя(включительно)
		for node in self.nodes:
			#--- все ноды до родителя(включительно)
			if node.tree_rk >= parent_rk and node.tree_lk < parent_rk:
				node.tree_rk += diff



		#--- вставка новой ветви первой в очереди
		new_branch.sort(key=lambda node: node.tree_lk)			# сортировка для получения первой ноды
		first_node = new_branch[0]

		#--- вычисляем различие ключей от родителя для обновления
		diff_k = parent_lk + 1 - first_node.tree_lk
		diff_l = parent_level + 1 - first_node.tree_level

		for node in new_branch:
			node.tree_lk += diff_k
			node.tree_rk += diff_k
			node.tree_level += diff_l


		#--- добавляем ноды в список
		for node in new_branch:
			self.nodes.append(node)
			self.nodes_map[node.uuid] = node

		#--- на всякий случай сортируем
		self.nodes.sort(key=lambda node: node.tree_lk)





	def __remove_branch(self, node):
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


		return del_nodes








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


	def find_next_node(self, node_uuid):
		snode = self.get_node(node_uuid)
		result = None
		for node in self.nodes:
			if (node.tree_level == snode.tree_level) and (node.tree_lk - 1 == snode.tree_rk):
				result = node
				break
		return result

	def find_prev_node(self, node_uuid):
		snode = self.get_node(node_uuid)
		result = None
		for node in self.nodes:
			if (node.tree_level == snode.tree_level) and (node.tree_rk + 1 == snode.tree_lk):
				result = node
				break
		return result
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


		prev_node = self.find_prev_node(node_uuid)

		if prev_node is None:
			return False

		node = self.get_node(node_uuid)

		self.__swap_nodes(node, prev_node)
		return True

		# parent_node = self.find_parent_node(node_uuid)
		# childrens = self.get_childrens(parent_node)
		# childrens_uuid = [node.uuid for node in childrens]
		#
		#
		# index = childrens_uuid.index(node_uuid)
		#
		# node_a = childrens[index]
		# # if node_a.tree_rk - node_a.tree_lk > 1:
		# # 	log.warning("невозможно переместить ноду - она имеет потомков!!!")
		# # 	return False
		#
		# if index > 0:
		#
		# 	node_b = childrens[index - 1]
		#
		# 	self.__swap_nodes(node_a, node_b)
		#
		#
		#
		# 	return True
		#
		# return False




	def move_node_down(self, node_uuid):
		"""перемещение ноды вверх
			!!!! не реализовано перемещение поддерева !!!!
		"""

		next_node = self.find_next_node(node_uuid)

		if next_node is None:
			return False

		node = self.get_node(node_uuid)

		self.__swap_nodes(node, next_node)
		return True

		#
		# parent_node = self.find_parent_node(node_uuid)
		# childrens = self.get_childrens(parent_node)
		# childrens_uuid = [node.uuid for node in childrens]
		#
		#
		# index = childrens_uuid.index(node_uuid)
		#
		# node_a = childrens[index]
		# if node_a.tree_rk - node_a.tree_lk > 1:
		# 	log.warning("невозможно переместить ноду - она имеет потомков!!!")
		# 	return False
		#
		# if index + 1 < len(childrens_uuid):
		#
		# 	node_b = childrens[index + 1]
		#
		# 	self.__swap_nodes(node_a, node_b)
		#
		# 	return True
		#
		# return False




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




	def move_node(self, node_uuid, dest_uuid):
		"""перемещение заданной ноды(ветви) в указнного родителя"""
		log.debug("перемещение ноды")

		node = self.get_node(node_uuid)
		parent_node = self.get_node(dest_uuid)

		#--- remove node(branch)
		nodes_branch = self.__remove_branch(node)

		#--- insert node(branch)
		self.__insert_branch(parent_node, nodes_branch)



	# def cut_branch(self, node_uuid):
	# 	""""""
	# 	node = self.get_node(node_uuid)
	#
	# 	return self.__remove_branch(node)
	#
	#
	# def insert_branch(self, parent_node_uuid, nodes_branch):
	#
	# 	parent_node = self.get_node(parent_node_uuid)
	#
	# 	self.__insert_branch(parent_node, nodes_branch)






	
	#--- prints ---------------------------------------------------------------
	def print_nodes(self):
		for node in sorted(self.nodes, key=lambda a: a.tree_lk):
			# print(self.__fill_tabs(node.tree_level) + node.name + " - " + str(node.tree_lk) + " - " + str(node.tree_rk))
			# print(self.__fill_tabs(node.tree_level) + node.name + "(" + str(node.uuid) + ")")
			print(self.__fill_tabs(node.tree_level) + node.name + "[" + str(node.tree_lk) + ":" + str(node.tree_rk) + "]")

	def __fill_tabs(self, num):
		return "  "*num
	#--- prints ---------------------------------------------------------------


















if __name__ == '__main__':

	import json

	tree = NSTree()
	FILE_PROJECT = "/home/nia/Development/_Python/_DNote/tests/tupdown/project.json"


	with open(FILE_PROJECT, "r", encoding="utf-8") as fd:
		data_json = fd.read()

	data = json.loads(data_json)
	# tree.load(data["tree"])






	# def create(parent_uuid, node_uuid, name):
	# 	node = tree.create_node(parent_uuid)
	# 	node.name = name
	# 	node.uuid = node_uuid

	
	

	tree.print_nodes()

	tree.create_node("0", "1", "1")
	tree.create_node("1", "11", "11")
	tree.create_node("1", "12", "12")



	tree.create_node("0", "2", "2")
	tree.create_node("2", "21", "21")
	tree.create_node("2", "22", "22")
	tree.create_node("2", "23", "23")
	tree.create_node("23", "231", "231")


	tree.print_nodes()


	print("--- move ---------------------------")
	nodes = tree.move_node("23", "1")
	tree.print_nodes()
	# print(tree.nodes)
	print("--- move ---------------------------")

	# print("--- cut ---------------------------")
	# nodes = tree.cut_branch("2")
	# tree.print_nodes()
	# print("--- cut ---------------------------")
	#
	# print("--- paste ---------------------------")
	# nodes = tree.insert_branch("1", nodes)
	# tree.print_nodes()
	# print("--- paste ---------------------------")


	# print("------------------------------")
	# tree.remove_node("22")
	# tree.print_nodes()
	# print("------------------------------")
	#
	#
	#
	# print("------------------------------")
	# tree.move_node_up("23")
	# tree.print_nodes()
	# print("------------------------------")
	#
	# print("------------------------------")
	# tree.move_node_up("2")
	# tree.print_nodes()
	# print("------------------------------")




	
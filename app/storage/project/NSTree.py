#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
http://www.getinfo.ru/article610.html



	public:
		load(nodes_list)
		create_node(parent_node_uuid, node_uuid, name="")	-> node
		remove_node(node_uuid)								-> [node]
		get_node(node_uuid)									-> node
		move_node_up(node_uuid)								-> bool
		move_node_down(node_uuid)							-> bool
		move_node(node_uuid, dest_uuid)
		find_parent_node(node_uuid)							-> node
		find_childrens(node_uuid)							-> [node]
		find_parent_branch(node_uuid)						-> [node]
		find_branch(node_uuid)								-> [node]
		find_next_node(node_uuid)							-> node/None
		find_prev_node(node_uuid)							-> node/None
		get_nodes_level(level)								-> [node]
		export()											-> [node_dict]
		set_empty()


	private:
		__insert_node(parent_node, new_node)
		__insert_branch(parent_node, new_branch)
		__remove_branch(node)								-> [node]
		__swap_nodes(node_1, node_2)

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



	def create_node(self, parent_node_uuid, node_uuid, name="", ntype="text"):
		"""создание новой ноды от родителя"""
		log.debug("создание новой ноды для родителя: " + parent_node_uuid)
		parent_node = self.nodes_map[parent_node_uuid]
		new_node = NSNode()
		new_node.uuid = node_uuid
		new_node.name = name
		new_node.ntype = ntype
		self.__insert_node(parent_node, new_node)
		return new_node



	def remove_node(self, node_uuid):
		"""удаление заданной ноды из дерева"""
		log.debug("удаление заданной ноды из дерева: " + node_uuid)
		node = self.get_node(node_uuid)

		if node:
			return self.__remove_branch(node)
		else:
			return []


	def get_node(self, node_uuid):

		node = self.nodes_map.get(node_uuid)
		if node is None:
			log.error("get_node - no node found with uuid: " + node_uuid)

		return node



	def move_node_up(self, node_uuid):
		"""перемещение ноды вверх"""

		prev_node = self.find_prev_node(node_uuid)

		if prev_node is None:
			log.debug("prev node is None")
			return False

		node = self.get_node(node_uuid)

		self.__swap_nodes(node, prev_node)
		return True





	def move_node_down(self, node_uuid):
		"""перемещение ноды вверх
			!!!! не реализовано перемещение поддерева !!!!
		"""

		next_node = self.find_next_node(node_uuid)

		if next_node is None:
			log.debug("next node is None")
			return False

		node = self.get_node(node_uuid)

		self.__swap_nodes(node, next_node)
		return True



	def move_node(self, node_uuid, dest_uuid):
		"""перемещение заданной ноды(ветви) в указнного родителя"""
		log.debug("перемещение ноды")

		node = self.get_node(node_uuid)
		parent_node = self.get_node(dest_uuid)

		#--- remove node(branch)
		nodes_branch = self.__remove_branch(node)

		#--- insert node(branch)
		self.__insert_branch(parent_node, nodes_branch)


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



	def get_nodes_level(self, level):
		"""получить все ноды заданного уровня"""
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
	#--- public ---------------------------------------------------------------






















	#--- tree operations ------------------------------------------------------
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

	#--- tree operations ------------------------------------------------------



















	#--- prints ---------------------------------------------------------------
	def print_nodes(self):
		for node in sorted(self.nodes, key=lambda a: a.tree_lk):
			# print(self.__fill_tabs(node.tree_level) + node.name + " - " + str(node.tree_lk) + " - " + str(node.tree_rk))
			# print(self.__fill_tabs(node.tree_level) + node.name + "(" + str(node.uuid) + ")")
			print(self.__fill_tabs(node.tree_level) + node.name + "[" + str(node.tree_lk) + ":" + str(node.tree_rk) + "]")

	def __fill_tabs(self, num):
		return "  "*num
	#--- prints ---------------------------------------------------------------















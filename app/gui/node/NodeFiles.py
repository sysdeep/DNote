#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QListWidgetItem, QFileDialog
from .. import events

class NodeFiles(QGroupBox):
	def __init__(self, parent=None):
		super(NodeFiles, self).__init__(parent)
		self.setTitle("files")
		self.main_layout = QVBoxLayout(self)

		self.node = None
		
		grid = QGridLayout()
		self.main_layout.addLayout(grid)

		self.label_files_len = QLabel()
		grid.addWidget(QLabel("files:"), 0, 0)
		grid.addWidget(self.label_files_len, 0, 1)

		btn_show = QPushButton("show")
		btn_show.clicked.connect(self.__show_files_modal)
		self.main_layout.addWidget(btn_show)
		# for index, item in enumerate(self.node_items):
		# 	self.main_layout.addWidget(QLabel(item), index, 0)

		# 	label = QLabel()
		# 	self.main_layout.addWidget(label, index, 1)
		# 	self.node_labels[item] = label



		edit_box = QHBoxLayout()
		self.main_layout.addLayout(edit_box)

		self.clist = QListWidget()
		edit_box.addWidget(self.clist)


		actions_box = QVBoxLayout()
		edit_box.addLayout(actions_box)

		btn_add = QPushButton("add")
		btn_add.clicked.connect(self.__on_add_action)

		btn_remove = QPushButton("remove")
		actions_box.addWidget(btn_add)
		actions_box.addWidget(btn_remove)
		actions_box.addStretch()


		#--- events
		events.on("update_current_node", self.__update_current)



	def update_node(self, node):
		self.node = node
		self.__update_current()
		self.__load_files()
		


	def __update_current(self):

		node_files = self.node.files

		self.label_files_len.setText( str(len(node_files.files)) )
		

	def __show_files_modal(self):

		events.show_edit_files(self.node)


	def __load_files(self):
		# self.current_ipack = ICON_PACKS[index]

		self.clist.clear()

		files = self.node.files.files

		# self.clist.clear()
		for f in files:

			# icon = QIcon(get_icon_path(self.current_ipack, f))
			# item = QListWidgetItem(icon, f)
			item = QListWidgetItem(f)
			# item.setData(Qt.UserRole+1, f)
			self.clist.addItem(item)

	



	def __on_add_action(self):
		fname = QFileDialog.getOpenFileName(self, "Open")			# (file_name, file_filter)

		print(fname)

		if fname[0]:
			self.node.create_file(fname[0])

			#--- send events
			events.update_current_node()				# update_tree - вызовет и это

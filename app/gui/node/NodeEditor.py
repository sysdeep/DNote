#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit

from app.storage import get_storage

from .. import events




class NodeEditor(QGroupBox):
	def __init__(self, parent=None):
		super(NodeEditor, self).__init__(parent)
		self.setTitle("editor")
		self.main_layout = QVBoxLayout(self)

		self.node = None
		self.storage = get_storage()

		self.__make_gui()




	def __make_gui(self):

		self.name_edit = QLineEdit()
		self.main_layout.addWidget(self.name_edit)


		self.text_edit = QTextEdit()
		self.main_layout.addWidget(self.text_edit)




		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)

		btn_save = QPushButton("save")
		btn_save.clicked.connect(self.__save)


		controls.addStretch()
		controls.addWidget(btn_save)


	def update_node(self, node):
		self.node = node

		#--- node name
		name = node.name
		self.name_edit.setText(name)

		#--- page text
		text = node.page.raw_text
		self.text_edit.setText(text)



	def __save(self):


		#--- get data
		name = self.name_edit.text()
		text = self.text_edit.toPlainText()


		#--- update node data
		self.node.set_name(name)
		self.node.page.raw_text = text
		self.node.write_node()


		#--- update project data
		self.storage.project.set_node_name(self.node.uuid, name)
		self.storage.project.write_file()


		#--- send events
		# events.update_current_node()				# update_tree - вызовет и это
		events.update_tree()





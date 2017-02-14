#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit

from app.storage import get_storage

from .. import events

from .style_python import PythonHighlighter
from .style_md import MarkdownHighlighter


class NodeEditor(QGroupBox):
	def __init__(self, parent=None):
		super(NodeEditor, self).__init__(parent)
		self.setTitle("editor")
		self.main_layout = QVBoxLayout(self)

		self.node = None
		self.storage = get_storage()

		self.__make_gui()




	def __make_gui(self):

		self.text_edit = QTextEdit()
		self.main_layout.addWidget(self.text_edit)

		#--- подсветка синтаксиса
		# self.hh = PythonHighlighter(self.text_edit.document())
		# self.hh = MarkdownHighlighter(self.text_edit)


		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)


		btn_new_node = QPushButton("old create")
		btn_new_node.clicked.connect(self.__create_node)


		btn_remove_node = QPushButton("old remove")
		btn_remove_node.clicked.connect(self.__remove_node)


		btn_show_icons = QPushButton("old icon")
		btn_show_icons.clicked.connect(self.__show_icons)



		btn_save = QPushButton("save")
		btn_save.clicked.connect(self.__save)

		controls.addWidget(btn_new_node)
		controls.addWidget(btn_remove_node)
		controls.addWidget(btn_show_icons)
		controls.addStretch()
		controls.addWidget(btn_save)


	def update_node(self, node):
		self.node = node


		#--- page text
		text = node.page.raw_text
		self.text_edit.setText(text)



	def __save(self):


		#--- get data
		text = self.text_edit.toPlainText()


		#--- update node data
		self.node.page.raw_text = text
		self.node.write_node()


		#--- send events
		events.update_current_node()				# update_tree - вызовет и это
		# events.update_tree()


	def __create_node(self):
		"""создание новой ноды от родителя"""
		parent_project_node = self.storage.project.find_node_by_uuid(self.node.uuid)
		events.show_modal_create_node(parent_node=parent_project_node)

	def __remove_node(self):
		"""удаление ноды от родителя"""

		events.show_remove_node(self.node.uuid)

	def __show_icons(self):

		events.show_edit_icon(self.node.uuid)


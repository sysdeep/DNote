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

		self.storage.eon("node_selected", self.__update_node_data)




	def __make_gui(self):

		self.text_edit = QTextEdit()
		self.main_layout.addWidget(self.text_edit)

		#--- подсветка синтаксиса
		# self.hh = PythonHighlighter(self.text_edit.document())
		# self.hh = MarkdownHighlighter(self.text_edit)


		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)





		btn_save = QPushButton("save")
		btn_save.clicked.connect(self.__save)

		controls.addStretch()
		controls.addWidget(btn_save)



	def __update_node_data(self):
		# self.node = node

		self.node = self.storage.get_current_node()


		#--- page text
		text = self.node.page.raw_text
		self.text_edit.setText(text)





	def __save(self):


		#--- get data
		text = self.text_edit.toPlainText()

		#--- update node data
		self.node.update_page_text(text)


		#--- send events
		# events.update_current_node()				# update_tree - вызовет и это
		# events.update_tree()


	
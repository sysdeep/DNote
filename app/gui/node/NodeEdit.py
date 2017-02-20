#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtWebKitWidgets import QWebView

from vendors import markdown
from app.storage import get_storage

from .. import events






class NodeEdit(QWidget):
	def __init__(self, parent=None):
		super(NodeEdit, self).__init__(parent)
		# self.setTitle("viewer")
		self.main_layout = QVBoxLayout(self)

		self.node = None
		self.storage = get_storage()

		self.__make_gui()

		self.storage.eon("node_selected", self.__on_node_selected)
		# self.storage.eon("node_updated", self.__on_node_updated)




	def __make_gui(self):

		self.text_edit = QTextEdit()
		self.main_layout.addWidget(self.text_edit)


		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)


		self.btn_save = QPushButton("save")
		self.btn_save.clicked.connect(self.__on_save)


		controls.addStretch()
		controls.addWidget(self.btn_save)

		



	def __on_node_selected(self):
		self.node = self.storage.get_current_node()
		self.__set_content()
		




	# def __on_node_updated(self):
	# 	self.__set_content()

	



	def __set_content(self):


		# self.setTitle(self.node.name + "["+self.node.meta.ntype+"]")

		text = self.node.page.raw_text
		self.text_edit.setText(text)




	def __on_save(self):
		#--- get data
		text = self.text_edit.toPlainText()

		#--- update node data
		self.node.update_page_text(text)



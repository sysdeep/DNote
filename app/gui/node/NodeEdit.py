#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtWebKitWidgets import QWebView


from app.storage import get_storage, smanager, sevents







class NodeEdit(QWidget):
	def __init__(self, parent=None):
		super(NodeEdit, self).__init__(parent)
		# self.setTitle("viewer")
		self.main_layout = QVBoxLayout(self)

		# self.node = None
		# self.storage = smanager.get_storage()
		# self.storage = get_storage()

		self.__make_gui()

		sevents.eon("node_selected", self.__on_node_selected)




	def __make_gui(self):

		self.text_edit = QTextEdit()
		self.text_edit.setAcceptRichText(False)					# disable ctrl+v rich text
		self.main_layout.addWidget(self.text_edit)


		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)


		self.btn_save = QPushButton("save")
		self.btn_save.clicked.connect(self.__on_save)
		# self.


		controls.addStretch()
		controls.addWidget(self.btn_save)

		



	def __on_node_selected(self):
		# self.node = smanager.storage.get_current_node()
		self.__set_content()
		




	# def __on_node_updated(self):
	# 	self.__set_content()

	



	def __set_content(self):
		storage = smanager.get_storage()
		text = storage.nnode.page.raw_text
		self.text_edit.setPlainText(text)




	def __on_save(self):

		storage = smanager.get_storage()

		#--- get data
		text = self.text_edit.toPlainText()

		#--- update node data
		storage.nnode.update_page_text(text)

		#--- send event
		storage.update_node_event()



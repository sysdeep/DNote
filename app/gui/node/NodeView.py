#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtWebKitWidgets import QWebView

from vendors import markdown
from app.storage import get_storage, smanager, sevents

from .. import events






class NodeViewe(QWidget):
	def __init__(self, parent=None):
		super(NodeViewe, self).__init__(parent)
		# self.setTitle("viewer")
		self.main_layout = QVBoxLayout(self)

		self.node = None
		# self.storage = get_storage()
		self.storage = smanager.get_storage()

		self.__make_gui()

		sevents.eon("node_selected", self.__on_node_selected)
		# sevents.eon("storage_opened", self.__on_storage_opened)
		sevents.eon("node_updated", self.__on_node_updated)




	def __make_gui(self):


		self.web = QWebView()
		self.main_layout.addWidget(self.web)
		# self.web.setHtml(html)




	def __on_node_selected(self):
		print("selected")
		# self.node = self.storage.get_current_node()
		self.node = smanager.storage.get_current_node()
		self.__set_content()
		




	def __on_node_updated(self):
		self.__set_content()

	



	def __set_content(self):


		# self.setTitle(self.node.name + "["+self.node.meta.ntype+"]")

		text = self.node.page.raw_text

		if self.node.meta.ntype == "text":
			# self.web.setHtml(text)
			html = markdown.markdown(text)
			self.web.setHtml(html)
		elif self.node.meta.ntype == "markdown":
			html = markdown.markdown(text)
			self.web.setHtml(html)



	# def __on_storage_opened(self):
	# 	print("opened")
	# 	self.storage = smanager.get_storage()



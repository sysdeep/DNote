#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtWebKitWidgets import QWebView

from vendors import markdown
from app.storage import storage






class NodeViewe(QWidget):
	def __init__(self, parent=None):
		super(NodeViewe, self).__init__(parent)
		# self.setTitle("viewer")
		self.main_layout = QVBoxLayout(self)

		# self.node = None
		# self.storage = get_storage()
		# self.storage = smanager.get_storage()

		self.web = QWebView()
		self.main_layout.addWidget(self.web)
		# self.web.setHtml(html)



	def update_data(self):
		self.__set_content()





	def __set_content(self):


		# self.setTitle(self.node.name + "["+self.node.meta.ntype+"]")


		# text = self.node.page.raw_text
		# storage = smanager.get_storage()
		text = storage.nnode.page.raw_text


		# html = markdown.markdown(text, extensions=[CImgExtension(), 'vendors.markdown.extensions.tables'])
		html = markdown.markdown(text, extensions=['vendors.markdown.extensions.tables'])
		self.web.setHtml(html)

		# if self.node.meta.ntype == "text":
		# 	# self.web.setHtml(text)
		# 	html = markdown.markdown(text)
		# 	self.web.setHtml(html)
		# elif self.node.meta.ntype == "markdown":
		# 	html = markdown.markdown(text)
		# 	self.web.setHtml(html)



	# def __on_storage_opened(self):
	# 	print("opened")
	# 	self.storage = smanager.get_storage()



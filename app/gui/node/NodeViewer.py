#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit, QTabWidget
from PyQt5.QtWebKitWidgets import QWebView

from vendors import markdown
from app.storage import get_storage, smanager, sevents

from .. import events
from ..modals.NodeEditor import NodeEditor
from ..modals.NodeHtmlViewer import NodeHtmlViewer

from .style_python import PythonHighlighter
from .style_md import MarkdownHighlighter

from .NodeView import NodeViewe
from .NodeEdit import NodeEdit






class NodeViewer(QGroupBox):
	def __init__(self, parent=None):
		super(NodeViewer, self).__init__(parent)
		self.setTitle("viewer")
		self.main_layout = QVBoxLayout(self)

		self.node = None
		self.storage = smanager.get_storage()
		# self.storage = get_storage()

		self.__make_gui()

		sevents.eon("node_selected", self.__on_node_selected)
		# sevents.eon("storage_opened", self.__on_storage_opened)
		# self.storage.eon("node_selected", self.__on_node_selected)
		sevents.eon("node_updated", self.__on_node_updated)




	def __make_gui(self):


		tabs = QTabWidget()
		self.main_layout.addWidget(tabs)


		node_view = NodeViewe()
		node_edit = NodeEdit()

		tabs.addTab(node_view, "Просмотр")
		tabs.addTab(node_edit, "Редактирование")


		# self.web = QWebView()
		# self.main_layout.addWidget(self.web)
		# self.web.setHtml(html)

		# #--- controls
		# controls = QHBoxLayout()
		# self.main_layout.addLayout(controls)


		# self.btn_show_edit = QPushButton("show_edit")
		# self.btn_show_edit.clicked.connect(self.__on_show_edit)

		# self.btn_show_html = QPushButton("show_html")
		# self.btn_show_html.clicked.connect(self.__on_show_html)



		# controls.addStretch()
		# controls.addWidget(self.btn_show_edit)
		# controls.addWidget(self.btn_show_html)



	def __on_node_selected(self):
		# self.node = node

		self.node = smanager.storage.get_current_node()
		
		

		# text = self.node.page.raw_text


		self.__set_content()
		# if self.node.meta.ntype == "text":
		# 	self.__set_view_text(text)
		# elif self.node.meta.ntype == "markdown":
		# 	self.__set_view_markdown(text)
		# else:
		# 	pass
		#--- page text
		
		
		# self.web.setHtml(text)

		




	def __on_node_updated(self):
		self.__set_content()

		# text = self.node.page.raw_text
		# html = markdown.markdown(text)
		# self.web.setHtml(html)





	def __set_content(self):


		self.setTitle(self.node.name + "["+self.node.meta.ntype+"]")

		# text = self.node.page.raw_text

		# if self.node.meta.ntype == "text":
		# 	# self.web.setHtml(text)
		# 	html = markdown.markdown(text)
		# 	self.web.setHtml(html)
		# elif self.node.meta.ntype == "markdown":
		# 	html = markdown.markdown(text)
		# 	self.web.setHtml(html)



	# def __on_storage_opened(self):
	# 	self.storage = smanager.get_storage()




	# def __on_show_edit(self):
	# 	modal = NodeEditor(self.node, self)
	# 	modal.show()


	# def __on_show_html(self):
	# 	modal = NodeHtmlViewer(self.node, self)
	# 	modal.show()

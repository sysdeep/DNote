#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtWebKitWidgets import QWebView

from vendors import markdown
from app.storage import get_storage

from .. import events
from ..modals.NodeEditor import NodeEditor
from ..modals.NodeHtmlViewer import NodeHtmlViewer

from .style_python import PythonHighlighter
from .style_md import MarkdownHighlighter



html = '''<html>
<head>
<title>A Sample Page</title>
</head>
<body>
<h1>Hello, World!</h1>
<hr />
I have nothing to say.
</body>
</html>'''






class NodeViewer(QGroupBox):
	def __init__(self, parent=None):
		super(NodeViewer, self).__init__(parent)
		self.setTitle("viewer")
		self.main_layout = QVBoxLayout(self)

		self.node = None
		self.storage = get_storage()

		self.__make_gui()

		self.storage.eon("node_selected", self.__on_node_selected)
		self.storage.eon("node_updated", self.__on_node_updated)




	def __make_gui(self):


		self.web = QWebView()
		self.main_layout.addWidget(self.web)
		# self.web.setHtml(html)

		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)


		self.btn_show_edit = QPushButton("show_edit")
		self.btn_show_edit.clicked.connect(self.__on_show_edit)

		self.btn_show_html = QPushButton("show_html")
		self.btn_show_html.clicked.connect(self.__on_show_html)



		controls.addStretch()
		controls.addWidget(self.btn_show_edit)
		controls.addWidget(self.btn_show_html)



	def __on_node_selected(self):
		# self.node = node

		self.node = self.storage.get_current_node()
		
		

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

		text = self.node.page.raw_text

		if self.node.meta.ntype == "text":
			# self.web.setHtml(text)
			html = markdown.markdown(text)
			self.web.setHtml(html)
		elif self.node.meta.ntype == "markdown":
			html = markdown.markdown(text)
			self.web.setHtml(html)








	def __on_show_edit(self):
		modal = NodeEditor(self.node, self)
		modal.show()


	def __on_show_html(self):
		modal = NodeHtmlViewer(self.node, self)
		modal.show()

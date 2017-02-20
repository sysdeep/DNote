#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtWebKitWidgets import QWebView

from vendors import markdown
from app.storage import get_storage

from .. import events
from ..modals.NodeEditor import NodeEditor as NodeEditorModal

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

class NodeEditor(QGroupBox):
	def __init__(self, parent=None):
		super(NodeEditor, self).__init__(parent)
		self.setTitle("editor")
		self.main_layout = QVBoxLayout(self)

		self.node = None
		self.storage = get_storage()

		self.__make_gui()

		self.storage.eon("node_selected", self.__on_node_selected)
		self.storage.eon("node_updated", self.__on_node_updated)




	def __make_gui(self):

		self.text_edit = QTextEdit()
		self.main_layout.addWidget(self.text_edit)

		#--- подсветка синтаксиса
		# self.hh = PythonHighlighter(self.text_edit.document())
		# self.hh = MarkdownHighlighter(self.text_edit)


		self.web = QWebView()
		self.main_layout.addWidget(self.web)
		# self.web.setHtml(html)

		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)



		self.btn_view_edit = QPushButton("edit")
		self.btn_view_edit.clicked.connect(self.__on_set_view_edit)

		self.btn_view_web = QPushButton("web")
		self.btn_view_web.clicked.connect(self.__on_set_view_web)


		self.btn_show_edit = QPushButton("show_edit")
		self.btn_show_edit.clicked.connect(self.__on_show_edit)


		self.btn_save = QPushButton("save")
		self.btn_save.clicked.connect(self.__save)

		controls.addWidget(self.btn_view_web)
		controls.addWidget(self.btn_view_edit)
		controls.addStretch()
		controls.addWidget(self.btn_show_edit)
		controls.addStretch()
		controls.addWidget(self.btn_save)



	def __on_node_selected(self):
		# self.node = node

		self.node = self.storage.get_current_node()
		
		self.setTitle(self.node.name)

		text = self.node.page.raw_text

		if self.node.meta.ntype == "text":
			self.__set_view_text(text)
		elif self.node.meta.ntype == "markdown":
			self.__set_view_markdown(text)
		else:
			pass
		#--- page text
		
		
		# self.web.setHtml(text)

		




	def __on_node_updated(self):
		self.setTitle(self.node.name)

		text = self.node.page.raw_text
		html = markdown.markdown(text)
		self.web.setHtml(html)




	def __save(self):


		#--- get data
		text = self.text_edit.toPlainText()

		#--- update node data
		self.node.update_page_text(text)


		#--- send events
		# events.update_current_node()				# update_tree - вызовет и это
		# events.update_tree()



	def __set_view_text(self, text):
		self.__on_set_view_edit()
		self.text_edit.setText(text)
		self.btn_view_web.setDisabled(True)
		


	def __set_view_markdown(self, text):
		self.__on_set_view_web()
		self.text_edit.setText(text)
		html = markdown.markdown(text)
		self.web.setHtml(html)



	def __on_set_view_edit(self):
		self.web.hide()
		self.text_edit.show()
		self.btn_view_edit.setDisabled(True)
		self.btn_view_web.setEnabled(True)
		self.btn_save.setEnabled(True)

	def __on_set_view_web(self):
		self.web.show()
		self.text_edit.hide()
		self.btn_view_web.setDisabled(True)
		self.btn_view_edit.setEnabled(True)
		self.btn_save.setEnabled(False)




	def __on_show_edit(self):
		modal = NodeEditorModal(self.node, self)
		modal.show()

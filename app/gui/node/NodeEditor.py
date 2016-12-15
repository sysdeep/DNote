#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton

from .. import events

class NodeEditor(QGroupBox):
	def __init__(self, parent=None):
		super(NodeEditor, self).__init__(parent)
		self.setTitle("editor")
		self.main_layout = QVBoxLayout(self)

		self.node = None

		self.text_edit = QTextEdit()
		self.main_layout.addWidget(self.text_edit)

		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)

		btn_save = QPushButton("save")
		btn_save.clicked.connect(self.__save)

		controls.addStretch()
		controls.addWidget(btn_save)

		

	def update_node(self, node):
		self.node = node
		# print(dir(node))
		# page = node.page
		text = node.page.raw_text

		self.text_edit.setText(text)



	def __save(self):

		text = self.text_edit.toPlainText()

		self.node.page.raw_text = text

		self.node.write_node()

		events.update_current_node()





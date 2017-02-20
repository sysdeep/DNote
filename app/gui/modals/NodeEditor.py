#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QTextEdit, QFormLayout, QLineEdit
from PyQt5.QtGui import QFont



from app.storage import get_storage



class NodeEditor(QDialog):
	def __init__(self, node, parent=None):
		super(NodeEditor, self).__init__(parent)

		self.setWindowTitle("Node Editor")
		self.setMinimumHeight(400)
		self.setMinimumWidth(500)


		self.node = node





		# self.main_layout = QGridLayout(self)
		self.main_layout = QVBoxLayout(self)


		self.text_edit = QTextEdit()



		
		

		self.main_layout.addWidget(self.text_edit)
		self.main_layout.addStretch()



		#--- controls
		c_box = QHBoxLayout()
		self.main_layout.addLayout(c_box)

		btn_close = QPushButton("Close")
		btn_close.clicked.connect(self.close)

		btn_save = QPushButton("Save")
		btn_save.clicked.connect(self.__on_save)

		c_box.addStretch()
		c_box.addWidget(btn_save)
		c_box.addWidget(btn_close)



		text = self.node.page.raw_text
		self.text_edit.setText(text)
		

	def __on_save(self):
		#--- get data
		text = self.text_edit.toPlainText()

		#--- update node data
		self.node.update_page_text(text)

		# self.__update_current()


	# def __update_current(self):
	# 	self.node_labels["ntype"].setText(self.node.meta.ntype)
	# 	self.node_labels["uuid"].setText(self.node.meta.uuid)
	# 	self.node_labels["name"].setText(self.node.meta.name)
	# 	self.node_labels["path"].setText(self.node.meta.path)
	# 	self.node_labels["ctime"].setText(self.node.meta.get_ctime())
	# 	self.node_labels["mtime"].setText(self.node.meta.get_mtime())

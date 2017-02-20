#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QTextEdit, QFormLayout, QLineEdit
from PyQt5.QtGui import QFont


from vendors import markdown



class NodeHtmlViewer(QDialog):
	def __init__(self, node, parent=None):
		super(NodeHtmlViewer, self).__init__(parent)

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

		

		c_box.addStretch()
		c_box.addWidget(btn_close)



		text = self.node.page.raw_text


		html = markdown.markdown(text)
		self.text_edit.setText(html)
		

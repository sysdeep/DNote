#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QTextEdit, QPushButton, QLineEdit
from PyQt5.QtWebKitWidgets import QWebView


from app.lib.EventEmitter import Signal
# from app.storage import get_storage, smanager, sevents
from app.storage import storage







class NodeEdit(QWidget):

	s_updated = Signal()

	def __init__(self, parent=None):
		super(NodeEdit, self).__init__(parent)
		# self.setTitle("viewer")
		self.main_layout = QVBoxLayout(self)


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

		


	def update_data(self):

		text = storage.nnode.page.raw_text
		self.text_edit.setPlainText(text)





	def __on_save(self):

		# storage = smanager.get_storage()

		#--- get data
		text = self.text_edit.toPlainText()

		#--- update node data
		storage.nnode.update_page_text(text)

		self.s_updated.emit()


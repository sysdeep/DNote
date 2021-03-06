#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QTextEdit, QFormLayout, QLineEdit
from PyQt5.QtGui import QFont

# from app.storage import smanager
from app.storage import create_storage

# TODO: ввести проверки и рефакторинг

class CreateNotebook(QDialog):
	def __init__(self, parent=None):
		super(CreateNotebook, self).__init__(parent)


		self.main_layout = QVBoxLayout(self)


		self.edit_name = QLineEdit()
		self.edit_path = QLineEdit("/home/nia/Development/_Python/_DNote/tests")
		self.main_layout.addWidget(self.edit_name)
		self.main_layout.addWidget(self.edit_path)




		#--- controls
		c_box = QHBoxLayout()
		self.main_layout.addLayout(c_box)

		btn_close = QPushButton("Close")
		btn_close.clicked.connect(self.close)

		btn_create = QPushButton("Create")
		btn_create.clicked.connect(self.__on_create)

		c_box.addStretch()
		c_box.addWidget(btn_create)
		c_box.addWidget(btn_close)




	def __on_create(self):
		name = self.edit_name.text()
		path = self.edit_path.text()


		print(name, path)
		print("!!!!CreateNotebook - not implement")


		create_storage(name, path)


		self.close()
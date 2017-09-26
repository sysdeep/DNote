#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QTextEdit, QFormLayout, QLineEdit
from PyQt5.QtGui import QFont

# from app.storage import smanager
from app.lib import dbus



class OpenNotebook(QDialog):
	def __init__(self, parent=None):
		super(OpenNotebook, self).__init__(parent)


		self.main_layout = QVBoxLayout(self)


		
		self.edit_path = QLineEdit("/home/nia/Development/_Python/_DNote/sdir1/")
		
		self.main_layout.addWidget(self.edit_path)




		#--- controls
		c_box = QHBoxLayout()
		self.main_layout.addLayout(c_box)

		btn_close = QPushButton("Close")
		btn_close.clicked.connect(self.close)

		btn_create = QPushButton("Open")
		btn_create.clicked.connect(self.__on_open)


		btn_select = QPushButton("Select")
		btn_select.clicked.connect(self.__on_select)

		c_box.addWidget(btn_select)
		c_box.addStretch()
		c_box.addWidget(btn_create)
		c_box.addWidget(btn_close)




	def __on_open(self):
		path = self.edit_path.text()

		# print(path)

		# smanager.open_storage(path)
		dbus.emit(dbus.STORAGE_OPEN, path)

		self.close()



	def __on_select(self):
		fname = QFileDialog.getExistingDirectory(self, "Open notebook", "/home/nia/Development/_Python/_DNote/")

		print(fname)

		self.edit_path.setText(fname)

		# if fname[0]:
		# 	self.node.create_file(fname[0])




"""

/home/nia/Development/_Python/_DNote/tests



/home/nia/Development/_Python/_DNote/sdir1/


"""
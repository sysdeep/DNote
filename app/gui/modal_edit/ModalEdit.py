#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QTextEdit
from PyQt5.QtGui import QFont

















class ModalEdit(QDialog):
	def __init__(self, parent=None):
		super(ModalEdit, self).__init__(parent)

		self.main_layout = QHBoxLayout(self)

		self.__make_gui()


	def __make_gui(self):







		controls = QVBoxLayout()
		self.main_layout.addLayout(controls)

		btn_close = QPushButton("Close")
		btn_close.clicked.connect(self.close)

		controls.addStretch()
		controls.addWidget(btn_close)





















if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	import sys
	# from PyQt5.QtWidgets import QStyleFactory
	# from PyQt5.QtCore import QStyleFactory

	app = QApplication(sys.argv)

	# app.setStyle(QStyleFactory.create("fusion"))

	modal = ModalEdit()
	# main_win.DEBUG = True
	# main_win.start_net()
	modal.show()

	app.exec_()
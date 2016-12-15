#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QTextEdit, QFormLayout, QLineEdit
from PyQt5.QtGui import QFont



from app.storage import get_storage








class ModalCreate(QDialog):
	def __init__(self, parent_node=None, parent=None):
		super(ModalCreate, self).__init__(parent)

		self.storage 		= get_storage()
		
		if parent_node is None:
			self.parent_node = self.storage.project.get_root_node()
		else:
			self.parent_node 	= parent_node

		
		self.__make_gui()


	def __make_gui(self):
		
		self.main_layout = QHBoxLayout(self)



		input_layout = QVBoxLayout()
		self.main_layout.addLayout(input_layout)

		form = QFormLayout()
		input_layout.addLayout(form)


		self.edit_name = QLineEdit()

		form.addRow("name", self.edit_name)



		self.edit_text = QTextEdit()
		input_layout.addWidget(self.edit_text)
		



		controls = QVBoxLayout()
		self.main_layout.addLayout(controls)

		btn_close = QPushButton("Close")
		btn_close.clicked.connect(self.close)

		btn_create = QPushButton("Create")
		btn_create.clicked.connect(self.__create)

		controls.addWidget(btn_create)
		controls.addStretch()
		controls.addWidget(btn_close)




	def __create(self):
		"""создание новой ноды"""

		#--- название
		name = self.edit_name.text()

		#--- содержимое
		text = self.edit_text.toPlainText()


		#--- создание дефолтных записей ноды
		node = self.storage.create_node(self.parent_node, name)

		#--- обновление данных
		node.page.raw_text = text
		node.write_node()


		self.close()


















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
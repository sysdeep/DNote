#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox, QTextEdit, QFormLayout, QLineEdit
from PyQt5.QtGui import QFont



from app.storage import storage, NODE_TYPES
# from .. import events






class ModalEditName(QDialog):
	def __init__(self, parent=None):
		super(ModalEditName, self).__init__(parent)

		self.main_layout 	= QVBoxLayout(self)
		self.setWindowTitle("Изменение названия")

		
		# self.types 			= storage.get_node_types()			# типы контента
		# self.node			= storage.pnode
		


		form = QFormLayout()
		self.main_layout.addLayout(form)

		#--- name
		self.edit_name = QLineEdit(storage.pnode.name)

		# #--- type
		# self.edit_type = QComboBox()
		# self.edit_type.addItems(self.types)


		form.addRow("Название", self.edit_name)
		# form.addRow("Тип", self.edit_type)



		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)

		btn_close = QPushButton("Закрыть")
		btn_close.clicked.connect(self.close)

		btn_save = QPushButton("Сохранить")
		btn_save.clicked.connect(self.__save)

		controls.addWidget(btn_save)
		controls.addStretch()
		controls.addWidget(btn_close)


		#
		#
		# #--- load current data
		# self.__load_data()






	#
	# def __load_data(self):
	# 	ntype = self.node.ntype
	# 	index = self.types.index(ntype)
	# 	self.edit_type.setCurrentIndex(index)



	def __save(self):
		"""обновление ноды"""


		#--- get data
		name = self.edit_name.text()


		# #--- тип
		# index = self.edit_type.currentIndex()
		# node_type = self.types[index]

		#--- update node data
		storage.pnode.name = name
		# self.node.ntype = node_type


		#--- update project file
		storage.update_project_file()



		self.close()


















if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	import sys
	# from PyQt5.QtWidgets import QStyleFactory
	# from PyQt5.QtCore import QStyleFactory

	app = QApplication(sys.argv)

	# app.setStyle(QStyleFactory.create("fusion"))

	modal = ModalEditName()
	# main_win.DEBUG = True
	# main_win.start_net()
	modal.show()

	app.exec_()
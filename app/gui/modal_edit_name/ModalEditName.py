#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox, QTextEdit, QFormLayout, QLineEdit
from PyQt5.QtGui import QFont


from app.storage import smanager
# from .. import events






class ModalEditName(QDialog):
	def __init__(self, parent=None):
		super(ModalEditName, self).__init__(parent)

		self.main_layout 	= QVBoxLayout(self)

		
		self.storage 		= smanager.get_storage()				# тек. хранилище
		self.node 			= self.storage.get_current_node()		# тек. нода
		self.types 			= self.storage.get_node_types()			# типы контента
		
		
		self.__make_gui()
		self.__load_data()


	def __make_gui(self):
		
		


		form = QFormLayout()
		self.main_layout.addLayout(form)

		#--- name
		self.edit_name = QLineEdit(self.node.name)

		#--- type
		self.edit_type = QComboBox()
		self.edit_type.addItems(self.types)


		form.addRow("Название", self.edit_name)
		form.addRow("Тип", self.edit_type)



		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)

		btn_close = QPushButton("Close")
		btn_close.clicked.connect(self.close)

		btn_save = QPushButton("Save")
		btn_save.clicked.connect(self.__save)

		controls.addWidget(btn_save)
		controls.addStretch()
		controls.addWidget(btn_close)


	def __load_data(self):
		ntype = self.node.meta.ntype
		index = self.types.index(ntype)
		self.edit_type.setCurrentIndex(index)



	def __save(self):
		"""обновление ноды"""


		#--- get data
		name = self.edit_name.text()


		#--- тип
		index = self.edit_type.currentIndex()
		node_type = self.types[index]

		#--- update node data
		self.node.meta.ntype = node_type
		self.node.update_node_name(name)

		#--- update project data
		self.storage.project.set_node_name(self.node.uuid, name)
		self.storage.project.write_file()

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
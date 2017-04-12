#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QTextEdit, QFormLayout, QLineEdit, QComboBox
from PyQt5.QtGui import QFont



from app.storage import smanager








class ModalCreate(QDialog):
	def __init__(self, parent_node_uuid=None, parent=None):
		super(ModalCreate, self).__init__(parent)

		self.setWindowTitle("Создание новой записи")
		self.storage 		= smanager.get_storage()
		
		if parent_node_uuid is None:
			self.parent_node_uuid = self.storage.pmanager.get_root_node().uuid
		else:
			self.parent_node_uuid 	= parent_node_uuid


		self.types = self.storage.get_node_types()


		self.main_layout = QVBoxLayout(self)
		self.__make_gui()






	def __make_gui(self):
		

		# label_root_name = QLabel("Родитель: {}".format(self.parent_node.name))
		# self.main_layout.addWidget(label_root_name)


		#--- edit
		input_layout = QVBoxLayout()
		self.main_layout.addLayout(input_layout)

		form = QFormLayout()
		input_layout.addLayout(form)


		self.edit_name = QLineEdit()

		self.edit_type = QComboBox()
		self.edit_type.addItems(self.types)




		form.addRow("Название", self.edit_name)
		form.addRow("Тип", self.edit_type)



		self.edit_text = QTextEdit()
		input_layout.addWidget(self.edit_text)
		


		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)

		btn_close = QPushButton("Закрыть")
		btn_close.clicked.connect(self.close)

		btn_create = QPushButton("Создать")
		btn_create.clicked.connect(self.__create)

		controls.addStretch()
		controls.addWidget(btn_create)
		controls.addWidget(btn_close)




	def __create(self):
		"""создание новой ноды"""

		#--- название
		name = self.edit_name.text()

		#--- тип
		index = self.edit_type.currentIndex()
		node_type = self.types[index]


		#--- содержимое
		text = self.edit_text.toPlainText()



		self.storage.create_node(self.parent_node_uuid, name, node_type, text)

		# #--- создание дефолтных записей ноды
		# node = self.storage.create_node(self.parent_node, name)
		#
		# #--- обновление данных
		# node.meta.ntype = node_type
		# node.update_page_text(text)

		self.close()














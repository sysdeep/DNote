#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QListWidget, QTextEdit, QFormLayout, QComboBox, QListWidgetItem
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


from app.storage import get_storage
from app.rc import get_icon_path, ICON_PACKS, get_list_icons_pack
from .. import events






class ModalFiles(QDialog):
	def __init__(self, node, parent=None):
		super(ModalFiles, self).__init__(parent)
		self.main_layout = QVBoxLayout(self)
		
		self.node 	= node

		
		self.clist 	= None

		
		self.__make_gui()

		self.__load_files()


	def __make_gui(self):


		self.clist = QListWidget()
		# self.clist.itemClicked.connect(self.__set_icon)

		self.main_layout.addWidget(self.clist)


		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)

		btn_close = QPushButton("Close")
		btn_close.clicked.connect(self.close)

		# btn_create = QPushButton("ok")
		# btn_create.clicked.connect(self.__create)

		# controls.addWidget(btn_create)
		controls.addStretch()
		controls.addWidget(btn_close)





	def __load_files(self):
		# self.current_ipack = ICON_PACKS[index]

		files = self.node.files.files

		# self.clist.clear()
		for f in files:

			# icon = QIcon(get_icon_path(self.current_ipack, f))
			# item = QListWidgetItem(icon, f)
			item = QListWidgetItem(f)
			# item.setData(Qt.UserRole+1, f)
			self.clist.addItem(item)






	# def __set_icon(self, list_item):

	# 	self.current_icon = list_item.data(Qt.UserRole+1)
	# 	# print(self.current_icon)



	# def __create(self):
	# 	""""""
		
	# 	events.selected_icon(self.current_ipack, self.current_icon)

	# 	self.close()

	

















if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	import sys
	# from PyQt5.QtWidgets import QStyleFactory
	# from PyQt5.QtCore import QStyleFactory

	app = QApplication(sys.argv)

	# app.setStyle(QStyleFactory.create("fusion"))

	modal = ModalFiles()
	# main_win.DEBUG = True
	# main_win.start_net()
	modal.show()

	app.exec_()
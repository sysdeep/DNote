#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QListWidget, QTextEdit, QFormLayout, QComboBox, QListWidgetItem
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


from app.storage import get_storage
from app.rc import get_icon_path, ICON_PACKS, get_list_icons_pack
from ..utils.icons import qicon, dicon
from .. import events






class ModalIcons(QDialog):
	def __init__(self, parent=None):
		super(ModalIcons, self).__init__(parent)

		self.setWindowTitle("Выбор иконки")
		self.main_layout = QVBoxLayout(self)
		self.setMinimumWidth(400)
		self.setMinimumHeight(400)


		self.cbox 	= None					# спсиок пакетов
		self.clist 	= None					# список иконок в пакете

		self.current_ipack 	= ""
		self.current_icon	= ""
		
		self.__make_gui()

		self.__update_pack(0)


	def __make_gui(self):

		#--- pack select
		self.cbox = QComboBox()
		self.cbox.addItems(ICON_PACKS)
		self.cbox.currentIndexChanged.connect(self.__update_pack)		# event

		self.main_layout.addWidget(self.cbox)


		#--- icon select
		self.clist = QListWidget()
		self.clist.itemClicked.connect(self.__on_select)
		self.clist.itemDoubleClicked.connect(self.__on_select_set)

		self.main_layout.addWidget(self.clist)


		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)

		btn_close = QPushButton("Закрыть")
		btn_close.clicked.connect(self.close)
		btn_close.setIcon(dicon("close"))

		self.btn_select = QPushButton("Выбрать")
		self.btn_select.clicked.connect(self.__on_apply_select)
		self.btn_select.setIcon(dicon("ok"))
		self.btn_select.setDisabled(True)

		controls.addStretch()
		controls.addWidget(self.btn_select)
		controls.addWidget(btn_close)





	def __update_pack(self, index):
		"""обновить список иконок для выбранного набора"""
		self.current_ipack = ICON_PACKS[index]

		files = get_list_icons_pack(self.current_ipack)

		self.clist.clear()
		for f in files:

			icon = QIcon(get_icon_path(self.current_ipack, f))
			item = QListWidgetItem(icon, f)
			item.setData(Qt.UserRole+1, f)
			self.clist.addItem(item)

		#--- отключаем кнопку
		self.btn_select.setDisabled(True)






	def __on_select(self, list_item):
		"""выбор иконки"""
		self.current_icon = list_item.data(Qt.UserRole+1)

		#--- оживляем кнопку
		if not self.btn_select.isEnabled():
			self.btn_select.setDisabled(False)
		


	def __on_select_set(self, list_item):
		"""выбор и применение иконки"""
		self.current_icon = list_item.data(Qt.UserRole+1)
		self.__on_apply_select()


	def __on_apply_select(self):
		"""применение иконки"""
		
		events.selected_icon(self.current_ipack, self.current_icon)

		self.close()

	

















if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	import sys
	# from PyQt5.QtWidgets import QStyleFactory
	# from PyQt5.QtCore import QStyleFactory

	app = QApplication(sys.argv)

	# app.setStyle(QStyleFactory.create("fusion"))

	modal = ModalIcons()
	# main_win.DEBUG = True
	# main_win.start_net()
	modal.show()

	app.exec_()
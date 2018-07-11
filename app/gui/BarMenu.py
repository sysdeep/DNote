#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction, QFileDialog
# from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

# from app.rc import get_icon_path
from . import actions


from . import events, qicon
from .modals.CreateNotebook import CreateNotebook
from .modals.OpenNotebook import OpenNotebook

# from .ModalScan import ModalScan

# from .icons import qicon
# from app.logic import get_project

# from .modals import show_modal_once, Settings, ControlCenter, ObjectsEmu, About, ProjectPackages
# from .modals.FaenzaIcons import FaenzaIcons
# from .modals.Users import Users
# from .modals.CalibrationFlags import CalibrationFlags


# from .modals.console import PyConsoleModal


class BarMenu(object):
	def __init__(self, parent):
		self.parent 	= parent				# MainWindow
		# self.project 	= get_project()


		self.menu 		= self.parent.menuBar()
		self.toolbar 	= self.parent.addToolBar("Main")

		#--- file -------------------------------------------------------------
		file_menu = self.menu.addMenu("Файл")



		#--- create new notebook
		file_create_new_notebook = QAction("Создать новый блокнот", self.parent)
		file_create_new_notebook.setIcon(qicon("actions", "document_new.png"))
		file_create_new_notebook.triggered.connect(lambda: self.__file_create_new_notebook())

		file_menu.addAction(file_create_new_notebook)
		self.toolbar.addAction(file_create_new_notebook)



		#--- open notebook
		file_open_notebook = QAction("Открыть блокнот", self.parent)
		file_open_notebook.setIcon(qicon("actions", "document_open.png"))
		file_open_notebook.triggered.connect(lambda: self.__file_open_notebook())

		file_menu.addAction(file_open_notebook)
		self.toolbar.addAction(file_open_notebook)


		#--- create root item
		file_create_root_item_action = QAction("Создать корневую запись", self.parent)
		file_create_root_item_action.setIcon(qicon("filesystems", "folder_blue.png"))
		file_create_root_item_action.triggered.connect(lambda: self.__file_create_root_item_action())

		file_menu.addAction(file_create_root_item_action)
		self.toolbar.addAction(file_create_root_item_action)


		#--- exit
		file_exit_action = QAction("&Закрыть", self.parent)
		file_exit_action.setShortcut("Ctrl+Q")
		file_exit_action.setStatusTip("Закрыть приложение")
		file_exit_action.setIcon(qicon("actions", "system_shutdown.png"))
		file_exit_action.triggered.connect(self.parent.exit)
		file_menu.addAction(file_exit_action)



	def __file_create_root_item_action(self):
		# events.show_modal_create_node(parent_node=None)
		actions.show_modal_create_node(None)

	
	def __file_create_new_notebook(self):
		# modal = CreateNotebook(self.parent)
		# modal.show()
		print("BarMenu - create - not implement!!!!!")


	def __file_open_notebook(self):
		# modal = OpenNotebook(self.parent)
		# modal.show()
		print("BarMenu - open - not implement!!!!!")

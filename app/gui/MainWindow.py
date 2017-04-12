#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFontDatabase
# from PyQt5.QtCore import QTimer, pyqtSignal


from app import log

from .MainFrame import MainFrame

# from app.logic import get_tree, load_tree, load_tree_demo
# from .Controller import Controller


# from .utils.WalkerDispatcher import WalkerDispatcher
# from ..logic import get_server, get_project
# from .modals import LoginWindow
# from ..storage import ulog
# from app.rc import get_font_path
from .Controller import Controller
from .BarMenu import BarMenu
# from .SystemTray import SystemTray
# from . import events
from . import qicon
# from app.logic import twalker
# from app.rc import DIR_SCAN

from . import actions


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		log.debug("инициализация главного окна программы")
		self.TERMINATED = False
		# self.mnemo 		= None
		# self.DEBUG 		= False
		# self.DEBUG_SHOW_LOGIN = False


		self.max_x = 800
		self.max_y = 600

		self.setWindowTitle("DCat")
		self.setMinimumWidth(self.max_x)							# min width
		self.setMinimumHeight(self.max_y)


		# self.server 	= get_server()
		# self.project 	= get_project()
		# self.client 	= None


		#--- add fonts
		# QFontDatabase.addApplicationFont(get_font_path("Play-Bold.ttf"))
		# QFontDatabase.addApplicationFont(get_font_path("roboto", "RobotoRegular.ttf"))
		# QFontDatabase.addApplicationFont(get_font_path("roboto", "RobotoMono-Regular.ttf"))


		actions.set_parent(self)
		self.controller = Controller(parent=self)


		#
		# self.walker_dispatcher = WalkerDispatcher(self)
		# self.walker_dispatcher.msg.connect(lambda x: print(x))
		#
		#
		#
		# self.walker_dispatcher.start()




		self.__init_gui()




		#--- system tray
		# tray = SystemTray(self)
		# tray.show()


		






	def __init_gui(self):

		# self.setGeometry(300, 300, 300, 300)

		#--- main menu
		menu = BarMenu(self)

		#--- mnemo bar
		self.__make_main()

		#--- status bar
		self.__make_status_bar()



		self.show()



	


	def __make_main(self):

		#--- central_widget
		central_widget = QWidget(self)
		# central_widget.setContentsMargins(0, 0, 0, 0)
		self.setCentralWidget(central_widget)
		# self.setContentsMargins(0, 0, 0, 0)				# mainwindow margins

		

		#--- central_box
		# central_box = QVBoxLayout()
		# central_widget.setLayout(central_box)
		central_box = QVBoxLayout(central_widget)
		# central_box.setContentsMargins(0, 0, 0, 0)




		main_frame = MainFrame()
		central_box.addWidget(main_frame)


	

		#--- controls
		controls_bar = QHBoxLayout()
		central_box.addLayout(controls_bar)


		btn_exit = QPushButton("Выход")
		btn_exit.setIcon(qicon("actions", "system_shutdown.png"))
		btn_exit.clicked.connect(self.exit)

		controls_bar.addStretch()
		controls_bar.addWidget(btn_exit)

	





	def __make_status_bar(self):
		self.statusBar().showMessage('Ready')






	def exit(self):
		log.info("запрос на закрытие приложения")
		self.close()



	def closeEvent(self, QCloseEvent):
		"""перехват зактытия окна - предварительные завершения для объектов"""

		log.info("закрытие приложения - останавливаем процессы")

		log.info("закрытие приложения - выходим")
		QCloseEvent.accept()









if __name__ == "__main__":

	# from PyQt5.QtWidgets import QStyleFactory
	# from PyQt5.QtCore import QStyleFactory

	app = QApplication(sys.argv)

	# app.setStyle(QStyleFactory.create("fusion"))

	main_win = MainWindow()
	# main_win.DEBUG = True
	# main_win.start_net()

	app.exec_()


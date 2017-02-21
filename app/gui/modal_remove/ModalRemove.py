#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QTextEdit, QFormLayout, QLineEdit
from PyQt5.QtGui import QFont


from app.storage import smanager
from .. import events






class ModalRemove(QDialog):
	def __init__(self, node_uuid, parent=None):
		super(ModalRemove, self).__init__(parent)

		self.main_layout 	= QVBoxLayout(self)

		self.node_uuid 		= node_uuid
		
		
		self.node_items 	= ("ntype", "uuid", "name", "ctime", "mtime", "path")
		self.node_labels 	= {}
		
		self.__make_gui()
		self.__load_data()


	def __make_gui(self):
		
		
		info_box = QGridLayout()
		self.main_layout.addLayout(info_box)

		for index, item in enumerate(self.node_items):
			info_box.addWidget(QLabel(item), index, 0)

			label = QLabel()
			info_box.addWidget(label, index, 1)
			self.node_labels[item] = label


		#--- controls
		controls = QHBoxLayout()
		self.main_layout.addLayout(controls)

		btn_close = QPushButton("Close")
		btn_close.clicked.connect(self.close)

		btn_remove = QPushButton("Remove")
		btn_remove.clicked.connect(self.__remove)

		controls.addWidget(btn_remove)
		controls.addStretch()
		controls.addWidget(btn_close)



	def __load_data(self):

		node = smanager.storage.get_node(self.node_uuid)
		self.node_labels["ntype"].setText(node.meta.ntype)
		self.node_labels["uuid"].setText(node.meta.uuid)
		self.node_labels["name"].setText(node.meta.name)
		self.node_labels["path"].setText(node.meta.path)
		self.node_labels["ctime"].setText(node.meta.get_ctime())
		self.node_labels["mtime"].setText(node.meta.get_mtime())



	def __remove(self):
		"""удаление ноды"""

		smanager.storage.remove_node(self.node_uuid)
		
		self.close()


















if __name__ == "__main__":
	from PyQt5.QtWidgets import QApplication
	import sys
	# from PyQt5.QtWidgets import QStyleFactory
	# from PyQt5.QtCore import QStyleFactory

	app = QApplication(sys.argv)

	# app.setStyle(QStyleFactory.create("fusion"))

	modal = ModalRemove()
	# main_win.DEBUG = True
	# main_win.start_net()
	modal.show()

	app.exec_()
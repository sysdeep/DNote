#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time, signal, sys
from app import log

from PyQt5.QtWidgets import QApplication

from .gui.MainWindow import MainWindow







class App(object):
	def __init__(self):
		log.info("инициализация приложения")


		self.qtapp = QApplication(sys.argv)




		signal.signal(signal.SIGINT, self.__signal_handler)		# обработка Ctrl+C




	def __signal_handler(self, signum, frame):
		"""обработчик сигнала завершения от системы"""
		log.info("перехвачен сигнал SIGINT(Ctrl+C)")
		log.info("запрос на выход из cmd")
		# self.stop()

		self.qtapp.exit(0)





	def start(self):
		"""запуск приложения"""
		log.info("запуск приложения")

		self.main_window = MainWindow()
		# self.main_window.start_net()
		self.qtapp.exec_()

		#
		# #--- цикл для работы потоков и основного приложения
		# while not self.TERMINATED:
		# 	print("app.loop")
		# 	time.sleep(2)
		#
		#
		# #--- по окончании основного потока - выходим
		# log.info("приложение остановленно")
		# sys.exit(0)




	# def stop(self):
	# 	"""остановка приложения"""
	# 	log.info("запрос на остановку приложения")
		# self.worker_job.stop()									# сообщаем job о прекращении работы
		# self.worker_job.join()									# дожидаемся его прекоащения

		# self.TERMINATED = True									# взводим флаг прекращения







if __name__ == "__main__":

	app = App()
	app.start()
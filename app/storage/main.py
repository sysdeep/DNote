#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import log

from .Controller import Controller



DATA = {
	"controller": None
}






def set_up():
	log.info("set up")
	controller = Controller()
	controller.load_project_default()
	DATA["controller"] = controller




def get_controller():
	return DATA["controller"]


def get_tree():
	controller = get_controller()
	tree = controller.project.tree
	return tree







def create_demo():
	controller = Controller()
	controller.load_project_default()
	controller.create_top_node("test_1")
	controller.create_top_node("test_2")
	controller.create_top_node("test_3")



if __name__ == '__main__':
	set_up()
	# print(DATA)

	# print(get_tree())

	# create_demo()
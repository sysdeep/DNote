#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from app import log
from app.rc import DIR_PROJECT
from .Storage import Storage



DATA = {
	"storage": None
}






def set_up():
	log.info("set up")
	storage = Storage()

	#--- for development only
	storage.load_project(DIR_PROJECT)
	#--- for development only
	
	DATA["storage"] = storage
	return storage




def get_storage():
	storage = DATA.get("storage")
	if storage is None:
		storage = set_up()
	
	return storage


	# return DATA["storage"]







def load_default_project():
	storage = get_storage()
	storage.load_project(DIR_PROJECT)





# def get_tree():
# 	controller = get_controller()
# 	tree = controller.project.tree
# 	return tree







# def create_demo():
# 	controller = Controller()
# 	controller.load_project_default()
# 	controller.create_top_node("test_1")
# 	controller.create_top_node("test_2")
# 	controller.create_top_node("test_3")



if __name__ == '__main__':
	pass
	# set_up()
	# print(DATA)

	# print(get_tree())

	# create_demo()
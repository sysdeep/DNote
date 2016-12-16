#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ресурсы приложения"""

import os

#--- dirs
DIR_SELF 		= os.path.dirname(os.path.abspath(__file__))
DIR_MEDIA 		= os.path.normpath(os.path.join(DIR_SELF, "..", "media"))
DIR_ICONS		= os.path.join(DIR_MEDIA, "icons")
DIR_UI_ICONS 	= os.path.join(DIR_MEDIA, "ui_icons")




class Shared:
	current_project_directory	= ""









#--- for tests in progress

DIR_PROJECT = os.path.normpath(os.path.join(DIR_SELF, "..", "..", "sdir"))
DIR_PROJECT_NODES = os.path.join(DIR_PROJECT, "nodes")
FILE_PROJECT	= os.path.join(DIR_PROJECT, "project.json")
# FILE_JSON = os.path.normpath(os.path.join(DIR_SELF, "..", "..", "sdir.json"))
DIR_TEST_NODE = os.path.join(DIR_PROJECT_NODES, "28bd6ab8-c116-11e6-b160-e0cb4e1afb73")


# QUE_WALKER = Queue()



ICON_PACKS = ("Elementary", "Flat", "Universal")

def get_icon_path(*icon_subpath):
	return os.path.join(DIR_ICONS, *icon_subpath)



def get_list_icons_pack(icons_pack):
	icons_path = os.path.join(DIR_ICONS, icons_pack)
	files = os.listdir(icons_path)
	return files



def get_ui_icon_path(*icon_subpath):
	return os.path.join(DIR_UI_ICONS, *icon_subpath)

# def set_scan_dir(new_path):
# 	global DIR_SCAN
# 	DIR_SCAN = new_path

# def get_scan_dir():
# 	global DIR_SCAN
# 	return DIR_SCAN
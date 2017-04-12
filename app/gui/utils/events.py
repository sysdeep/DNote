#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	система обмена событиями в GUI
"""

from app.lib import EventEmitter

emitter = EventEmitter()


def on(event_name, cb):
	"""подписаться на события"""
	emitter.eon(event_name, cb)







# def show_modal_create_node(parent_node=None):
# 	"""запрос на создание новой ноды"""
# 	emitter.emit("show_modal_create_node", parent_node)

# def show_remove_node(node_uuid):
# 	"""запрос на удаление ноды"""
# 	emitter.emit("show_remove_node", node_uuid)

# def show_edit_name(node_uuid=None):
# 	"""запрос на изменение имени ноды"""
# 	emitter.emit("show_edit_name", node_uuid)

# def show_edit_icon(node_uuid):
# 	"""запрос на изменение иконки ноды"""
# 	emitter.emit("show_edit_icon", node_uuid)
#
#
# def show_edit_files(node):
# 	"""запрос на изменение иконки ноды"""
# 	emitter.emit("show_edit_files", node)
#
# def show_current_node_info():
# 	"""запрос на отображение модала с информацией о тек. ноде"""
# 	emitter.emit("show_current_node_info")
#



#
#
#
# def update_tree():
# 	emitter.emit("update_tree")
#
#
# def update_current_node():
# 	emitter.emit("update_current_node")
#
#
#
# def selected_icon(ipack, icon):
# 	emitter.emit("selected_icon", ipack, icon)
#












# def set_scan_path(path):
# 	emitter.emit("set_scan_path", path)



# def start_scan():
# 	emitter.emit("start_scan")


# def set_save_file(path):
# 	emitter.emit("set_save_file", path)


# def set_open_file(path):
# 	emitter.emit("set_open_file", path)




# def update_tree():
# 	emitter.emit("update_tree")


#
#
# def show_tray_message(text, title="", state="info"):
# 	"""
# 		отобразить сообщение из системного трея
#
# 		on:
# 			SystemTray.py
# 	"""
# 	emitter.emit("show_tray_message", title, text, state)
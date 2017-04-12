#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .modal_edit_name.ModalEditName import ModalEditName
from .modal_create.ModalCreate import ModalCreate
from .modal_remove.ModalRemove import ModalRemove
# from .modals.ModalIcons import ModalIcons

DATA = {
	"parent": None
}


def set_parent(parent):
	DATA["parent"] = parent


def get_parent():
	return DATA["parent"]





def show_modal_edit_name():
	"""отображение модального окна изменения названия"""
	modal = ModalEditName(parent=get_parent())
	modal.show()


def show_modal_create_node(parent_node_uuid=None):
	"""отображение модального окна создания новой записи"""
	modal = ModalCreate(parent_node_uuid, parent=get_parent())
	modal.show()


def show_modal_remove_node():
	"""отображение модального окна удаления записи"""
	modal = ModalRemove(parent=get_parent())
	modal.show()


# def show_modal_icons():
# 	modal = ModalIcons(parent=get_parent())
# 	modal.show()


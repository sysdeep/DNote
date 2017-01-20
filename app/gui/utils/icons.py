#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtGui import QIcon
from app.rc import get_ui_icon_path

# def qicon(file_name):
#     return QIcon(get_icon_path(file_name))


def qicon(*section_icon):
    return QIcon(get_ui_icon_path(*section_icon))




#--- соответствие иконок стандартным методам
# QFDEF = {
# 	"ok"		: "dialog-ok.png",
# 	"cancel"	: "process-stop.png",
# 	"close"		: "window-close.png",
# 	"refresh"	: "view-refresh.png",
# }

# # "actions", "system_shutdown.png"

# def dicon(name):
# 	"""получить иконку по даданному соответствию"""
# 	if name in QFDEF:
# 		return qficon(QFDEF[name])
# 	else:
# 		return qficon(name)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from PyQt5.QtGui import QIcon
from app.rc import get_ui_icon_path

# def qicon(file_name):
#     return QIcon(get_icon_path(file_name))


def qicon(*section_icon):
    return QIcon(get_ui_icon_path(*section_icon))
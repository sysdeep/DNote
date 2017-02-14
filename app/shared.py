#!/usr/bin/env python3
# -*- coding: utf-8 -*-



DATA = {
	"current_node": None
}




def get(key):
	return DATA.get(key)


def set(key, value):
	DATA[key] = value



def get_current_node():
	return DATA["current_node"]

def set_current_node(node):
	DATA["current_node"] = node
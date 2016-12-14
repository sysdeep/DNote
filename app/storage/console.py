#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import get_storage, load_default_project







def test1():
	storage = get_storage()
	# load_default_project()

	storage.project.tree.print_nodes()









if __name__ == '__main__':



	test1()
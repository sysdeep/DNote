#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .NSTree import NSTree

tree = NSTree()

tree.print_nodes()

tree.create_node("0", "1", "1")
tree.create_node("1", "11", "11")
tree.create_node("1", "12", "12")



tree.create_node("0", "2", "2")
tree.create_node("2", "21", "21")
tree.create_node("2", "22", "22")
tree.create_node("2", "23", "23")
tree.create_node("23", "231", "231")


tree.print_nodes()




print("---------------------------")
# tree.move_node_up("2")
tree.move_node_down("22")
tree.print_nodes()
print("---------------------------")
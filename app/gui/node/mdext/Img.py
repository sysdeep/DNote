#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
	2017.09.26 - попытка внедрить свой обработчик - только тесты
"""
from vendors import markdown
from vendors.markdown import Extension
from vendors.markdown import blockprocessors
from vendors.markdown import preprocessors

# class CImgProcessor(blockprocessors.BlockProcessor):
class CImgProcessor(preprocessors.Preprocessor):
	def __init__(self, parser):
		self.border = False
		self.separator = ''
		super(CImgProcessor, self).__init__(parser)

	# def test(self, parent, block):
	# 	pass
	# 	print(block)
	#
	#
	# 	# if block
	# 	# header = [row.strip() for row in block.split('\n')[0:2]]
	# 	# print(header)
	# 	return False

	def run(self, lines):
		print("run ext")
		print(lines)

		new_lines = []
		for line in lines:
			new_lines.append(line)

		return new_lines






class CImgExtension(Extension):
	""" Add tables to Markdown. """

	def extendMarkdown(self, md, md_globals):
		""" Add an instance of TableProcessor to BlockParser. """
		pass
		# if '|' not in md.ESCAPED_CHARS:
		#     md.ESCAPED_CHARS.append('|')
		# md.parser.blockprocessors.add('cimg', CImgProcessor(md.parser), '<hashheader')
		md.preprocessors.add('cimg', CImgProcessor(md), '<reference')


def makeExtension(*args, **kwargs):
	return CImgExtension(*args, **kwargs)
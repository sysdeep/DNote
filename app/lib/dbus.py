#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from .EventEmitter import EventEmitter


DATA = {
	"emitter"	: EventEmitter()
}


#--- events consts
STORAGE_OPENED = "storage_opened"				# args: storage_path(string)
STORAGE_OPEN = "storage_open"					# open storage - args: storage_path(string)

def eon(event_name, f):
	DATA["emitter"].eon(event_name, f)

def eoff(event_name, f):
	DATA["emitter"].eoff(event_name, f)

def emit(event_name, *args, **kwargs):
	DATA["emitter"].emit(event_name, *args, **kwargs)


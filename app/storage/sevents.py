#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.lib.EventEmitter import EventEmitter

__event_emitter = EventEmitter()


def eon(event, cb):
	__event_emitter.eon(event, cb)







#--- manager ------------------------------------------------------------------
def storage_opened():
	__event_emitter.emit("storage_opened")

def storage_created():
	__event_emitter.emit("storage_created")
#--- manager ------------------------------------------------------------------



#--- storage ------------------------------------------------------------------
def node_selected():
	__event_emitter.emit("node_selected")

def node_updated():
	__event_emitter.emit("node_updated")
#--- storage ------------------------------------------------------------------
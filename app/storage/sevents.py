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


#--- project ------------------------------------------------------------------
def project_loaded():
	__event_emitter.emit("project_loaded")

def project_node_created():
	__event_emitter.emit("project_node_created")

def project_node_removed():
	__event_emitter.emit("project_node_removed")

def project_updated():
	__event_emitter.emit("project_updated")
#--- project ------------------------------------------------------------------

#--- storage ------------------------------------------------------------------
def node_selected():
	__event_emitter.emit("node_selected")

def node_updated():
	__event_emitter.emit("node_updated")

def node_created():
	__event_emitter.emit("node_created")

def node_removed():
	__event_emitter.emit("node_removed")
#--- storage ------------------------------------------------------------------
import pygame
from pygame.locals import *
from etoffiutils import true, false

class Backend:
	def isEventPending (self):
		return (pygame.event.peek () != None)
#	def pendingEvent (self):
#		return pygame.event.peek ()
	def getEvent (self):
		return pygame.event.get ()[0]
	def defaultEventHandler (self, obj, evt):
		rv=false
		if event.type == QUIT:
			rv=true
			self.quit ()
		elif event.type == KEYDOWN:
			fireToEx ('expose onkeydown', [('keycode', event.key)], obj, obj)
			rv=true
		return rv
		

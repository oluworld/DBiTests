from Window import *

class AttrHandledWindow(Window):
	def handle(self, evt):
		r = 'handle_'+evt.msg.replace(' ', '_')
		if hasattr(self, r):
			rr = getattr(self, r)
			return rr(evt)
		return None

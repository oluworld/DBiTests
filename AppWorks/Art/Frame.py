from Window import *

class Frame(Window):
	def _reset(self):
		Window._reset(self)
		self['dbiroot']='~/Interface'

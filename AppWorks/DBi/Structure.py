FOR_ENUM = 1
FOR_GET  = 0
EnumFlat = 0
EnumRecursive = 1

class DBiHandlerAddEvent:
	""" fired when a DBiHandler adds a value """
	def __init__ (self, value, handler):
		self.value = value
		self.handler = handler
class DBiServerAddEvent:
	""" fired when the DBiServer recieves a HandlerAddEvent.
		prolly should remain internal to DBiServer.
	"""
	def __init__ (self, line, line_path, server):
		self.value = line
		self.value_path = line_path
		self.server = server

class DBiServerEnumListener:
	def actionPerformed (self, evt):
		self.list.append (evt.value)
##		print "self.list =", self.list
	def __init__ (self):
		self.list = []
	def getResult (self):
		return self.list
class DBiServerEnumPrinter:
	def actionPerformed (self, evt):
		print "$$", evt.line
	def __init__ (self):
		pass
	def getResult (self):
		pass

class DBiHandlerListener:
	def actionPerformed (self, evt):
		""" called when a DBiHandler adds a value """
##		print "** adding ", evt.value
		self.server.add (evt.value)
	def __init__ (self, server):
		self.server = server

class DBiHandlerGetValueListener:
	def actionPerformed (self, evt):
		""" called when a DBiHandler adds a value """
		if evt.value.path == self.look:
##			print evt.value
			self.res = evt.value
	def __init__ (self, look):
		self.look = look
		self.res = None
	def getResult (self):
		return self.res


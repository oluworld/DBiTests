# path name host type perms atime mtime ctime size
class Desc:
	def __init__ (self, filename=None, ctx=None):
		self.fullname 	= filename
		self.host     	= None
		self.type 		= None
		self.perms 		= None
		self.atime 		= None
		self.mtime 		= None
		self.ctime 		= None
		self.size		= 0
		self.ctx		= ctx
	def set (self, host, type, perms, size = 0, ctx = None):
		self.host     	= host
		self.type 		= type
		self.perms 		= perms
		self.size		= size
		self.ctx		= ctx
	def setTimes (self, mtime, atime, ctime):
		self.atime 		= atime
		self.mtime 		= mtime
		self.ctime 		= ctime
	def is_dir (self):
		return self.type.is_dir ()
	def getFullName  (self):
		rv = self.fullname
		return rv
	def getType (self):
		if self.type == None:
			self.makeType ()
		print "host is:",self.host 
		return self.type
	def makeType (self):
		pass
	def official (self, ctx=None):
		""" usually self will be discarded since it would only contain the name
		    and maybe a context """
		if ctx==None:
			ctx=self.ctx
		off = ctx.get_shared_file_server ().stat (self.getFullName (), ctx)
		return off
		
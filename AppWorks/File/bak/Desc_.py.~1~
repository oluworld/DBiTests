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
		if ctx==None:
			ctx=self.ctx
		off = ctx.get_shared_file_server ().stat (self.getFullName (), ctx)
		return off
		
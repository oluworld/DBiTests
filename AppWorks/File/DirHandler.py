#
#
#

class NotImplementedException(Exception):
	pass

# AppWorks::File::iDirHandler
class iDirHandler:
	def getClassType(self):
		return 'AppClass.DirHandler'
		
	def getRoot(self):
		return self.root
		
	def canOpen(self, path, perm):
		""" path:File.Path, perm:File.Perms -> bool"""
		raise NotImplementedException()
		
	def enumerate(self, spec):
		""" spec:String -> List<File.Desc> """
		raise NotImplementedException()
		
	def enumerateFirstByName(self, spec):
		""" spec:File.Name -> File.Desc """
		raise NotImplementedException()
	
	def insert(self, desc):
		""" -> bool """
		raise NotImplementedException()
		
	def unlink(self, desc):
		""" -> bool """
		raise NotImplementedException()
		
	def open(self, desc, perms, flags):
		""" -> File.Handle """
		raise NotImplementedException()
		
	def reopen(self, handle, perms, flags):
		""" -> File.Handle """
		raise NotImplementedException()
		
	def close(self, handle):
		""" -> bool """
		raise NotImplementedException()
		
	def write(self, handle, data, size):
		""" File.Handle ByteStream int -> int """
		raise NotImplementedException()
		
	def read(self, handle, size):
		""" File.Handle int -> ByteStream """
		raise NotImplementedException()
	
	def seek(self, amt, dir, pos):
		""" amt:uint dir:(*forward*, backward) pos:(beg, end, *cur*) """
		raise NotImplementedException()
		
	def setParams(self, handle, params):
		""" handle:File.Handle params:?a """
		raise NotImplementedException()
		
	def handle(self, evt):
		raise NotImplementedException()

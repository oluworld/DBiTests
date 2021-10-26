import AppWorks.Util.DBiValue
from etoffiutils import true, false, nequals
from RCDBiHandler import RCDBiHandler

class errNotFound(Exception):
	pass
class AwxDBiServer:
	DBIROOT = 'q:/DBi/'
	EnumFlat = 0
	EnumRecursive = 1
	FOR_ENUM = 1
	FOR_GET  = 0
	
	def enum(self, topkey, root='~/', kind=EnumFlat):
##		print '%% enum ( %s %s ) ' % (topkey, root)
		top = self.translatePath(topkey, root)
##		print '%% enum ( %s %s ) ((%s))' % (topkey, root, top)
		self.lock()
		r = self.lockedlist
		for each in self.handlers:
			if each.canOpen(top, AwxDBiServer.FOR_ENUM):
				each.Begin(top)
				break
		self.unlock()
		return r

	def get(self, path, root):
##		print 99, path, root
		search = self.translatePath(path, root)
##		print 100, search
		if self.entries.has_key(search):
			return self.entries[search]
		look = self.__lookup(search)
		if not look:
			print search
			raise errNotFound() ## TODO:
		self.entries[search] = look
		return look
	def getStr(self, path, root):
		rv = self.get(path, root).getStr()
		return rv
	def getStrOrNil(self, path, root):
		try:
			return self.getStr(path, root)
		except errNotFound:
			return None
	def __lookup(self, path):
		rv   = None
#		path = self.translatePath(path_, '~/')
		AWX_DBI_NEWACTION = false
		if AWX_DBI_NEWACTION == true:
			b = progressiveParse(path, '/')
			for parsePath in b:
				if fileSystem.exists(parsePath):
					h = self.handlerForPath(parsePath)
					if h:
						rv = h.getValue(path)
					else:
						self.log('No handler for path %s' % parsePath)
		else:
			for iterdata in self.handlers:
##				print 'LPO',iterdata
				if iterdata.canOpen(path, AwxDBiServer.FOR_GET):
					## place iterdata at top of handler stack
##					print self.entries
					rv = iterdata.getValue(path)
			## throws an exception in AbxLib (errNotFound)
##		print '%% lookup (%s) -> %s' % (path, rv)
		return rv
	def translatePath(self, path, root):
##		print 'UU', root, '\t', path
		def _fix(root, path):
			def replace_begin(instr, replacethis, withthis):
				if nequals(instr, replacethis):
					rv = withthis+instr[len(replacethis):]
				else:
					rv = instr
				return rv
			root = replace_begin(root, '~/', '/local/DBi/')
			path = replace_begin(path, '~/', root or '/local/DBi/')
##			path = replace_begin(path, './', root)
			return root,path
		root, path = _fix(root, path)
		rv = ''
		if not nequals(path, root):
			if len(root): rv += root
			if rv[-1:] != '/': rv += '/'
		rv = rv + path
##		print 'translated path is', rv
		return rv
	def handlerForPath(self, path):
		fd = FileDesc(path)
		handlerPath = '/local/DBi/FileTypes/%s/Handlers/DBiHandler'%fd.getType().toString() # ShellContext, etc
		handlerName = DBiServer.getStr(handlerPath)
		rv = eval('%s()'%handlerName)
		return rv
	def lock(self):
		self.locked = true

	def unlock(self):
		self.locked = false
		self.lockedlist = []

	def add(self, line):
		self.entries[line.path]=line
		if self.locked:
			self.lockedlist.append(line)
##		print line
		
	def __init__(self):
		self.unlock()
#		self.locked 	= false
#		self.lockedlist = []
		self.handlers 	= [RCDBiHandler(self)]
		self.entries 	= {}
#		self.handlers.append(RCDBiHandler(self))

	def __del__ (self):
		for each in self.handlers:
			each = None
			
##_DBiServer = None
#
##def getDBiServer():
##	global _DBiServer
##	if _DBiServer == None:
##		_DBiServer = AwxDBiServer()
##	return _DBiServer
#
##DBiServer = getDBiServer()
##print 'xxg ', `DBiServer`
##print 'xgx ', `DBiServer.lockedlist`


DBiServer = AwxDBiServer()

#eof

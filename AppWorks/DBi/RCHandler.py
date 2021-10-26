from Value import *
from etoffiutils import xstat, progressiveParse, \
	true, false, checkRemoveEnd
import string
from Structure import *
#from File.System_ import oixfs
from File.Flags_ import Flags
from File import Perms

def getQuoted(line):
	i = 1
	ch = line[:1]
	while line[i:i+1] != ch:
		if line[i:i-1] == '\\':
			continue
		i = i + 1
	return line[1:i], line[i+2:]

def SplitLine(line):
	name = ''
	value = ''

	if line[:1] == '"':
		name, value = getQuoted(line)
	else:
		while line[:1] not in (' ', '\t') and len(line):
##			print line
			name = name + line[:1]
			line = line[1:]
		value = line[1:]

	if value[:1] in ('"', "'"):
		value = value[1:-1]
#	else:
#		value = value[1:]
		
	return (name, value)

class RCDBiHandler:
	RCEXT = '.rc'
	RCSIG = None

	def __init__(self, fn):
		self._files = {}
		self.locked = false
		self.getRoot = fn
		self.addListeners = []
	def __del__ (self):
		try:
			print "** RCDBiHandler is being GC'ed"
			for each in self._files.keys():
				self.End (each)
		except AttributeError:
			pass
	def getValue(self, path):
		gvl = DBiHandlerGetValueListener (path)
		self.addAddListener (gvl)
##		print 'get_value ( %s ) {' % path
		for each in progressiveParse(path, '/')[1:]:
			each=checkRemoveEnd(each, '/')
			fn=self.GetFileName(each)
			if fn [:-4] != '/.rc' and xstat(fn): 
				self.lock()
				self._Begin(each)
				rv = self.locker[path]
				self.unlock()
				break
		rv = gvl.getResult()
		self.removeAddListener (gvl)
##		print '}'
		return rv
	def canOpen(self, root, Type):
		Result=false
##		print "enum root", root
		u = progressiveParse(root, '/')[:-3] #:-3 to remove /local/DBi
		if Type == FOR_GET:
			u = u[1:]
##			print 'for_get {'
		else:
##			print 'for_enum {'
#			if u[0][:-1]=='/':
#				u=u[:-1]
			pass
		Result = self.__canOpen (u)
##		print '}'
		return Result

	def enum (self, top, kind=EnumFlat):
		return self.enum_flat (top)
		
	def enum_recursive (self, top):
##		if rr == EnumRecursive:
##			for each in el.getResult ():
##				rr = self.enum (each)
##				if rr is None:
##					Result.append (each)
##				else:
##					Result.append (rr)
		pass
		
	def enum_flat (self, top):
		Result = None

		try:
			ff = self._files[checkRemoveEnd(top,'/')]
			Result = []
			for each in ff.keys():
##				print "ff [ %s ] = / %s /" % (each, ff[each])
				if type(ff[each]) != type(8):
					Result.append (ff[each])
		except KeyError:
			el = DBiServerEnumListener ()
			self.addAddListener (el)

			if self.canOpen(top, FOR_ENUM):
				self.Begin(top)

			Result = el.getResult ()
			self.removeAddListener (el)
				
		return Result
		

	def __canOpen(self, aFileNameList):
		Result=false
		for each in aFileNameList:
			each = checkRemoveEnd(each, '/')
			fn   = self.GetFileName(each)
##			print 'EACH', each
##			print 'STAT', fn
			if fn [-4:] != '/.rc' and xstat(fn): 
				Result = true
##				print "yyu", fn
				break
		return Result

	def Begin(self, root):
		# Begin(root:STRING)->None
		try:
			root=checkRemoveEnd(root,'/')
			if not self._files.has_key(root):
				# TODO: these next two lines seem not to work ...
				self._files[root] = {}
				self._files[root]['max'] = 0

				self._Begin(root) # the real worker bee
			else:
				print "here fool"
		except IOError, e:
			print e
	def getFileObj(self, filename_):
		""" return an object that supports `readline' """
		## TODO: this function is capable of opening *any* file on a system!!!
		fn = self.GetFileName(filename_)
##		rv = open(fn, 'r')
		rv = oixfs.open (fn, Perms.Read, Flags())
		
##		print '%% (RCDBiHandler::_Begin) -> (%s)==(%s)' % (filename_, fn)
		
		if rv:
			if RCDBiHandler.RCSIG:
				if rv.readline() != RCDBiHandler.RCSIG:
					if rv.readline() != RCDBiHandler.RCSIG:
						rv = None
		return rv
	def _Begin(self, root):
		s       = self.getFileObj(root)
		linenum = 0 # one based!!!

##		print "_Begin", root
		
		if s == None:
			return

		if not self._files.has_key(root):
			self._files[root] = {}
			self._files[root]['max'] = 0

		try:
			while 1:
				line = s.readline()
				if not line: s.close(); break
				linenum = linenum + 1
				if len(line)<2 or line[0] == '#':
##					print 'skipping ', line,
					continue
		
##				if line[:-1] == '\\':
##					line[:-1] = ''
##					linenum = linenum - 1
##					continue
		
				(name, value) = SplitLine(line[:-1])
		
				newval = DBiValue(root+'/'+name, value, self, (root, linenum))
				self._files[root][linenum]=newval
				self._files[root]['max']=max(self._files[root]['max'], linenum)
				self.__notifyNewValue(newval)
		finally:
			s.close()
			
	def End(self, root):
		print "ending ********************************", root
		R=self._files[root]
		F=self.GetOutFile(root)
		for each in xrange(1, self._files[root]['max']+1):
			L=R[each]
			L_name=L.path[string.rindex(L.path, '/')+1:]
			for each in (' ', '\n', '\r', '\t', "'", '=', '"'):
				if each in L_name:
					if each == '"':
						L_name = "'%s'" % L_name
					else:
						L_name = '"%s"' % L_name
					break
			F.write('%s %s\012' % (L_name, L.value))
		R=None
#		self._files.remove(root)
		del self._files[root]
	def __add_to_locker(self, value):
		if self.locked:
			self.locker[value.path]=value
	def __notifyNewValue(self, newval):
		self.__add_to_locker(newval)
		##
		evt = DBiHandlerAddEvent (newval, self)
		for each in self.addListeners:
			each.actionPerformed (evt)
		evt = None # TODO: is this right??
		##
	## locking -------------------------------------------------
	def lock(self):
		self.locker={}
		self.locked=true
	def unlock(self):
		self.locker={}
		self.locked=false
	## ---------------------------------------------------------
	def x__repr__(self):
		return '<RCDBiHandler >'
	## backend -------------------------------------------------
	def GetOutFile(self, root, mode='wb'):
		return open(self.GetFileName(root), mode)
	def GetFileName(self, root):
		rv = oixfs.enumerateFirstByName (root)
		return rv
	def xx_GetFileName(self, root):
		if root[:2] == '~/':
			Root = "%s%s%s" % (self.getRoot(), root[2:], self.RCEXT)
		elif root[:11] == '/local/DBi/':
			Root = "%s%s%s" % (self.getRoot(), root[11:], self.RCEXT)
		else:
			Root = '%s%s' % (root, self.RCEXT)
		return Root
	## listeners -----------------------------------------------
	def addAddListener (self, aListener):
		self.addListeners.append (aListener)
	def removeAddListener (self, aListener):
		self.addListeners.remove (aListener)


#eof

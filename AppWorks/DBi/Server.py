from Base.Base_ import AwxBase
import Value
from etoffiutils import true, false, nequals, progressiveParse
from RCHandler import RCDBiHandler
from Structure import *
from File.System_ import System
from File.Desc_ import Desc as FileDesc
from NodeTools import *

class errNotFound(Exception):
	pass
class DBiServerProviderProxy:
	def __init__ (self, ctx):
		self.ctx = ctx
	def get_shared_information_server (self):
		return self.ctx
	def get_shared_file_server (self):
		return self.ctx.get_shared_file_server ()
class AwxDBiServer (AwxBase):
	DBIROOT = '/home/olu/oix/local/DBi/'

	def get_shared_file_server (self):
		rv = 5
		try:
			rv = self._my_file_server
		except AttributeError:
			self.building = true
			self._DBi_server_building = true
			self._my_file_server = System (self)
			rv = self._my_file_server
			self.building = false
		return rv  # would really be the server of MasterConsole
	def get_shared_information_server (self):
		return None  # would really be the server of MasterConsole
	
#	def enum(self, topkey, root='~/', kind=EnumFlat, ctx=None):
	def enum(self, topkey, root, kind, ctx):
		#~ print 711,topkey, root, kind, ctx
		#~ oixfs = ctx.get_shared_file_server ()
		rv   = []
		path = self.translatePath(topkey, root, ctx)
		#~ print '** DBi.enum > TOP =', path
		if 1:
			splitNames = path.split ('/')
			H, T = head(splitNames), tail(splitNames)
			start_node = self.node_for_path(H)
			splitNames = T
			H, T = head(splitNames), tail(splitNames)
			R = start_node.resolve(H, T)
			#~ print 715, R.name, R.nodes
			# --
			#~ assert 0
			rv = R.nodes.values()
		#~ print 716, rv
		return rv

	def get(self, path, root, ctx):
##		print 99, path, root
		search = self.translatePath(path, root, ctx)
##		print 100, search
		if self.entries.has_key(search):
			return self.entries[search]
		look = self.__lookup(search, ctx)
		if not look:
			print "search =",search
			raise errNotFound() ## TODO:
		self.entries[search] = look
		return look

	def getStr(self, path, root, ctx):
		rv = self.get(path, root, ctx).getStr()
		return rv

	def getStrOrNil(self, path, root):
		try:
			return self.getStr(path, root)
		except errNotFound:
			return None

	def __lookup(self, path, ctx):
		oixfs = ctx.get_shared_file_server ()
		rv   = None
#		path = self.translatePath(path_, '~/')
		AWX_DBI_NEWACTION = true
		if AWX_DBI_NEWACTION == true:
			b = progressiveParse(path, '/')
			for parsePath in b:
				if oixfs.exists(parsePath, ctx):
					h = self.handlerForPath(parsePath, ctx)
					if h:
						rv = h.getValue(path)
					else:
						self.log('No handler for path %s' % parsePath)
					break
		else:
			for iterdata in self.handlers:
				if iterdata.canOpen(path, FOR_GET):
					## place iterdata at top of handler stack
					rv = iterdata.getValue(path)
			## throws an exception in AbxLib (errNotFound)
		return rv

	def translatePath(self, path, root, ctx):
		if nequals(path, '~/') or path[0]=='/':
			pass
		else:
			path = root + path
		return path

	def xxyyxxyy(self, path, root, ctx):
		#~ z#~ z#~ z#~ #~ z#~ z#~ z#~ #~ z#~ z#~ z#~ #~ z#~ z#~ z#~ 
		print 888,path,root
		splitNames = path.split('/')
		#~ print 889,splitNames
		if splitNames[0] == '~':
			X = tail(splitNames)
			try:
				self.local_node.resolve(head(X), tail(X))
			except NodeNotResolvable, e:
				e.Path = path
				raise e
		assert 0

	def handlerForPath(self, path, ctx):
#		fd = FileDesc(path, DBiServerProviderProxy(self)).official ()
		fd = FileDesc(path).official (ctx)
		s='/local/DBi/FileTypes/%s/Handlers/DBiHandler'
		handlerPath = s%fd.getType().toString() # ShellContext, etc
		handlerName = DBiServer.getStr(handlerPath)
		rv = eval('%s()'%handlerName)
		return rv

	## locking -------------------------------------------------
	def lock(self):
		self.locked = true
	def unlock(self):
		self.locked = false
		self.lockedlist = []

	## adding --------------------------------------------------
	def addAddListener (self, aListener):
##		print "preadd", self.addListeners
		self.addListeners.append (aListener)
##		print "postadd", self.addListeners
	def removeAddListener (self, aListener):
		self.addListeners.remove (aListener)
	def add(self, line):
##		print "** DBiServer.addLine (", line, ")"
		self.entries[line.path]=line
		##
		evt = DBiServerAddEvent (line, line.path, self)
##		print "yy", self.addListeners
		for each in self.addListeners:
			each.actionPerformed (evt)
		evt = None # TODO: garbagef collect, please ...
		##
##		print "** tb **"
##		traceback.print_stack(file=sys.stdout)
		##
##		if self.locked:
##			self.lockedlist.append(line)

	def getRoot (self):
		return self.DBIROOT

	def node_for_path(self, path):
		if path == '~':
			return self.local_node
	
	def __init__(self):
##		self.unlock()
		dhl = DBiHandlerListener (self)
		rc = RCDBiHandler (self.getRoot)
		rc.addAddListener (dhl)
		self.handlers 		= [rc]
		self.entries 		= {}
		self.addListeners 	= []
		
		self.local_node = DBiNode_Branch()
		self.remote_nodes = DBiNode_Branch()
		
		#~ self.initialize (dhl)

	def __del__ (self):
		try:
			for each in self.handlers:
				each = None
		except AttributeError:
			pass

class InitialServer(AwxDBiServer):
	def __init__(self):
##		self.unlock()
		dhl = DBiHandlerListener (self)
		rc = RCDBiHandler (self.getRoot)
		rc.addAddListener (dhl)
		self.handlers 		= [rc]
		self.entries 		= {}
		self.addListeners 	= []
		
		self.local_node = DBiNode_Branch()
		self.remote_nodes = DBiNode_Branch()
		
		self.initialize (dhl)

	def initialize (self, dhl):
		#self.handlers[0].Begin ('~/FileSystem/TargetPonts/')
		from DBiInitializer import init
		init (dhl)

#
# eof
#

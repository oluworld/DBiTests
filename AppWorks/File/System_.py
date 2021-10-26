from string import split as string_split

from Base.Base_ import AwxBase2 as AppWorksService
from DBi.Handle_ import Handle

from Desc_ import Desc
from StdHandler_ import StdHandler
from apw_load import apw_load_class
from etoffiutils import true, false


class NodeNotResolvable(Exception): pass


def head(x): return x[0]


def tail(x): return x[1:]


class FSNode_Leaf:
	name = ''
	has_nodes = false


class FSNode_Branch:
	name = ''
	has_nodes = true
	nodes = {}

	def resolve(self, h, t):
		if not h in self.nodes:
			raise NodeNotResolvable()
		else:
			self.nodes[h].resolve(head(t), tail(t))


class System (AppWorksService):
	
	def __init__ (self, ctx):
		#AppWorksService.__init__ (ctx.get_shared_information_server ())
		self._setBasicInformationCtx (ctx)
		if 1:
			self.root_node = FSNode_Branch()
			self.root_node.name = ''
		if 1:
			stdnode = FSNode_Branch()
			stdnode.name = 'local'
			stdnode.obj = StdHandler(stdnode)
			self.addNode(stdnode)
		# ---------=
		#~ assert 0
	
	def addNode(self, stdnode):
		self.root_node.nodes[stdnode.name] = stdnode

	def stat (self, aFileName, ctx):
		rv = self.enumerateFirstByName (aFileName, ctx)
		return rv

	def enumerateFirstByName (self, aFileName, ctx):
		splitNames = aFileName.split('/')
		assert splitNames[0] == ''
		X = tail(splitNames)
		Y = self.root_node.resolve(head(X),tail(X))
		print 789, Y
		assert 0
		hh = self._find_host (aFileName, ctx)
		if hh:
			rv = hh.enumerateFirstByName (aFileName)
		else:
			rv = Desc (aFileName)
		return rv

	def exists (self, aFileName, ctx):
		#~ rv = false
		splitName = aFileName.split('/')
		print 'oixfs.exists %s'%aFileName,splitName
		assert splitName[0]==''
		X = tail(splitName)
		try:
			self.root_node.resolve(head(X),tail(X))
			rv = true
		except NodeNotResolvable:
			rv = false
		return rv

	def _find_host (self, aFileName, ctx):
		print "_find_host\n\tself: %s\n\tname: %s\n\tctx: %s" % (self, aFileName, ctx)
		my_dbi = Handle (ctx)
		c = string_split (aFileName, '/')[1]
		s = my_dbi.getStr ('~/FileSystem/TargetPoints/'+c)
		print 'getStr ~/FileSystem/TargetPoints/%s --> %s'%(c, s)
		print '_find_host wants to load %s' % s
		kl = apw_load_class (s, 'File')
		print kl
		return apply (kl, ())

	def xx_find_host (self, aFileName):
		if self.__primary == 1:
			my_dbi = Handle (self)
			c = string_split (aFileName, '/')[1]
			#print 800, c[1]
			s = my_dbi.getStr ('~/FileSystem/TargetPoints/'+c)
			print s
		else:
			self.__primary = 1
			return self.handlers[0]

	def open (self, aFileDesc, perm, flags, ctx):
		hh = self._find_host (aFileDesc.getFullName (), ctx)
		if hh:
			rv = hh.open (aFileDesc, perm, flags)
		else:
			rv = None
		#print 'open -->', rv
		return rv


class InitialSystem (System):
	def __init__ (self, ctx):
		#AppWorksService.__init__ (ctx.get_shared_information_server ())
		self._setBasicInformationCtx (ctx)
		if 1:
			self.root_node = FSNode_Branch()
			self.root_node.name = ''
		if 1:
			stdnode = FSNode_Branch()
			stdnode.name = 'local'
			stdnode.obj = StdHandler(stdnode)
			self.addNode(stdnode)
		# ----=----=----=----=----=----=----=----=----=----=----=----=----

	def initialize(self, ctx):
		my_dbi = Handle (ctx)
		s = my_dbi.enum ('~/FileSystem/TargetPoints/')
		for each in s:
			#~ print dir(each)
			each = each.obj
			#~ print 7116, each
			kl = apw_load_class (each+'Delayer', 'File')
			V = kl()
			#~ print V
		#~ assert 0
#
# eof
#

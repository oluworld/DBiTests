from etoffiutils import true, false, progressiveParse
from Desc_ import Desc
from StdHandler_ import StdHandler
from string import split as string_split
from Base.Base_ import AwxBase2 as AppWorksService
from DBi.Handle_ import Handle
from apw_load import apw_load_class
	
class System (AppWorksService):
	def __init__ (self, ctx):
		#AppWorksService.__init__ (ctx.get_shared_information_server ())
		self._setBasicInformationCtx (ctx)
		self.handlers = []
		self.addHandler (StdHandler())
		#self.__primary = 0
	def addHandler (self, handler):
		self.handlers.append (handler)
	def stat (self, aFileName, ctx):
		rv = self.enumerateFirstByName (aFileName, ctx)
		return rv
	def enumerateFirstByName (self, aFileName, ctx=None):
		# FIXME: this is wrong.  do not automaticall use ourself as a context!!
		if ctx==None: ctx=self
		hh = self._find_host (aFileName, ctx)
		if hh:
			rv = hh.enumerateFirstByName (aFileName)
		else:
			rv = Desc (aFileName)
		return rv
	def exists (self, aFileName, ctx):
		rv = false
		print 'oixfs.exists %s'%aFileName
		for each in self.handlers: #should we use #inNamespace??
			if each.exists (aFileName, ctx):
				rv = true
				break
		return rv
	def _find_host (self, aFileName, ctx):
		#print "_find_host\n\tself: %s\n\tname: %s\n\tctx: %s" % (self, aFileName, ctx)
		my_dbi = Handle (ctx)
		c = string_split (aFileName, '/')[1]
		s = my_dbi.getStr ('~/FileSystem/TargetPoints/'+c)
		#print 'getStr ~/FileSystem/TargetPoints/%s --> %s'%(c, s)
		#print '_find_host wants to load %s' % s
		kl = apw_load_class (s, 'File')
		#print kl
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
		


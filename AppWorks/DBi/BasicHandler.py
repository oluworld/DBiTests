from Base.Base_ import AwxBase2
from Value import *
from etoffiutils import true, false
from Structure import *
#from File.System_ import oixfs
from File.Flags_ import Flags
from File import Perms

class BasicHandler (AwxBase2):
	#~ INIEXT = '.ini'
	#~ INISIG = None # 'DBiIni'

	def _NAME (self):
		return 0/0
	def __init__(self, fn, ss):
#		AwxBase2.__init__ (self)
		self._setBasicInformationCtx (ss)
		self.locked = false
		self.getRoot = fn
		self.addListeners = []
		
	def __del__ (self):
		print "** %s is being GC'ed" % self._NAME ()
#		for each in self._files.keys():
#			self.End (each)
	def form_name (self, root, name):
		return '%s/%s' % (root,name)
	def End(self, root):
		print "ending ********************************", root
	def _add_to_locker(self, value):
		if self.locked:
			self.locker[value.path]=value
		print value.path, value.value
	def _notifyNewValue(self, newval):
		#self._add_to_locker(newval)
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
	## backend -------------------------------------------------
	def GetOutFile(self, root, mode='wb'):
		return open(self.GetFileName(root), mode)
	def GetFileName(self, root):
		rv = oixfs.enumerateFirstByName (root)
		return rv
	## listeners -----------------------------------------------
	def addAddListener (self, aListener):
		self.addListeners.append (aListener)
	def removeAddListener (self, aListener):
		self.addListeners.remove (aListener)

#eof

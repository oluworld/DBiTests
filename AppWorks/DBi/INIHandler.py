from BasicHandler import *
from ConfParser import ConfParser as ConfigParser
from NodeTools import *

class IniDBiHandler (BasicHandler):
	INIEXT = '.ini'
	INISIG = None # 'DBiIni'

	def xx__init__(self, fn, ss):
		BasicHandler .__init__ (self, fn, ss)
		self.locked = false
		self.getRoot = fn
		self.addListeners = []
	def _NAME (self):
		return "IniDBiHandler"
	def _set_sps (self, srv):
		self.sps = srv
	def Begin(self, root):
		c = ConfigParser ()
		c.read (root)
		
		for each in c.options ('DBiIni'):
			if each == '__name__': continue
			name, value = each, c.get ('DBiIni', each)
			
			self._a(name, value)
			root_node = self.sps.node_for_path('~')
			#~ print 7132,root_node.nodes
			#~ print 7133,root,name,value,self.form_name (root, name)
			#~ assert 0
			try:
				p = self.sps.translatePath (name, '~/', self)
			except AttributeError:
				p = name
				print 'yy'
			print 885, p
			newval = DBiValue(self.form_name (root, p), value, self, ())
			#~ self._files[root][linenum]=newval
			self._notifyNewValue(newval)
		
		c = None
	def End(self, root):
		print "ending ********************************", root
	def _a(self, name, value):
		splitName=name.split('/')
		#~ print 711,name,splitName
		assert splitName[0]=='~'
		root_node = self.sps.node_for_path('~')
		splitName=tail(splitName)
		B = self._b(root_node, head(splitName), tail(splitName))
		#~ print 713,B.name,B.obj
		B.obj = value
		#~ print 714,B.name,B.obj
	def _b(self, node, h, t):
		#~ print 712,h,node.name,node.nodes
		if node.has(h):
			m = node.at(h)
			if m.is_multi():
				m.prepend()
			return node
		else:
			if t:
				#~ print 715,h,t
				bb = DBiNode_Branch()
				bb.name = h
				node.nodes[h]=bb
				return self._b(bb, head(t), tail(t))
			else:
				#~ print 714,h
				assert node.name == 'TargetPoints'
				bb=DBiNode_Leaf()
				bb.name = h
				node.nodes[h]=bb
				return bb
		assert 0 # NotReached

#eof

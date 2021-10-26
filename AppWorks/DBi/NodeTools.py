#
#
#

from etoffiutils import true, false

class NodeNotResolvable(Exception): pass

def head(x): return x[0]
def tail(x): return x[1:]

class DBiNode_Leaf:
	def __init__(self):
		self.name = ''
		self.has_nodes = false
		self.obj = None

class DBiNode_Branch:
	def __init__(self):
		self.name = ''
		self.has_nodes = true
		self.nodes = {}
	def resolve(self, h, t):
		#~ print 1233, self.nodes
		#~ print 1234, "(%s) (%s)" % ([h], t)
		if not h in self.nodes:
			raise NodeNotResolvable()
		H = head(t)
		T = tail(t)
		if H == '': # cope with ~/FileSystem//...
			if not len(T):
				rv = self.nodes[h]
		else:
			rv = self.nodes[h].resolve(H, T)
		return rv
	def has(self, h):
		#~ print 2213, self.nodes
		return h in self.nodes
	def at(self, h):
		return self.nodes[h]
	def is_multi(self):
		return false

#
# eof
#

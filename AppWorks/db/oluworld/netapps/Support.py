from etoffiutils2.pkg        import true, false
from etoffiutils2.EqParser   import eqp_file_dict
from etoffiutils2.BackupFile import BackupFile

# ----=----=----=----=----=----=----=----=----=----=----=----=----=----=----= #

class EnvironmentAccess:

	def writelist(self, name, l):
		lower = 1
		upper = len(l)
		self.env.set(name+"/lower",str(lower))
		self.env.set(name+"/upper",str(upper))
		for each in range(lower-1, upper):
			self.env.set ("%s/%d/item"%(name,each),str(l[each]))
			#~ print "456_534: ", each,item

	def readlist(self, name):
		R = []
		lower = int(self.getenv (name+"/lower"))
		upper = int(self.getenv (name+"/upper"))
		for each in range(lower, upper+1):
			item = self.getenv ("%s/%d/item"%(name,each))
			#~ print "456_534: ", each,item
			R.append(item)
		return R

	def readdict(self, name):
		R = {}
		for each in self.readdoublet(name):
			R[each[0]]=each[1]
		return R

	def readtriplet(self, name):
		R = []
		lower = int(self.getenv (name+"/lower"))
		upper = int(self.getenv (name+"/upper"))
		for each in range(lower, upper):
			first  = self.getenv ("%s/%d/first"%(name,each))
			second = self.getenv ("%s/%d/second"%(name,each))
			third  = self.getenv ("%s/%d/third"%(name,each))
			R.append([first, second, third])
		return R

	def readdoublet(self, name):
		R = []
		lower = int(self.getenv (name+"/lower"))
		upper = int(self.getenv (name+"/upper"))
		for each in range(lower, upper):
			first  = self.getenv ("%s/%d/first"%(name,each))
			second = self.getenv ("%s/%d/second"%(name,each))
			R.append([first, second])
		return R

	def getenv(self, s):
		return self.env.get(s)

	def getenv_d(self, s, d):
		try:
			return self.getenv(s)
		except KeyError:
			return d

	def set_dict_entry(self, first, second):
		self.env.set(first+'/first',  first)
		self.env.set(first+'/second', second)

	def has(self, key):
		return e.has(key)

# ----=----=----=----=----=----=----=----=----=----=----=----=----=----=----= #

class Environment:
	def __init__(self):
		self._E = None
	def __del__(self):
		self.close()
	def close(self):
		if self._E:
			b = BackupFile(self._filename)
			for n, v in self._E.items():
				b.write('%s = %s\012' %(n,v))
			b.close()
			self._E = None
	def read_from(self, filename):
		import os
		if not os.path.isfile(filename):
			print "Cannot Initialize environment in "+filename
			raise "Cannot Initialize environment in "+filename
		x=open(filename)
		dd = eqp_file_dict(x)
		x.close()
		self._E = dd #print dd
		self._filename = filename
	def get(self, x):
		return self._E[x]
	def set(self, x, y):
		self._E[x] = y
	def has(self, key):
		R = true
		try:
			G = self.get(key)
		except KeyError:
			R = false
		return R
	#
	__slots__ = [__init__, read_from, get, set, close, has]

# ----=----=----=----=----=----=----=----=----=----=----=----=----=----=----= #

#
# eof
#

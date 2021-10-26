from __future__ import generators
import os

"""
 BackupFile will automagically make a backup of a file
  before opening it (for writing).  It is compatible 
  with OIX filenames (ie: env.{456e56})
 
"""

def extract_oix_type(filename):
	try:
		e = filename[-9:]
		if e[:2] == '.{' and e[-1] == '}':
			R = (filename[:-9], e[1:])
		else:
			R = (filename, '')
	finally:
		if R[1]: assert "%s.%s"%(R[0],R[1])==filename
		return R

def ensure_clear_name(filename,renamer=os.rename,isfile=os.path.isfile):
	a,b=extract_oix_type(filename)
	if not b:
		fn = RegFileNameAdapter(filename)
	else:
		fn = OixFileName(filename)
	
	assert fn.wholename()==filename
	if isfile (fn.wholename()):
		newfn = fn.renamed(fn.N)
		i = 1
		while isfile (newfn.wholename()):
			#~ print 88,newfn.wholename()
			newfn = newfn.renamed(fn.N+'.~%d~' % i)
			#~ print 86,newfn.wholename()
			i = i + 1
		#~ print "567_457: ",fn.wholename(), newfn.wholename()
		renamer(fn.wholename(), newfn.wholename())
		assert isfile (newfn.wholename())
		assert not isfile (fn.wholename())

class RegFileNameAdapter:
	def __init__(self, filename=None):
		if not filename: return
		self.N = filename
	def renamed(self, newname):
		R = RegFileNameAdapter(newname)
		return R
	def wholename(self):
		return self.N

class OixFileName:
	def __init__(self, filename=None):
		if not filename: return
		e = filename[-8:]
		if e[0] == '{' and e[-1] == '}':
			R = (filename[:-9], e)
		else:
			R = (filename, '{000000}')
		self.N, self.E = R
	def renamed(self, newname):
		R = OixFileName()
		R.N = newname
		R.E = self.E
		return R
	def wholename(self):
		return "%s.%s"%(self.N,self.E)

class BackupFile:
	def __init__(self, filename=None):
		if filename: self.open(filename)
	def open(self, filename):
		ensure_clear_name(filename)
		self._f = open(filename, "w")
		self.filename = filename
	def close(self):
		self._f.close()
	def write(self, s):
		self._f.write(s)

def test():
	def _rename(x,y):
		assert x=='env.{456e56}'
		assert y=='env.~1~.{456e56}'
	def _isfile(x):
		yield true
		yield false
	ensure_clear_name('env.{456e56}',_rename,_isfile)

#
# eof
#

from etoffiutils2.time_ import tt, ttp

true  = 1
false = 0

# --------=--------=--------=--------=--------=--------=--------=--------=--------#

def combine_lists(x,y): 
	""" 1.0 -- marked 2002_04Apr23 """
	return tuple(x)+tuple(y)

# --------=--------=--------=--------=--------=--------=--------=--------=--------#

class EtoffiBasicException(Exception):
	""" 1.0 -- 2002_04Apr23 """
	def __init__(self, e):
		self.e = e
	def __str__(self):
		return `self.e`

# --------=--------=--------=--------=--------=--------=--------=--------=--------#

def hex_md5(aString):
	''' takes a string. returns a string '''
	""" marked 2002_04Apr23 """
	import md5
	return md5.new(aString).hexdigest()

# --------=--------=--------=--------=--------=--------=--------=--------=--------#

def xpmt (s):
	''' fill a line with s between equal signs '''
	""" 1.0 -- marked 2002_04Apr23 """
	S = 75 - len(s)
	if S > 0:
		print '== %s %s' % (s, '='*S)
	else:
		print '== %s =' % s

# --------=--------=--------=--------=--------=--------=--------=--------=--------#

def xmpta (s):
	''' fill a line with s between asterisks '''
	""" 1.0 -- marked 2002_04Apr24 """
	S = 75 - len(s)
	if S > 0:
		print '** %s %s' % (s, '*'*S)
	else:
		print '** %s *' % s

# --------=--------=--------=--------=--------=--------=--------=--------=--------#

def identity(x): return x
def choose(x,y,z): 
	if x: 
		return y
	return z

# --------=--------=--------=--------=--------=--------=--------=--------=--------#

#
# eof
#

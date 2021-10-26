from etoffiutils2.pkg import choose, identity

# 1.0: 2002_07Jul27 2200
# 1.5: 2002_08Aug22 2000

#
# call eqp with each line
#

#def eqp(s):
#	return eqp_(s, '', '')
def eqp_(S,n,v):
	G = 1
	N = 0
	s = S
	while G:
		x  = s[0]
		xs = s[1:]
		if x == '=':
			G = 0
		else:
			N+=1
			s = xs
	return S[:N], xs

def eqp_lines(l,a=identity,b=identity):
	# eqp_lines(list) -> tuple_list
	R = []
	for each in l:
		if len (each)==1: continue  #filter blanks
		n, v = eqp_(each, '', '')
		R.append((a(n),b(v)))
	return R

def fixfile(f):
	R=f[:0]
	for n,v in f:
		n = n.rstrip()
		v = v[:-1].lstrip()
		R.append((n,v))
	return R

def eqp_file(f):
	""" eqp_file(file_object) -> pair_list 
	"""
	def a(x): return x.rstrip()
	def b(x): return x[:-1].lstrip()
	# --
	if not hasattr(f, 'xreadlines'):
		f.xreadlines = f.readlines
	R = eqp_lines(f.xreadlines(),a,b)
	#~ return fixfile(R)
	return R

def eqp_file_dict(f):
	# f is a file object
	L = eqp_file(f)
	R = tuple_list_to_dict(L)
	return R
	
def tuple_list_to_dict(L):
	R = {}
	for n, v in L:
		R[n] = v
	return R
	
#
# eof
#

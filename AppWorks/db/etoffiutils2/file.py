import os

true = 1
false = 0

def xstat(fn):
	import os
	try:
		os.stat(fn)
#		print 'XSTAT /+/ ' + fn
		return true
	except OSError:
		print 'XSTAT \\-\\ ' + fn
		return false

def progressiveParse(Str, Sep):
	""" Jan-05 """
	r=string.split(Str, Sep)
	rv=[]
	for each in xrange(len(r), 0, -1):
		m=string.join(r[:each], '/')+'/'
##		print m
		rv.append(m)
	return rv #.reverse()

def reverse_findfile(fn):
	""" Jan-05 """
	l=progressiveParse(fn, '/')
	for each in l:
		if os.stat(each):
			return each

def ____cvg(x):
	if x.errno!=2:
		print x
def read_firstline_from_file(filename, strip=true, eh=____cvg):
	""" Jan-06 (1734) """
	rv=None
	try:
		F  = open(filename)
		rv = F.readline()
		if strip:
			rv = rv[:-1]
		F.close()
	except IOError, e:
		if eh: eh(e)
	return rv

def quickAppend(fn, lines, addNL=true):
	""" fn:FileName lines:List<?a> addNL:bool=true 01-Jan-13 (0349) """
	f = open(fn, 'ab+')
	if addNL:
		f.writelines(map(lambda e: "%s\012" % str(e), lines))
	else:
		f.writelines(lines)
	f.close()


def ensure_directory_present(dn, logfile=None):
	try:
		os.makedirs(dn)
	except OSError, e:
		if e.errno != 17: # EEXIST
			if logfile:
				logfile.write(e)

def quickWrite(fn, lines, addNL=true):
	"""fn:FileName lines:List<?a> addNL:bool=true"""
	f = open(fn, 'w')
	if addNL:
		f.writelines(map(lambda e: "%s\012" % str(e), lines))
	else:
		f.writelines(lines)
	f.close()

def inc_until_nofile(num, pre, post, logfile=None):
	try:
		qr = '%s%d%s' % (pre, num, post)
		while os.stat(qr):
			num = num + 1
			qr = '%s%d%s' % (pre, num, post)
	except OSError, e:
		if e.errno != 2:
			if logfile:
				logfile.write(e)
	return num	

def inc_until_nofile_fn(num, fun, logfile=None):
	try:
		qr = apply(fun, (num,))
		while os.stat(qr):
			num = num + 1
			qr = apply(fun, (num,))
	except OSError, e:
		if e.errno != 2:
			if logfile:
				logfile.write(e)
	return num	
def quickReadFunc(filename, fn, strip=false, stripcomments=false):
	return map (fn, dumplines(open(filename).readlines(), strip, stripcomments))

def dumptextfile(filename, strip=false, stripcomments=false):
	return dumplines(open(filename).readlines(), strip, stripcomments)

def dumplines(l, strip=false, stripcomments=false):
	if strip:
		l = map(lambda e: e.rstrip(), l)
	if stripcomments:
		l = map(lambda e: strip_comments(e), l)
	
	return l

def strip_comments(line):
	r = line.find('#')
	if r == -1:
		return line
	if r == 0:
		return ''
	if line[r-1:][0] == '\\':
		return strip_comments(line[r+1:])
	raise line[r:]

def ensure_clear_name(filename):
	if os.path.isfile (filename):
		newfn = filename
		i = 1
		while os.path.isfile (newfn):
			newfn = '%s.~%d~' % (newfn, i)
			i = i + 1
		os.rename(filename, newfn)
		assert os.path.isfile (newfn)
		assert not os.path.isfile (filename)

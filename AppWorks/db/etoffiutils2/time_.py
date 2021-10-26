#
#
#

import time, os

# --------=--------=--------=--------=--------=--------=--------=--------=--------#

# from rfc822.py. thnaks Python!!
def formatdate(timeval=None):
	"""Returns time format preferred for Internet standards.

	Sun, 06 Nov 1994 08:49:37 GMT  ; RFC 822, updated by RFC 1123
	"""
	if timeval is None:
		timeval	= time.time()
	return time.strftime('%a, %d	%b %Y %H:%M:%S GMT', 
	                       time.gmtime(timeval))

# --------=--------=--------=--------=--------=--------=--------=--------=--------#

def tt():
	""" 1.0 -- marked 2002_04Apr23 """
	R=time.strftime("%y_%m%b%d=%H%M", time.localtime(time.time()))
	return R
	
def ttp():
	""" 1.0 -- marked 2002_04Apr23 """
	R=time.strftime("%Y_%m%b%d (%H%M:%S)", time.localtime(time.time()))
	return R

# --------=--------=--------=--------=--------=--------=--------=--------=--------#

def today_date():
	r = time.strftime('%Y-%b-%d (%H%M)', time.localtime(time.time()))
	return r

# --------=--------=--------=--------=--------=--------=--------=--------=--------#

#
# eof
#

#
# etoffiutils2.string
#

def string_ends_with(s,s2):
	if string_right(s, len(s2)) == s2:
		return 1
	return 0

def string_right(str, len):
	return str[-len:]

def string_upto(str, spot):
	return str[:-spot]

def checkRemoveEnd(instr, endwith):
	le = len(endwith)
	if string_right(instr,le)==endwith:
		rv=string_upto(instr, le)
	else:		
		rv=instr
	return rv

def is_integral_string(s):
	for each in s:
		if not each in "0123456789":
			return false
	return true

def is_octal_string(s):
	for each in s:
		if not each in "01234567":
			return false
	return true

def nequals(s1, s2):
	return s1[:len(s2)] == s2

def Fill(num, fillspec='0', length=3):
	""" does not truncate data. then full number num will be output. 
	    fillspec must be a char 
	"""
	ret = str(num)
	l   = length - len(ret)
	if l > 0:
		ret = '%s%s' % (fillspec * l,ret)

	return ret

#
# eof
#

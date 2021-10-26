modCache = {}
def apw_load_module (klazz, module_):
	v = (klazz, module_)
	global modCache
	try:
		rv=modCache[v]
	except KeyError:
		# <begin_whoa>
		mm = __import__('AppWorks.%s.%s'%(module_,klazz))
		kl = mm.__dict__[module_].__dict__[klazz]
		#print 'kl',kl
		# </end_whoa>
		modCache[v]=kl
		rv=kl
	return rv
def apw_load_class (klazz, module_):
	return apw_load_module (klazz, module_).__dict__ [klazz]


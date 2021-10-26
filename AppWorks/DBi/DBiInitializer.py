from INIHandler import IniDBiHandler

class IniDBiHandler2 (IniDBiHandler):
	def form_name (self, root, name):
		return name

def init (dhl):
	i = IniDBiHandler2 (dhl.server.getRoot (), dhl.server)
	i.addAddListener (dhl)
	i._set_sps (dhl.server)
#	print 'ii'
	i.Begin ('root.dbi')
#	print 'iii'

#eof


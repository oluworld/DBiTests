from DBi.INIHandler import IniDBiHandler

class IniDBiHandler2 (IniDBiHandler):
	def form_name (self, root, name):
		return name

# accepts root : FileName, DBiHandler
i = IniDBiHandler2 ('q:/DBi', None)
i.Begin ('root.dbi')

#eof


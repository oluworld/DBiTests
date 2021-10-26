from DBi.Handle_ import *
from Base.App_ import App
from DBi.Server import AwxDBiServer as Server
from File.System_ import System

class DefaultApp (App):
	def preInit (self):
		self._my_info_server = Server ()
		self._my_file_server = System (self)
#		self._setBasicInformation (Server (), System (self))
	def do_run (self):
		my_dbi = Handle (self)
		my_dbi.setRoot ("~/Programs/OluWorld/DBiTest/")
		c = my_dbi.enum ("")

		print my_dbi.enumStr ('')

		print len(c)

		for each in c:
			print each.getName (), '\t', each.value

		c = my_dbi.enum ("../Typeman/")
		
		for each in c:
			print each.getName (), '\t', each.value

		self.quit ()

app = DefaultApp ()
app.init ([])
app.run ()


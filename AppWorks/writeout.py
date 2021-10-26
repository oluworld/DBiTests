from etoffiutils import ensure_directory_present, true, false

from Base.App_ import App

from File.System_ import System
from File.Desc_ import Desc
from File.Flags_ import Flags, Blank_Flags
from File import Perms

from DBi.Server import AwxDBiServer as Server

class e: pass

def gget (n):
	rv = ''
	for each in range(n):
		rv = '%s%s' % ('*'*n,rv)
	return rv

def write_out (n, lines, oixfs, ctx):
	dd = Desc ('out/%d'%n)
	hh = oixfs.open (dd, Perms.Read, Blank_Flags, ctx)
	rv = false
	if hh:
		for each in lines:
			hh.write (each, len(each))
		rv = true
		hh = None
	return rv
		
class DefaultApp (App):
	def preInit (self):
		self._my_info_server = Server ()
		self._my_file_server = System (self)
#		self._setBasicInformation (Server (), System (self))
	def do_run (self):
		oixfs = self.get_shared_file_server ()

		ensure_directory_present('out')
		for n in range(1,10):
			try:
				# dont delete until we know it written
				if write_out (n, gget(n), oixfs, self):
					print '-- ok', n
				else:
					print '-- file was not written'
			except e:
				pass
		self.quit ()

app = DefaultApp ()
app.init (None)
app.run ()

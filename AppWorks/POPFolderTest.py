import sys, os
sys.path.append(os.getcwd()+'/../')

# -----

#from AppWorks.File.POPFolder import POPFolder
#from AppWorks.File import Perms, Flags
from etoffiutils import quickWrite, ensure_directory_present, true, false

from AppWorks.Base.App_ import App
from AppWorks.Base.Base_ import AwxBase2

from AppWorks.File.System_ import System, InitialSystem
from AppWorks.File.Desc_ import Desc
from AppWorks.File.Flags_ import Flags, Blank_Flags
from AppWorks.File import Perms

from AppWorks.DBi.Server import AwxDBiServer as Server, InitialServer

from ConfParser import ConfParser as ConfigParser

server, user, passwd = 'localhost', 'user', 'secret'

def readdef ():
	c = ConfigParser ()
	c.read ('POPFolderTest.ini')
	global server, user, passwd
	server = c.get ('root', 'server')
	user   = c.get ('root', 'user')
	passwd = c.get ('root', 'passwd')
	c = None
	
def do_login (sname, user, passwd, oixfs, ctx):
	dd = oixfs.stat ('/pop/%s/login' % sname, ctx)
	handler = dd.host
#	login_handle = handler.open(dd, Perms.Read, Blank_Flags)
	login_handle = oixfs.open(dd, Perms.Read, Blank_Flags, ctx)
	rv = (None, dd, None, None)
	if login_handle:
		if login_handle.write_string ('user '+user) != None:
			m = login_handle.write_string ('pass '+passwd)
			if m != None:
#				assert (handler == login_handle.host)
				rv = (handler, dd, Blank_Flags, m) #login_handle)
				assert (login_handle.getServer() == m.getServer())
	#print 747, rv
	return rv

def write_out (n, lines):
	dd = Desc ('out/%d'%n)
	hh = oixfs.open (dd, Perms.Read, Blank_Flags)
	rv = false
	if hh:
		for each in lines:
			hh.write (each, len(each))
		rv = true
		hh = None
	return rv
	
class DefaultApp (App):
	def preInit (self):
		self._my_ctx_AppName = 'POPFolderTest-aug2002'
		self._my_ctx_AppVendor = 'AppWorksDemos!'
		#~ self._my_info_server = Server ()
		#~ self._my_file_server = System (self)
		##self._setBasicInformation (Server (), System (self))
		App.preInit(self)
	def postInit(self):
		App.postInit(self)
	def do_run (self):
		oixfs = self.get_shared_file_server ()
		#######################################
		# initialize
		readdef()
		#######################################
		# login to the server
		stat_handle, dd, ff, cur_handle = do_login (server, user, passwd, oixfs, self)
		
		ensure_directory_present('out')
		for n in range(1,10):
			dd     = Desc('/pop/%s@%s/msgnum/%d' % (user, server, n))
			##handle = cur_handle.open(dd, Perms.Read, ff)
			handle = oixfs.open(dd, Perms.Read, ff, self)
			print 918
			try:
				# dont delete until we know it written
				if write_out (n, handle.readlines()):
					if handle.unlink(handle.myDesc) == true:
						print '-- file removed'
					else:
						print '-- file not removed'
				else:
					print '-- file was not written'
			except:
				pass
		##	print "vvcls"
			handle.close()
			
		#login_handle.close()

def AppWorksMain(app):
	class Z(AwxBase2):pass
	initial = Z()
	initial._my_info_server = InitialServer ()
	initial._my_file_server = InitialSystem (initial)
	initial._my_file_server.initialize(initial)
	# --
	app._my_info_server = Server ()
	app._my_file_server = System (app)#initial)#app)
	#
	app.init (None)
	app.run ()

da = DefaultApp ()
AppWorksMain(da)

from etoffiutils import *

class StreamState:
	NoExist = -3
	NeverOpened = -2
	EndOfStream = -1
	Closed = 0
	Opening = 1
	Acceptable = 2
	Reading = 3
	Writing = 4
class Perms:
	Exist     = 0 #F_OK
	Read      = 1 #R_OK
	Write     = 2 #W_OK
	ReadWrite = 3 #R_OK|W_OK
	Execute   = 4 #X_OK
class Flags:
	def __init__(self):
		self.raw     = false #deref ::so files
		self.excl    = false #exclusive access
		self.trunc   = false #kill file contents on open
		self.rcreat  = false #create for write if non-existant upon open
		#
		self.inherit = true  #inherited by forked/sub- processes.
							 #at this point, there are no subprocesses and
							 #no forking. threads are not affected by this
		self.binary  = true  #crlf crap
		self.wcreat  = true  #create for write if non-existant upon open

class Desc:
	# path name host type perms atime mtime ctime size
	pass

class Handle:
	def __init__(self):
		self.myState = StreamState.NeverOpened
		self.mode    = Perms.Read
		self.myFlags = Flags()
		self.offset  = 0 #
		self.host    = None #[ABSTRACT]iACDirHandler()
		self.myDesc  = None #Desc()
		self.extra   = None
	def set(self, desc, handler, extra, state = StreamState.NeverOpened, \
					mode=Perms.Read, flags=Flags(), offset=0):
		self.myState = state
		self.mode    = mode
		self.myFlags = flags
		self.offset  = offset
		self.host    = handler
		self.myDesc  = desc
		self.extra   = extra
	def read(self, len): # add wait:BOOLEAN??
		self.host.read(self, len)
	def write(self, data, size):
		self.host.write(self, data, size)
	def write_string(self, str):
		self.host.write(self, str, len(str))
	def close(self):
		self.host.close(self)
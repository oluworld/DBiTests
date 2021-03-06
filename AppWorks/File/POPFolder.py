from DirHandler import iDirHandler
from poplib import POP3
from etoffiutils import *
#from AppWorks.File import *
from MMS.BasicMessage import MMSMessage
from string import split as string_split

from File.Desc_ import Desc
from File.Handle_ import Handle
from File import Perms
from File import StreamState

"""
implement a pop folder. will be used in AwxMail.

"""

class POPFolderError(Exception):
	def __init__(self, str):
		self.gg=str
	def __str__(self):
		return str
class POPFolderData:
	def __init__(self, folder, server):
		self.folder = folder
		self.server = server
class POPFolderWritableData(POPFolderData):
	pass

class POPFolderLoginHandle(Handle):
	def close(self):
		print "$$ quitting server"
		self.extra.server[0].quit()
	def getServer(self):
		return self.extra.server[0]

class POPFolderHandle(Handle):
	def readlines(self):
		return self.extra.msg.msg
	def getServer(self):
		return self.extra.server[0]
	def inc_srv_cnt(self):
		cnt = self.extra.server[1]
		self.extra.server = (self.extra.server[0], cnt+1)
		print '@@ increment', self.extra.server[0], cnt+1
	def close(self):
		cnt = self.extra.server[1]
		self.extra.server = (self.extra.server[0], cnt-1)
		print '@@ decrement', self.extra.server[0], cnt-1
		if self.extra.server[1] == 0:
			print "$$ quitting server"
			self.extra.server[0].quit()

class POPFolder(iDirHandler):
	def __init__(self):
		self.SRVLIST = {}
	def canOpen(self, path, perm):
		""" path:File.Path, perm:File.Perms -> bool
			/pop/$server/$msgnum
		"""
		if string_split (path, '/') > 3:
#		if path[:5] == '/pop/' and len(path)>5:
			return true
		else:
			return false

	def enumerate(self, spec):
		""" spec:String -> List<File.Desc> """
		pass

	def enumerateFirstByName(self, spec):
		""" spec:File.Name -> File.Desc """
		s = string_split (spec, '/')
		print 'stat %s (%s)' %  (spec, s[3])
		rv = Desc (spec)
		rv.host = self
		return rv
	
	def insert(self, desc):
		""" -> bool """
		if getParam('forward-smtp'):
			h = oixfs.getHandlerForPathOrNil(getParam('forward-server'))
			if h:
				return h.insert(desc)
		else:
			return false
		
	def unlink(self, desc):
		""" -> bool """
		Result = false
		f = Flags()
		f.excl = true
		print "** unlink", desc.getFullName ()
		h = self.open(desc, Perms.Read, f)
		if h:
			#print "ok"
			ll = string.split(desc.getFullName (), '/')
			if ll[3] == 'msgnum':
				msgnum = ll[4]
##				print "^^ msgnum", msgnum
				r = h.getServer().dele(msgnum)
				h.close()
				if r[:1] == '+':
					Result = true					
			else:
				raise POPFolderError("Invalid AccessMethod: "+ll[3])
		print "%% unlink"
		return Result
		
	def __validate_method(self, meth):
		#if meth != 'pop': raise InvalidMethodException(self, meth)
		pass
	def __make_srvname(self, ll):
		return ll
	def __int_open(self, desc, perms, flags, extra): #private, please
		ll = desc.getFullName ().split('/')[1:]
		self.__validate_method(ll[0])
		srvname = self.__make_srvname(ll[1])
		
		print "** __int_open: desc.getFullName ()", desc.getFullName ()

		# ---------------------------------------------------
		accval = None
		acctype = None
		# ---------------------------------------------------
		if len(ll) > 2:
			acctype = ll[2]
		else:
			raise POPFolderError("No AccessType Specified")
		# ---------------------------------------------------
		if len(ll) > 3:
			accval = ll[3:]
		else:
			#raise POPFolderError("No AccessValue Specified")
			pass			
		# ---------------------------------------------------

		if acctype == 'msgnum':
			curHandle = POPFolderHandle()
			curHandle.set(desc, self, None, StreamState.Opening, perms, flags)
			curHandle.extra = apply(extra, (curHandle,self.__int_getserver(srvname)))
			curHandle.myState = StreamState.Acceptable

			(resp, msg, octets) = curHandle.getServer().retr(accval[0])
			U = string.split(curHandle.getServer().uidl(accval[0]))[-1]
			curHandle.inc_srv_cnt()
#			msg = map(lambda e: "%s\012" % e, add_to_head("X-UIDL: %s" % U, msg))

			curHandle.extra.msg = MMSMessage(msg, U, resp, octets)
			return curHandle
		elif acctype == 'login':
			curHandle = POPFolderLoginHandle()
			curHandle.set(desc, self, None, StreamState.Opening, perms, flags)
			curHandle.extra = apply(extra, (curHandle,0))
				#self.__int_getserver(srvname, (accval[0],accval[1],'userpass'))))
			curHandle.myState = StreamState.Closed
			return curHandle
		else:
			raise POPFolderError("Invalid AccessType Specified")

	def __int_getserver(self, srvname, authinfo=None):
##		print "** getserver", srvname
##		print "---------"
##		print self.SRVLIST
##		print "---------"
		if self.SRVLIST.has_key(srvname):
			port, authinfo, refcnt, inst = self.SRVLIST[srvname]
#			self.SRVLIST[srvname] = (port, authinfo, refcnt, inst)
			return inst, refcnt
		else:
			#/pop/[user[:passwd]]@server[:port]/
			s = POP3(srvname) # vv port authinfo refcnt instance
			u = '(DEF)'
			if authinfo != None:
				if authinfo[2] == 'userpass':
					u = authinfo[0]
					s.user(authinfo[0])
					s.pass_(authinfo[1])
				elif authinfo[2] == 'apop':
					## APOP foofery
					pass
			self.SRVLIST[srvname+'-'+u] = (110, authinfo, 1, s)
			return s, 1
	
	def open(self, desc, perms, flags):
		""" -> File.Handle """
		if perms == Perms.Read:
			return self.__int_open(desc, perms, flags, POPFolderData)
		elif perms == Perms.Write:
			return self.__int_open(desc, perms, flags, POPFolderWriteableData)
		else:
			return None
		
	def reopen(self, handle, perms, flags):
		""" -> File.Handle """
		if perms == handle.perms and flags == handle.flags:
			return handle
		
		ret = open(handle.desc, perms, flags) # what if
		self.close(handle) # what kind of exception handling here?
		return ret
	
	def close(self, handle):
		""" -> bool """
		print "closing"
		if handle.server == None:
#			raise err("already closed")
			return false
		port, authinfo, refcnt, inst = handle.server
		if refcnt == 1:
			del port, authinfo, inst, refcnt, handle, server
##			handle.server = None
		return true
		
	def write(self, handle, data, size):
		""" File.Handle ByteStream int -> int """
		pass
		
	def read(self, handle, size):
		""" File.Handle int -> ByteStream """
		pass
		
	def seek(self, handle, amt, dir, pos):
		""" handle:File.Handle amt:uint dir:(*forward*, backward) pos:(beg, end, *cur*) """
		pass
		
##	def setParams(self, handle, params):
##		""" handle:File.Handle params:?a """
##		pass
##		
##	def handle(self, evt):
##		pass
	
	
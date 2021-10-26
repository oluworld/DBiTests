from Backend import *
from etoffiutils import true, false
#from AppWorks.Event import fireToEx
from Base.Base_ import AwxBase2 as AppWorksService

class App (AppWorksService):
	''' straight from AbxLib snapshot '''
	def __init__(self):
		self._quitNow   = false
		self._retVal    = 0
		self._PID       = 0
		self._extraInfo = None
		self._args      = None
		self.appname    = ''
		self.apppath    = ''
		AppWorksService.__init__ (self)
		
	def init(self, args):
		self.preInit()
		if args:
			if args.has ("--help"):
				self.fireTo ("expose onassist", self)
				self.quit ()
			elif args.has ("--version"):
				self.fireTo ("expose onassist", self, "version", "true")
				self.quit ()
		else:
			self.do_init(args)
			self._args=args
			self.postInit()
	def do_init(self, args):
		pass
	def unix_init(self, argc, argv):
		self._args = []
		for i in range(1, argc):
			self._args[i] = argv[i]
		self.init(self._args)
	def preInit(self):
		pass
	def postInit(self):
		pass
	def shExec(self, cmd):
		''' execute a shell command. return a Msg.Event '''
		pass
	def shExecAndWait(self, cmd):
		pass
	def onAssist(self, evt):
		if evt.msg == 'expose version':
			if hasattr(self, 'VERSION_STRING'):
				self.display_help_message(self.VERSION_STRING)
				return okEvent
			else:
				return badEvent
		if hasattr(self, 'HELP_MESSAGE'):
			self.display_help_message(self.HELP_MESSAGE)
			return okEvent
		else:
			return badEvent
	def setPID(self, pid):
		self._PID = pid
	def getHandle(self):
		return self._PID
	def preQuit(self):
		pass
	def postQuit(self):
		pass
	def quit(self, rc=0):
		self.preQuit()
		self._retVal=rc
		self._quitNow=true
		self.postQuit()
	def win_init(self, cmdline, cmdshow):
		pass
	def run(self):
		while not self._quitNow:
			self.do_run ()
	def xxrun(self):
		while not self._quitNow:
			if not self._be.isEventPending ():
				self.do_run()
			else:
				event = self._be.getEvent ()
				self.handle (self._be.translateEvent (event))
		return self._retVal
	def handle (self, evt):
		print 'unhandled in AppWorks.Base.App:',evt.msg
		

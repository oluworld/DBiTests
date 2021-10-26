from etoffiutils import true, false

class App:
	''' straight from AbxLib snapshot '''
	def __init__(self):
		self._quitNow   = false
		self._retVal    = 0
		self._PID       = 0
		self._extraInfo = None
		self._args      = None
		self.appname    = ''
		self.apppath    = ''
		
	def init(self, args):
		self.preInit()
		'''
			if(args->find(&STRING("--help")) != -1)
			{
				fireTo("expose onassist", this);
				
				quit();
				return;
			}
		
			if(args->find(&STRING("--version")) != -1)
			{
				fireTo("expose onassist", this, "version", "true");
				
				quit();
				return;
			}
		'''
		self.do_init(args)
		self.args=args
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
			self.do_run()
		return self._retVal

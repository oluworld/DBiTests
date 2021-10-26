true=1
false=0

Static     = 1
Expandable = 0
Shrinkable = 2

class PropertyHolder:
	def __init__(self):
		self.props={}
	def __getitem__(self, item):
		return self.props[item]
	def __setitem__(self, item, value):
		self.props[item] = value

class Window(PropertyHolder):
	def __init__(self):
		PropertyHolder.__init__(self)
		self.children = {}
		self._reset()
	def __getitem__(self, item):
		if item == 'name':
			rv = self.getName()
		else:	
			rv = PropertyHolder.__getitem__(self, item)
		return rv
	def getName(self):
		try:
			rv = PropertyHolder.__getitem__('name')
		except:
			import md5, time
			rv = md5.new(`time.time()`).hexdigest()
			self['name']=rv
		return rv
	def _reset(self):
		self['height'] = 10
		self['width'] = 10
		self['x-coord'] = 10
		self['y-coord'] = 10
	def add(self, child):
		self.children[child['name']] = child
	def Create(self, parent, dbiKey, readDBi=true):
		""" parent (can be NULL) dbiKey (also window name) readDbi 

		Create :
			1) calls preCreate
			2) sets the dbiroot property
			3) calls readDBi
			4) sets the window_name property
			5) adds the window to the parent (if not NULL)
			6) sets the parent (feature)
			7) calls do_Create (the one that gets overridden by impls)
			8) calls postCreate
		"""
		self.preCreate()
		if dbiKey[0]=='/' or dbiKey[:2]=='~/':
			self['dbiroot']=dbiKey
			self['XXXXXXXXXx']='NAME-IS-WRONG!!'
			self['name']=dbiKey[dbiKey.rfind('/'):]
		else:
			if parent:
				self['dbiroot']=parent['dbiroot']+'/'+dbiKey
			else:
				self['dbiroot']=dbiKey
##		self.readDBi(self['dbiroot'])
			self['name']=dbiKey
		if parent: ## skip this for frames, desktop, etc
			parent.add(self)
		self.parent=parent
		self.do_Create(parent, dbiKey, readDBi)
		self.postCreate()
	def preCreate(self):
		pass
	def postCreate(self):
		pass


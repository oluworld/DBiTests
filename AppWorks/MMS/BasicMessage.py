from etoffiutils import nequals

class MMSMessage:
	def __init__(self, msg, uidl, resp, octets, opts=()):
		self.msg    = msg
		self.uidl   = uidl
		self.resp   = resp
		self.octets = octets
		self.cached = {}
		self.opts   = opts
	def GetHeader(self, lookfor):
		lookfor     = lookfor.lower()
		if self.cached.has_key(lookfor):
			return self.cached[lookfor]
		lookfor_len = len(lookfor)+2 # Assuming <headername> colon space <value>
		for each_line in self.msg:
			if nequals(each_line.lower(), lookfor):
				self.cached[lookfor] = each_line[lookfor_len:]
				return self.cached[lookfor]
		return None
	def getId(self):
		return self.uidl

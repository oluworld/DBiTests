
class AwxBase:
	def get_shared_information_server (self):
		return DBiServer
class AwxBase2 (AwxBase):
	def __init__ (self):
		self._my_info_server = None
		self._my_file_server = None
	def _setBasicInformation (self, info, file, window = None):
		self._my_info_server = info
		self._my_file_server = file
	def get_shared_information_server (self):
		return self._my_info_server
	def get_shared_file_server (self):
		return self._my_file_server
	def _setBasicInformationCtx (self, ctx):
		self._my_info_server = ctx.get_shared_information_server ()
		try:
			ctx._DBi_server_building				
			self._my_file_server = None
		except AttributeError:
			self._my_file_server = ctx.get_shared_file_server ()
		
		
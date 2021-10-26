from AppWorks.File.POPFolder import POPFolder
from AppWorks.File import Perms, Flags

class _Desc:
	def __init__(self, path):
		self.path = path

handler = POPFolder()
dd = _Desc('/pop/localhost/login/etoffi/foo')
ff = Flags()
handle  = handler.open(dd, Perms.Read, ff)
dd = _Desc('/pop/localhost/msgid/1')
handle  = handler.open(dd, Perms.Read, ff)

open('dummy', 'w').writelines(handle.readlines())
print handler.unlink(handle.myDesc)

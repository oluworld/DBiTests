from AppWorks.File.POPFolder import POPFolder
from AppWorks.File import Perms, Flags

class _Desc:
	def __init__(self, path):
		self.path = path

handler = POPFolder()
dd = _Desc('/pop/localhost/login/etoffi/foo')
ff = Flags()
handle  = handler.open(dd, Perms.Read, ff)
dd = _Desc('/pop/localhost/msgnum/1')
handle  = handler.open(dd, Perms.Read, ff)

open('dummy', 'w').writelines(map(lambda b : '%s\012' %b, handle.readlines()))
print handler.unlink(handle.myDesc)

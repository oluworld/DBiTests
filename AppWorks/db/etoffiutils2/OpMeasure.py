import time
from etoffiutils2.pkg import tt, ttp, combine_lists, xpmt, xmpta, true, false

class OpMeasure:
	def __init__(self,f,l,t,c):
		#~ self.f=f
		self.l=l
		self.t=t
		self.c=c
		self._closed = false
		self.d=time.clock()
	#~ def __del__(self):
		#~ self.close()
	#~ def close(self):
		#~ if self._closed == false:
			#~ if self.remaining() == 0:
				#~ xmpta ('')
			#~ self._closed = true
	def xstartOp(self, each, v):
		xpmt (v)
		self.startOp(each)
	def startOp(self, each):
		self.c+=1
		#~ print '765',self.c,self.t
		assert self.c <= self.t
		xmpta ('%d of %d (%d left) [%d .. %d] (%f%%) %f' % (self.c, self.t, 
			self.remaining(), each, self.l+1,      # (%d left) [%d .. %d]
			(100*(float(self.c)/float(self.t))),   # (%f%%)
			self.elapsed_time()))                  # %f
	def endOp(self):
		self.d=time.clock()
	def remaining(self):
		return (self.t-self.c)
	def elapsed_time(self):
		return time.clock()-self.d

class Measurer:
	def xgo(self, l, v):
		xpmt(v)
		self.go(l)
	def go(self, l):
		count = len(l)
		measure = OpMeasure(1,count-1,count,0)
		for each in xrange(0, count):
			measure.startOp(each+1)
			l[each].doit()
			measure.endOp()

#
# eof
#

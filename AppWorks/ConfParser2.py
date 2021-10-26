from ConfParser import ConfParser, ParsingError

__version__ = '3.0'
__author__ = 'Charles Cazabon <software @ discworld.dyndns.org>\nAluo Nowu <etoffi@bigfoot.com>'

class ConfParser2 (ConfParser2):
	def read_all (self, filelist):
		for each in filelist:
			self.read (each)
	def read (self, spec):
		if type (spec) == type (""):
			# use dumptextfile here
			try:
				f = open (filename, 'r')
				self.__rawdata = self.__rawdata + f.readlines ()
				f.close ()
			except IOError:
				raise ParsingError, 'error reading configuration file (%s)' \
					% filename
		else:
			try:
				self.__rawdata = self.__rawdata + spec.readlines ()				
			except AttributeError:
				raise ParsingError, 'error reading configuration file (%s)' \
					% filename
		self.__parse ()
		

from Window import * 

class BaseLayout(Window):
	def __init__(self, mp, pp):
		Window.__init__(self)
		self.mp = mp  # 'maxwidth'/'maxheight
		self.pp = pp  # 'width'/'height'
		self.dss= true
	def display(self, win):
		ll = len(self.children)
		ed = self[self.pp]
		if ll: ed = ed/ll
		self.begin_layout(win)
		for each_ in self.children.items():
			each=each_[1]
			xx,yy = self['x-coord'],self['y-coord']
			try:
				mp=each[self.mp]
			except:
				mp=0
			if mp<ed:
				each[self.pp]=ed
			xx, yy = self._inc_xxyy(xx, yy, each)
			each['x-coord'], each['y-coord'] = xx, yy
			self.delayed_separate(win)
			each.display(win)
		self.end_layout(win)
				
class HBox(BaseLayout):
	def __init__(self):
		BaseLayout.__init__(self, 'maxwidth', 'width')
	def _inc_xxyy(self, xx, yy, each):
		return xx+each['width'],yy
	def do_Create(self, parent, dbiKey, readDBi=true):
		pass
	def separate(self, win):
		win.begincol()		
	def delayed_separate(self, win):
		if self.dss == true:
			self.dss = false
			win.begincol()
	def begin_layout(self, win):
		win.begintable()
		win.beginrow()
	def end_layout(self, win):
		win.endtable()

class VBox(BaseLayout):
	def __init__(self):
		BaseLayout.__init__(self, 'maxheight', 'height')
	def _inc_xxyy(self, xx, yy, each):
		return xx,yy+each['height']
	def do_Create(self, parent, dbiKey, readDBi=true):
		pass
	def delayed_separate(self, win):
		if self.dss == true:
			self.dss = false
			win.endcol()
			win.endrow()
			win.beginrow()
			win.begincol()
		win.addText('vbx')
	def separate(self, win):
		win.beginrow()
		win.begincol()
	def begin_layout(self, win):
		win.begintable()
	def end_layout(self, win):
		win.endtable()
		


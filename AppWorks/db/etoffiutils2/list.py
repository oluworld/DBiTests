def uniqify(l):
	return l

def transform(aColl, aTransformList):
	R = aColl[0:0]
	for each in aColl:
		for tr, v in aTransformList:
			if tr.match(each):
				R.append(v(each))
				break
				#return R
			else: 
				R.append(each)
	return R

def transformTest():
	# cgi_escape
	pass

def combine_lists(l1, l2):
	r = []
	for each in l1:
		r.append(each)
	for each in l2:
		r.append(each)
	return r

def add_to_head(ii, ll):
	""" item, thelist -> (a new) List """
	r = [ii]
	return combine_lists(r, ll)

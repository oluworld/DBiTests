from etoffiutils import quickWrite, b64_encode, qpi_encode, x2_encode, ensure_directory_present, true, false
from AppWorks.Jobs import Job
from AppWorks.Chan.MailExtract import MailExtract
import time, string

#
# OnetAddNewsgroupMessage.py
# --------------------------
#
# j.spec_list ->
# 	server, group_name, msgnum, options
# j.spec_list['options'] ->
#	store-in-filesystem
#	mangle-server-name
#	mangle-group-name
#	save-headers
#	extract-contents
#	delete-orig
# j.params ->
#	(msg_lines, oixfs_attr_dict)
#		|			+-> ignored (for now...)
#		+---> obvious
#

mangle_name = b64_encode

def print_spec_list(sl):
	for each in sl.keys():
		print each + '\t\t' + sl[each]

def extract_headers_from_message (msg):
	r = []
	for each in msg:
#		print each
		if each == '':
			break
		r.append (each)
	return r

def get_news_msg_st_root ():
	return 'c:/_'

def get_onet_base (x):
	return 'e:/_onet/by-%s' % x
def res_id_to_path (x):
	return x.replace ('-','/')

def today_date():
	r = time.strftime('%Y-%b-%d (%H%M)', time.localtime(time.time()))
	return r

def extract_info_from_msg (headers):
	h = {}
	for each in headers:
		p = each.index (':')
		h[each[:p].lower()]=each[p+1:]
#		print each[:p], each[p+1:]

	aa = h['from']
	author, author_email = '', ''
	aa = aa.split()
	if len(aa) == 2:
		author, author_email = aa[0], aa[1]
	else:
		author, author_email = aa[0][:aa[0].find('@')], aa[0]
	msgid, date, posting_host = (h['message-id'], h['date'], h['nntp-posting-host'] or '')

	return  author, author_email, msgid, date, posting_host 

def do_job(j, jm):
	print 'OnetAddNewsgroupMessage ======================================================='

#	print j.job_type
	print_spec_list (j.spec_list)

	msg_lines = j.params[0]	
	oix_attrs = j.params[1]	
	
	server = j.spec_list['server']
	msgnum = j.spec_list['msgnum']
	grpnam = j.spec_list['group_name']

	xserver, xgrpnam = server, grpnam

#	s = j.spec_list['options']
	l = j.spec_list['options'].split()

##	print oix_attrs

	delete_orig = 0
	extract_contents = 0
	
	if len(l):

#		store-in-filesystem
#		mangle-server-name
#		mangle-group-name
#		save-headers

		if "mangle-server-name" in l:
			xserver = mangle_name (server)
		if "mangle-group-name" in l:
			xgrpnam = mangle_name (grpnam)
		if "delete-orig" in l:
			delete_orig = 1
		if "extract-contents" in l:
			extract_contents = 1
		if "store-in-filesystem" in l:
	
			dl = '%s/%s/%s/' % (get_news_msg_st_root(), xserver, xgrpnam)
			ensure_directory_present (dl)
			sl = dl + msgnum
			quickWrite (sl, msg_lines, true)
			
			if "save-headers" in l:
				quickWrite (sl+".headers", extract_headers_from_message (msg_lines), true)

	base = get_onet_base ('basic-resource-id')
	resid = 'OnetAddNewsgroupMessage1-%s-%s-%s' % (xserver, xgrpnam, msgnum)
	fn_ = '%s/%s' % (base, res_id_to_path (resid))
	ensure_directory_present (fn_)
	fn = '%s/%s' % (fn_, msgnum)

	# -------------------
	#  start writing xml
	# -------------------

	if not delete_orig:
		quickWrite (fn, msg_lines, true)

	dpyname = '%s in %s at %s' % (msgnum, grpnam, server)
	headers = extract_headers_from_message (msg_lines)
	author, author_email, msgid, date, posting_host = extract_info_from_msg (headers)
	keywords = ''
	modelist = ''
	storage_location = msgnum+'.msg'
	if "save-headers" not in l:
		headers = None

	out = """<?xml version="1.0"?>
<file basic-resource-id="%s" displayname="%s">
	<type simple-mime="image/jpeg" complex-mime="image/jpeg" />
	<versions>
		<version v="1.0">
			<author name="%s" email="%s" ipaddy="%s" />
			<submittor logon="OnetAddNewsgroupMessage" ipaddy="127.0.0.1" date="%s" />
			<storage location="%s" />
		</version>
	</versions>
	<permissions order="allow, deny">
		<grant name="class:modify" to="user:GetNews" />
		<grant name="class:view" to="user:*" />
	</permissions>
	<keywords>
		%s
	</keywords>
	<modelist>
		%s
	</modelist>
	<properties>
		<property name="datetime" simple-type="string" complex-type="time/internet">
			%s
		</property>
		<property name="Message-ID" simple-type="string" complex-type="rfc822/message-id">
			%s
		</property>	
	"""	% 	(resid, dpyname, author, author_email, posting_host, today_date(), 
				storage_location, keywords, modelist, date, qpi_encode(msgid)
			)
	if headers != None:
		out += """		<property name="rfc822-header" author="user:GetNews" type="long_string">
%s
		</property>""" % (string.join (map(lambda x: x2_encode(x), headers)))
	out += """</properties>\n</file>\n"""

	quickWrite (fn+".onet", [out], false)
	
	# --------------------
	#  finish writing xml
	# --------------------

	if extract_contents == 1:
		me2 = MailExtract()
		me2.set_outdir (fn_)
		me2.do_decode_lines (msg_lines)
		

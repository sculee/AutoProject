import urllib
import urllib2
import json
import getopt
import sys

def postJson(path,url):
	if ""==path or ""==url:
		return
	
	values = ""
	jstr = ""

	with open(path,"r") as f:
		for line in f.readlines():
			jstr = jstr + line.strip()

	values = json.loads(jstr)
	jdata = json.dumps(values)

	req = urllib2.Request(url,jdata)

	req.add_header("Content-Type","application/json")
	req.add_header("appType","true")
#	print "++++++++++++++++++++"
#	print values
#	print url
	response = urllib2.urlopen(req)

	page = response.read()

#	print page

	return page

def postHeader(head,path,url):
	if ""==path or ""==url:
		return
	
	values = ""
	jstr = ""
	header = ""

	with open(path,"r") as f:
		for line in f.readlines():
			jstr = jstr + line.strip()
	
	with open(head,"r") as f:
		for line in f.readlines():
			header = header + line.strip()

	values = json.loads(jstr)#complie json body
	jdata = json.dumps(values)

	jhead = json.loads(header)#compile  request header
	jkey = jhead.keys()
	jvalue = jhead.values()

	req = urllib2.Request(url,jdata)

	jsize = len(jkey)
	
	for i in jsize:
		req.add_header(jkey[i],jvalue[i])#build request header

#	req.add_header("Content-Type","application/json")
#	req.add_header("appType","true")
#	print values
#	print url
	response = urllib2.urlopen(req)

	page = response.read()

#	print page
	return page

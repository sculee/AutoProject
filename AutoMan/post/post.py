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
	print "++++++++++++++++++++"
	print values
	print url
	response = urllib2.urlopen(req)

	page = response.read()

	print page

	return page


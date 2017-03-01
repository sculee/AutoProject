import urllib
import urllib2
import json
import getopt
import sys
import cookielib

def request(url,head="",path="",cookieFile=""):
	if ""==url:
		return
	
	values = ""
	jstr = ""
	header = ""
	jdata = ""#post body
	jsize = 0#header size
	jkey = ""#header keys
	jvalue = ""#header values

	try:
		with open(path,"r") as f:
			for line in f.readlines():
				jstr = jstr + line.strip()
	
		values = json.loads(jstr)#complie json body
		jdata = json.dumps(values)
	except IOError:
		jdata = ""	

	try:
		with open(head,"r") as f:
			for line in f.readlines():
				header = header + line.strip()


		jhead = json.loads(header)#compiled request header
		jkey = jhead.keys()
		jvalue = jhead.values()
		jsize = len(jkey)
	
	except IOError:
		pass


	if cookieFile == "":
		cookieFile = "cookie"

	try:

		cookie = cookielib.MozillaCookieJar()
		cookie.load(cookieFile, ignore_discard=True, ignore_expires=True)
		if "" == jdata:
			req = urllib2.Request(url)
		else:
			req = urllib2.Request(url,jdata)

		for i in range(jsize):
			req.add_header(jkey[i],jvalue[i])#build request header

		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		response = opener.open(req)
	except IOError:
		cookie = cookielib.MozillaCookieJar(cookieFile)
		handler = urllib2.HTTPCookieProcessor(cookie)
		opener = urllib2.build_opener(handler)

		if "" == jdata:
			req = urllib2.Request(url)
		else:
			req = urllib2.Request(url,jdata)
		for i in range(jsize):
			req.add_header(jkey[i],jvalue[i])#build request header

		response = opener.open(req)
		cookie.save(ignore_discard=True, ignore_expires=True)
		


	page = response.read()

#	print page
	return page

if __name__ == "__main__":
#	request("http://testcheckout.shishike.com/checkout_biz/channel/orgcfg/cfg/get")
#	request("http://www.baidu.com")
	request("http://gld.weixin.keruyun.com/user/login.json?shopId=810007772&mobile=13980691506&code=1234&timeStamp=1487581612605&fromBrand=1")

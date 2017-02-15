#coding=utf-8
from django.http import JsonResponse
from django.http import Http404,HttpResponse
from django.template.loader import get_template
from django.template import Context
import MySQLdb
import json
from addtion.search import getJson,getKey
from addtion import search
from addtion.parse import parseFunc
import time
import os
from  post import post

def hello(request):
	ua = request.META.get("HTTP_USER_AGENT","unknown")
	return HttpResponse("hello world, your browser is: %s" %ua);

def count(request):
	with open("count.txt","a") as f:
		print "+++++++++in counting++++++++++"
		f.write("1")
		f.write("\n")
	return HttpResponse("success")


def greet(request,name):
	html = "<html><body>hello %s</body></html>" %name
	return HttpResponse(html);


def indexPage(request):
	nameList = ["Bill","Bob","Stiff"];
	t = get_template("index/index.html");
	html = t.render(Context({"name_list":nameList}));
	return HttpResponse(html);


def query(request):
	db = MySQLdb.connect(user = "root",db = "mysql", passwd="123456",host="localhost");
	cursor = db.cursor();
	cursor.execute("select * from threads");
	data = [row[0] for row in cursor.fetchall()]
	db.close()
	t = get_template("index/index.html")
	html = t.render(Context({"name_list":data}));
	return HttpResponse(html);


def search_form(request):
	t = get_template("search/search_form.html")
	html = t.render()
	return HttpResponse(html)


def search(request):
	if "q" in request.GET and request.GET["q"] != "":
		message = "you searched for: %r" %request.GET["q"]
	else:
		message = "you submitted an empty form"
	
	return HttpResponse(message)

#接口自动化页面start
def compilePage(request):
	t = get_template("index/compile.html")
	html = t.render()
	return HttpResponse(html)


def edit(request):
	t = get_template("index/edit.html")
	html = t.render()
	return HttpResponse(html)


def compileFun(request):
	if "testcase" in request.GET and request.GET["testcase"] != "":
#		print "++++++++++time:"+str(time.mktime(time.ctime()))+"++++++++++++++"
		case = request.GET["testcase"]
		with open("case/temp","w") as w:
			w.write(case)
		parseFunc.getFunc("AutoMan/addtion/func.xml")
#		os.chdir("./AutoMan/addtion/parse/")
		parseFunc.parseFunc("case/temp")
		text = ""
		with open("case/temp.result","r") as f:
			for line in f.readlines():
				text = text + line
#		print "++++++++++++case:"+case+"+++++++++++++++++"
		t = get_template("index/compile.html")
		html = t.render(Context({"message":case,"compiled":text}));
		return HttpResponse(html)
	else:
		t = get_template("index/compile.html")
		html = t.render()
		return HttpResponse(html)
#		print "++++++++++++++in else+++++++++++++++"
#		pass
		

def save(request):
	if "case" in request.GET and request.GET["case"] != "" and "filename" in request.GET and request.GET["filename"] != "":
		case = request.GET["case"]
		path = "case/"+ request.GET["filename"]
		os.system("mkdir "+ path)#create testcase dir
		with open(path + "/testcase",'w') as f:
			f.write(case)
		jstr = '{"code":"OK"}'
		jdata = json.loads(jstr)
		return JsonResponse(jdata)
	

def hint(request):
#	print "++++++++++key:"+request.GET["key"]+"++++++++++"
	if "key" in request.GET and request.GET["key"] != "":
		keyword = request.GET["key"]
		temp = getKey(keyword,"$")
		s = getJson(temp)
#		print "+++++++++++json:"+temp+"+++++++++++++"
		return JsonResponse(s)
        else:
		return json.loads('{"key":[]}')

def result(request):
	print "+++++++++++result+++++++++++++"
	t = get_template("index/result.html")
	html = t.render()
	return HttpResponse(html)
	


def postJdata(request):
	if "url" in request.GET and request.GET["url"] != "" and "testcase" in request.GET and request.GET["testcase"] != "":
		url = request.GET["url"]
		case = request.GET["testcase"]
		with open("case/temp","w") as w:
			w.write(case)
		parseFunc.getFunc("AutoMan/addtion/func.xml")
		parseFunc.parseFunc("case/temp")
#		text = ""
#		with open("case/temp.result","r") as f:
#			for line in f.readlines():
#				text = text + line
		page = post.postJson("case/temp.result",url)
#		print page#需要将page组装成返回的页面，但是需要兼容返回回来的不是原本json的情况
		t = get_template("index/result.html")
		html = t.render(Context({"message":page}))
		return HttpResponse(html)
	elif "testcase" in request.GET and request.GET["testcase"] != "":
		case = request.GET["testcase"]
		t = get_template("index/compile.html")
		html = t.render(Context({"message":case}))
		return HttpResponse(html)
	elif "url" in request.GET and request.GET["url"] != "":
		url = request.GET["url"]
		t = get_template("index/compile.html")
		html = t.render(Context({"url":url}))
		return HttpResponse(html)
	else:
		t = get_template("index/compile.html")
		html = t.render()
		return HttpResponse(html)
	
def testHtml(request):
	t = get_template("index/test.html")
	html = t.render()
	return HttpResponse(html)
	




#接口自动化end

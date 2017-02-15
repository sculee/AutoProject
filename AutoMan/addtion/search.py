#coding=utf-8
import os
import sys
import xml.dom.minidom
from xml.dom.minidom import parse
import json

#arr = ["get","id","xpath","wget","idf"]
arr = []


def getFunc(file):#从xml中读取映射关系
        DOMTree = xml.dom.minidom.parse(file)
        collection = DOMTree.documentElement

        keys = collection.getElementsByTagName("key")

        for elem in keys:
                key = str(elem.getAttribute("name"))
		arr.append(key)


def search(key):
	res = []
	for temp in arr:
		try:
			pos = temp.index(key)
			if 0 == pos:
				res.append(temp)
		except ValueError as e:
			pass
	return res

def getKey(case,key):
	func = case.split(key)
#	print func[-1]
#	print type(func[-1])
	return func[-1]

#if "__main__" == __name__:
#	string = "{key:$fun1(),\nkey2:$fun2(),\nkey3:$fun3()"
#	getKey(string,"$")


def getJson(word):
	cdir = os.getcwd()
#	print "+++++++++++++++++"+cdir+"++++++++++++++++"
	if 0 == len(arr):
		getFunc("./AutoMan/addtion/func.xml")
	temp = str(search(word)).replace("\'","\"")
	final = '{"key":'+temp+'}'
#	jdata = json.loads("{'key':['query']}")
	jdata = json.loads(final)
#	print jdata
	return jdata

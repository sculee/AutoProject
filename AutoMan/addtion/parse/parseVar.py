#coding=utf-8
from __future__ import division

import time
import sys
import new
import pickle
import xml.dom.minidom
from xml.dom.minidom import parse


from pyparsing import *

#词法定义开始
word = Word(alphas,alphanums)#基础字段

num = Word(alphanums+".")#基础数字,包涵浮点

comma = Word(",")#逗号

varNum = num#函数传参数字

varStr = Word(alphas+"."+"_"+"'"+"\""+" "+"="+alphanums)#实参字符串：复杂字符串(如sql)

var = varNum|varStr#实参：字符串数字

strWord = "\"" + (word|num).setResultsName("dataName") + "\""#字符串

symbol = Word(":")#分号

varName = Word(alphas+"_"+alphanums)#变量定义


funName = word#函数名

func = "$"+funName.setResultsName("funName")+"("+varStr.setResultsName("var")+")"#函数调用


varAssign = "$"+varName.setResultsName("varName")+"="+func.setResultsName("funcName")#变量赋值

arrayElem = "$"+varName.setResultsName("arrayName")+"."+varName.setResultsName("keyName")#字典取值


#词法定义结束


#fun = {"query":"query","date":"dateToStamp"}
#cla = {"query":"sql","date":"stamp"}

fun = {}
cla = {}

def getFunc(file):#从xml中读取映射关系
        DOMTree = xml.dom.minidom.parse(file)
        collection = DOMTree.documentElement

        keys = collection.getElementsByTagName("key")

        for elem in keys:
                key = str(elem.getAttribute("name"))
                valueClass = elem.getElementsByTagName("class")[0].childNodes[0].data
                valueFunc = elem.getElementsByTagName("func")[0].childNodes[0].data
                fun[key] = str(valueFunc)
                cla[key] = str(valueClass)




def callFun(func,var):
	funcMod = __import__(cla.get(func))
	funcClass = getattr(funcMod,cla.get(func))
	
	instance = new.instance(funcClass)
	funName = getattr(funcClass,fun.get(func))
	data = apply(funName,[instance,var])

	return data

class parseError(StandardError):
	pass

def parseFunc(path):

	with open(path,'r') as f:

		match = False#匹配标示

		array = {}#解析后的变量存储

		for line in f.readlines():

			
			try:#变量赋值
				if match == False:
					assign = varAssign.parseString(line)
					value = callFun(assign.funcName.funName,assign.funcName.var)#表达式返回值
					var = assign.varName#变量名
#					data = "in parse var:"+var
#					print "+++++++++begin+++++++++++"
#					array = {}
					array[var] = value
#					array["c"] = "3"
#					print array.get("data")[1][1]
#					output = open("data.dat","wb")
#					pickle.dump(array,output)
#					output.close()
#					read = open("data.dat","rb")
#					data = pickle.load(read)
#					print data
#					print type(data)
#					with open("array.txt.res","w") as w:
#						w.write(array)
#					print "+++++++++++middle+++++++++++"
#					print value
#					print "++++++++++end++++++++++++"
			except ParseException as e:
				pass

			if match:
				match = False
			else:
#				print line
				pass

#		print "+++++++++++begin+++++++++++"
		array["c"] = "3"
#		print array.get("data")[1][1]
		output = open("data.dat","wb")
		pickle.dump(array,output)
		output.close()
#		print "++++++++++write+++++++++++"
		read = open("data.dat","rb")
		data = pickle.load(read)
		read.close()
#		print data
#		print array.get("data")[1][1]
#		print type(data)
#		print "+++++++++++end+++++++++++"



if "__main__" == __name__:
	getFunc("../func.xml")
	parseFunc("var.txt")
#	with open("array.txt","r") as f:
#		for line in f.readlines():
#			array = tuple(line)
#			print type(array)
#			print array
			

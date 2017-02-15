#coding=utf-8
from __future__ import division

import time
import sys
import new
import pickle
import xml.dom.minidom
from xml.dom.minidom import parse
import os


from pyparsing import *

#词法定义开始
word = Word(alphas,alphanums)#基础字段

num = Word(alphanums+".")#基础数字,包涵浮点

comma = Word(",")#逗号

varNum = num#函数传参数字

varStr = Word(alphas+"."+"_"+"'"+"\""+" "+"="+alphanums)#复杂字符串(如sql)

var = varNum|varStr

strWord = "\"" + (word|num).setResultsName("dataName") + "\""#字符串

symbol = Word(":")#分号

funName = word#函数名

varWord = Word(alphas+"_")#变量名定义

varName = "$" + varWord.setResultsName("varName")#变量定义

varData = strWord.setResultsName("data") + symbol + varName.setResultsName("var") + comma#变量中段取值

varEnd = strWord.setResultsName("data") + symbol + varName.setResultsName("var")#变量尾段取值

arrayData = strWord.setResultsName("data") + symbol + varName.setResultsName("var") + "[" + varNum.setResultsName("index") + "]" + comma#数组中段取值

arrayEnd = strWord.setResultsName("data") + symbol + varName.setResultsName("var") + "[" + varNum.setResultsName("index") + "]"#数组尾段取值

doubleArrayData = strWord.setResultsName("data") + symbol + varName.setResultsName("var") + "[" + varNum.setResultsName("index") + "]" + "[" + varNum.setResultsName("index2") + "]" + comma#二维数组中段取值

doubleArrayEnd = strWord.setResultsName("data") + symbol + varName.setResultsName("var") + "[" + varNum.setResultsName("index") + "]" + "[" + varNum.setResultsName("index2") + "]"#二维数组尾段取值

func = "$"+funName.setResultsName("funName")+"("+varStr.setResultsName("var")+")"#函数调用

funcf = "$"+funName.setResultsName("funfName")+"("+func.setResultsName("funfVar")+")"#多重函数调用

funcData = strWord.setResultsName("data") + symbol + func.setResultsName("fun") + comma#函数中段数据

funcEnd = strWord.setResultsName("data") + symbol + func.setResultsName("fun")#函数尾段数据

funcfData = strWord.setResultsName("data") + symbol + funcf.setResultsName("funf") + comma#多重函数中段数据

funcfEnd = strWord.setResultsName("data") + symbol + funcf.setResultsName("funf")#多重函数尾段数据
#词法定义结束

#fun = {"query":"query","date":"dateToStamp"}
#cla = {"query":"sql","date":"stamp"}

#print type(fun.get("query"))
#print cla


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
#		print type(valueFunc)






def callFun(func,var):#反射调用
#	os.chdir("./AutoMan/addtion/parse/")
	modName = cla.get(func)
	relPath = "AutoMan.addtion.parse."#web工程的相对路径
#	funcMod = __import__(modName+"."+modName,{},{},[modName])
	funcMod = __import__(relPath+modName+"."+modName,{},{},[modName])
	print "++++++++++++++moudle:"+str(funcMod)
	funcClass = getattr(funcMod,cla.get(func))
	
	instance = new.instance(funcClass)
	funName = getattr(funcClass,fun.get(func))
#	print type(var)
	data = apply(funName,[instance,var])
	return data

class parseError(StandardError):
	pass



def parseFunc(path):#语法解析

	objectFile = path + ".result"
	result = open(objectFile,"w")
#	result = open("temp.result","w")

	with open(path,'r') as f:

		print "+++++++++++++++++++path:"+path
		match = False#匹配标示

		for line in f.readlines():


			try:#函数中段数据分析
				if match == False:
					jdata = funcData.parseString(line)
					data = callFun(jdata.fun.funName,jdata.fun.var)
					json = "\"" + jdata.data.dataName + "\"" + ":" + "\"" + str(data) + "\","
					match = True
					print json
					result.write(json)
					result.write("\n")
#			except ParseException as e:
			except :
				pass

			try:#函数尾段数据分析
				if match == False:
					jdata = funcEnd.parseString(line)
#					os.chdir("./AutoMan/addtion/parse/")
					data = callFun(jdata.fun.funName,jdata.fun.var)
					json = "\"" + jdata.data.dataName + "\"" + ":" + "\"" + str(data) + "\""
					match = True
					print json
					result.write(json)
					result.write("\n")
#			except ParseException as e:
			except :
				pass

			try:#多重函数中段数据分析
				if match == False:
					jdata = funcfEnd.parseString(line)
					varFun = jdata.funf.funfVar.funName
					varVar = jdata.funf.funfVar.var
					fun = jdata.funf.funfName
					var = callFun(varFun,varVar)
					data = callFun(jdata.funf.funfName,var)
					jdata = funcfData.parseString(line)
					json = "\"" + jdata.data.dataName + "\"" + ":" + "\"" + str(data) + "\","
					match = True
					print json
					result.write(json)
					result.write("\n")
#			except ParseException as e:
			except :
				pass

			try:#多重函数尾段数据分析
				if match == False:
					jdata = funcfEnd.parseString(line)
					varFun = jdata.funf.funfVar.funName
					varVar = jdata.funf.funfVar.var
					fun = jdata.funf.funfName
					var = callFun(varFun,varVar)
					data = callFun(jdata.funf.funfName,var)
					json = "\"" + jdata.data.dataName + "\"" + ":" + "\"" + str(data) + "\""
					match = True
					print json
					result.write(json)
					result.write("\n")
#			except ParseException as e:
			except :
				pass

			try:#二维数组中段数据分析
				if match == False:
					jdata = doubleArrayData.parseString(line)
					fileName = path + ".dat"
					read = open(fileName,"rb")
					dic = pickle.load(read)
					read.close()
					data = dic.get(jdata.var.varName)
					index = int(jdata.index)
					index2 = int(jdata.index2)
					json = "\"" + jdata.data.dataName + "\"" + ":" + "\"" + str(data[index][index2]) + "\"" + ","
					match = True
					print json
					result.write(json)
					result.write("\n")
#			except ParseException as e:
			except :
				pass

			try:#二维数组尾段数据分析
				if match == False:
					jdata = doubleArrayEnd.parseString(line)
					fileName = path + ".dat"
					read = open(fileName,"rb")
					dic = pickle.load(read)
					read.close()
					data = dic.get(jdata.var.varName)
					index = int(jdata.index)
					index2 = int(jdata.index2)
					json = "\"" + jdata.data.dataName + "\"" + ":" + "\"" + str(data[index][index2]) + "\""
					match = True
					print json
					result.write(json)
					result.write("\n")
#			except ParseException as e:
			except :
				pass

			try:#数组中段数据分析
				if match == False:
					jdata = arrayData.parseString(line)
					fileName = path + ".dat"
					read = open(fileName,"rb")
					dic = pickle.load(read)
					read.close()
					data = dic.get(jdata.var.varName)
					index = int(jdata.index)
					json = "\"" + jdata.data.dataName + "\"" + ":" + "\"" + str(data[index]) + "\"" + ","
					match = True
					print json
					result.write(json)
					result.write("\n")
#			except ParseException as e:
			except :
				pass

			try:#数组尾段数据分析
				if match == False:
					jdata = arrayData.parseString(line)
					fileName = path + ".dat"
					read = open(fileName,"rb")
					dic = pickle.load(read)
					read.close()
					data = dic.get(jdata.var.varName)
					index = int(jdata.index)
					json = "\"" + jdata.data.dataName + "\"" + ":" + "\"" + str(data[index]) + "\"" 
					match = True
					print json
					result.write(json)
					result.write("\n")
#			except ParseException as e:
			except :
				pass

			try:#变量中段数据分析
				if match == False:
					jdata = varData.parseString(line)
					fileName = path + ".dat"
					read = open(fileName,"rb")
					dic = pickle.load(read)
					read.close()
					data = dic.get(jdata.var.varName)
					json = "\"" + jdata.data.dataName + "\"" + ":" + "\"" + str(data) + "\"" + ","
					match = True
					print json
					result.write(json)
					result.write("\n")
#			except ParseException as e:
			except :
				pass

			try:#变量尾段数据分析
				if match == False:
					jdata = varEnd.parseString(line)
					fileName = path + ".dat"
					read = open(fileName,"rb")
					data = dic.get(jdata.var.varName)
					json = "\"" + jdata.data.dataName + "\"" + ":" + "\"" + str(data) + "\"" + ","
					match = True
					print json
					result.write(json)
					result.write("\n")
#			except ParseException as e:
			except:
				pass



			if match:
				match = False
			else:
				print line
				result.write(line)
				result.write("\n")

if "__main__" == __name__:


	getFunc("../func.xml")
	parseFunc("json.txt")
#	json = "\"abcd\":$ce(a)"
#	print json
#	data = varEnd.parseString(json)
#	print data.var

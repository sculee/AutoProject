import time
import sys
import new

if "__main__" == __name__:
	rMod = __import__("sql")

	rClass = getattr(rMod,"sql")
	print rClass
	print type(rClass)
	obj = new.instance(rClass)
	objFunc = getattr(rClass,"query")
	data = apply(objFunc,[obj,"SELECT client_update_time FROM trade WHERE id = 620854"])
	print data

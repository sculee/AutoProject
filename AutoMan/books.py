from django.http import HttpResponse
from django.http import Http404,HttpResponse
from django.template.loader import get_template
from django.template import Context
import MySQLdb
from AutoApp.models import Book

def hello(request):
	ua = request.META.get("HTTP_USER_AGENT","unknown")
	return HttpResponse("hello world, your browser is: %s" %ua);


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
#		message = "you searched for: %r" %request.GET["q"]
		q = request.GET['q']
		books = Book.objects.filter(title__icontains=q)
		t = get_template("search/search_results.html")
		html = t.render(Context({"books":books,"q":q}))
		return HttpResponse(html)
	else:
#		message = "you submitted an empty form"
		t = get_template("search/search_form.html")
#		message = "may you give us some sugestion"
		message = ""
		html = t.render(Context({"error":True,"message":message}))
		return HttpResponse(html)
	
#	return HttpResponse(message)

"""AutoMan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
#from AutoMan.view import hello,greet,indexPage
from AutoMan import view


#from AutoMan import books
#import AutoMan.view
from django.contrib import admin
admin.autodiscover();

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^hello/$',view.hello),
	url(r'^index/$',view.indexPage),
	url(r'^greet/name/([A-Za-z]*)/$',view.greet),
#	url(r'^search-form/$',books.search_form),
#	url(r'^search/$',books.search),
#	url(r'^edit/$',view.compilePage),
#	url(r'^link/$',view.returnJson),
	url(r'^hint/$',view.hint),
#	url(r'^edit/$',view.edit),
	url(r'^save/$',view.save),
	url(r'^compile/$',view.compileFun),
	url(r'^$',view.compileFun),
	url(r'^result/$',view.result),
	url(r'^post/$',view.postJdata),
	url(r'^test/$',view.testHtml),
	url(r'^count/$',view.count),
]

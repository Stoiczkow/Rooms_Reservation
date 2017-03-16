"""contact_box URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from contacts.views import *
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^all/', show_all_contacts),
    url(r'^new/', NewContact.as_view()),
    url(r'^modify/(?P<id>(\d+))', ModifyContact.as_view()),
    url(r'^delete/(?P<id>(\d+))', DeleteContact.as_view()),
    url(r'^show/(?P<id>(\d+))', ShowOne.as_view()),
]

from django.conf.urls import url
from django.contrib import admin

from .views import (
	careers_list,
	careers_create,
	careers_detail,
	careers_update,
	careers_delete
	)

urlpatterns = [

    url(r'^$', careers_list, name = 'list'),
    url(r'^create/$', careers_create, name = 'create'),
    url(r'^(?P<slug>[\w-]+)/$', careers_detail, name = 'detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', careers_update, name = 'update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', careers_delete,  name = 'delete'),
]
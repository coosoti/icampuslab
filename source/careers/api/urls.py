from django.conf.urls import url
from django.contrib import admin

from .views import (
	CareerCreateAPIView,
	CareerListAPIView,
	CareerDetailAPIView,
	CareerDeleteAPIView,
	CareerUpdateAPIView,
	)

urlpatterns = [

    url(r'^$', CareerListAPIView.as_view(), name = 'list'),
    url(r'^create/$', CareerCreateAPIView.as_view(), name = 'create'),
    url(r'^(?P<slug>[\w-]+)/$', CareerDetailAPIView.as_view(), name = 'detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', CareerUpdateAPIView.as_view(), name = 'update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', CareerDeleteAPIView.as_view(),  name = 'delete'),
]
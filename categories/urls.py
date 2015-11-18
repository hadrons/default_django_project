#coding: utf-8
from django.conf.urls import patterns, url

from .views import CategoryListView, CategoryCreateView, CategoryUpdateView

urlpatterns = patterns('',
	url(r'^$', CategoryListView.as_view(), name='categories_list'),
	url(r'^nova/$', CategoryCreateView.as_view(), name='category_create'),
	url(r'^(?P<pk>\d+)/editar/$', CategoryUpdateView.as_view(), name='category_update'),
)
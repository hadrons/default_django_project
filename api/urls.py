#coding: utf-8
from django.conf.urls import include, url
from . import DefaultRouter

from rest_framework.authtoken import views
from people.views import PersonViewSet, PersonUpdateView, ObtainAuthToken

router = DefaultRouter()

router.register(r'people', PersonViewSet.as_view(), base_name='people')

helper_patterns = [

    url(r'^api-auth/$', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/$', ObtainAuthToken.as_view()),
    
    url(r'^people/$', PersonViewSet.as_view(), name='people'),
    url(r'^people/(?P<pk>[0-9]+)/$', PersonUpdateView.as_view()),
]

urlpatterns = helper_patterns
urlpatterns.extend(router.urls)
from django.conf.urls import url
from snippets import SnippetViewSet, UserViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers

snippet_list = SnippetViewSet.as_view({
	'get': 'list',
	'post': 'create'
	})

snippet_detail = SnippetViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
	})

snippet_highlight = SnippetViewSet.as_view({
	'get':'highlight'
	}, render_classes=[renderers.StaticHTMLRenderer])

user_list = UserViewSet.as_view({
	'get': 'list'
	})

user_detail = UserViewSet.as_view({
	'get': 'retrieve'
	})

urlpatterns = [
#	url(r'^snippets/$', views.snippet_list),
#	url(r'^snippets/(?P<pk>[0-9]+)/$', views.snippet_detail),
	url(r'^snippets/$', snippet_list, name='snippet-list'),
	url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
	url(r'^users/$', user_list, name='user-list'),
	url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
	url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
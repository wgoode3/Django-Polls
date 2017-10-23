from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^users/new$', views.new_user),
	url(r'^session/new$', views.new_session),
	url(r'^session/delete$', views.logout),
	url(r'^polls$', views.polls),
	url(r'^polls/new$', views.new_poll),
	url(r'^vote/(?P<id>\d+)$', views.vote)
]
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register_user$', views.register),
    url(r'^success$', views.success),
    url(r'^sessions$', views.login),
    url(r'^logout$', views.logout),
    url(r'^submit$', views.submit),
    url(r'^my_list/(?P<id>\d+)$', views.my_list),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^user_profile/(?P<id>\d+)$', views.user_profile),
    url(r'^dashboard$', views.dashboard),

 ]

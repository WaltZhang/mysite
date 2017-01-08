from django.conf.urls import url
from . import views


app_name = 'discovery'
urlpatterns = [
    url(r'^$', views.login_user, name='login_user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^projects/$', views.projects, name='projects'),
    url(r'^project/(?P<pk>\d+)/$', views.ProjectView.as_view(), name='project'),
    url(r'^datasets/$', views.datasets, name='datasets'),
    url(r'^daatset/(?P<pk>\d+)/$', views.DatasetView, name='dataset'),
    url(r'^save/$', views.save_aqi, name='save'),
    url(r'^load/$', views.load_aqi, name='load'),
]

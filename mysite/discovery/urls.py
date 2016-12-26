from django.conf.urls import url
from . import views


app_name = 'discovery'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^$', views.projects, name='projects'),
    url(r'^project/(?P<pk>\d+)/$', views.ProjectView.as_view(), name='project'),
]

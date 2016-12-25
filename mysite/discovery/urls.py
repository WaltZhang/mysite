from django.conf.urls import url
from . import views


app_name = 'discovery'
urlpatterns = [
    url(r'^$', views.projects, name='projects'),
    url(r'^project/(?P<pk>\d+)/$', views.ProjectView.as_view(), name='project'),
]

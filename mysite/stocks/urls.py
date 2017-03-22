from django.conf.urls import url
from . import views

app_name = 'stocks'

urlpatterns = [
    url(r'^$', views.InvestmentView.as_view(), name='investments'),
    url(r'^(?P<pk>\d+)/$', views.StockView.as_view(), name='stock'),
    url(r'^(?P<pk>\d+)/delete/$', views.InvestmentDelete.as_view(), name='delete'),
]

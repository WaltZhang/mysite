from django.conf.urls import url
from stocks.views import StockView

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', StockView.as_view(), name='stocks'),
]

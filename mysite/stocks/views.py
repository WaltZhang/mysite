from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.


class StockView(ListView):
    template_name = 'stocks/stocks.html'
    context_object_name = 'stock_list'

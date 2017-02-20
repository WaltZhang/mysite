from django.shortcuts import render
from django.views.generic import ListView
from datetime import datetime
from .models import StockModel
from .provision import StockProvider


class StockView(ListView):
    template_name = 'stocks/stocks.html'
    context_object_name = 'stock_list'


def refresh(code):
    stock_list = StockModel.objects.filter(code=code).order_by('-date')
    if not stock_list:
        today = datetime.today().date()
        if today > stock_list[0].date:
            provider = StockProvider(code, today)
            provider.load_latest_data()


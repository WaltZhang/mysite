from django.contrib import admin
from .models import InvestmentModel, StockModel


admin.site.register(InvestmentModel)
admin.site.register(StockModel)

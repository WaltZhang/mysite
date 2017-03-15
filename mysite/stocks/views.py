from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, TemplateView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import InvestmentModel, StockModel
from .provision import create_investment


class InvestmentView(ListView):
    template_name = 'stocks/stocks.html'
    context_object_name = 'investment_list'

    def get_queryset(self):
        return InvestmentModel.objects.filter(user__username=self.request.user.username)

    def post(self, request, *args, **kwargs):
        try:
            count = StockModel.objects.filter(code=request.POST.get('stock_code')).count()
            if count == 0:

            investment = InvestmentModel.objects.get(code=request.POST.get('stock_code'))
        except ObjectDoesNotExist:
            investment = create_investment(code=request.POST.get('stock_code'), user=self.request.user)
        return HttpResponse(investment)


class StockView(SingleObjectMixin, ListView):
    template_name = 'stocks/stock.html'
    context_object_name = 'stock_list'
    paginate_by = 30

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=InvestmentModel.objects.all())
        return super(StockView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StockView, self).get_context_data(**kwargs)
        context['investment'] = self.object
        return context

    def get_queryset(self):
        return self.object.stockmodel_set.all()


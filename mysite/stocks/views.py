from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, DetailView
from datetime import datetime
from .models import StockModel, InvestmentModel
from .provision import StockProvider


class InvestmentView(ListView):
    template_name = 'stocks/stocks.html'
    context_object_name = 'investment_list'

    def get_queryset(self):
        ivs = InvestmentModel.objects.filter(user__username=self.request.user.username)
        return ivs


class StockView(SingleObjectMixin, ListView):
    template_name = 'stocks/stock.html'
    paginate_by = 30

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=InvestmentModel.objects.all())
        return super(StockModel, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(StockModel, self).get_context_data(**kwargs)
        context['investment'] = self.object

    def get_queryset(self):
        return self.object.stock_set.all()


class StockDetailView(DetailView):
    template_name = 'stocks/detail.html'
    model = StockModel

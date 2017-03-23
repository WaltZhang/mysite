from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView
from django.shortcuts import redirect
from django.views.generic.edit import DeleteView
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from .models import InvestmentModel
from .provision import create_investment


class InvestmentView(ListView):
    template_name = 'stocks/stocks.html'
    context_object_name = 'investment_list'

    def get_queryset(self):
        return InvestmentModel.objects.filter(user__username=self.request.user.username)

    def post(self, request, *args, **kwargs):
        try:
            investment = InvestmentModel.objects.get(code=request.POST.get('stock_code'))
        except ObjectDoesNotExist:
            try:
                investment = create_investment(code=request.POST.get('stock_code'), user=self.request.user)
            except:
                messages.add_message(request, messages.INFO, 'Can not find stock with code: {}'.format(request.POST.get('stock_code')))
                return redirect('stocks:investment')
        return redirect('stocks:stock', investment.id)

    def get_context_data(self, **kwargs):
        context = super(InvestmentView, self).get_context_data(**kwargs)
        storage = messages.get_messages(self.request)
        for message in storage:
            context['error_message'] = message
        return context

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


class InvestmentDelete(DeleteView):
    model = InvestmentModel
    success_url = reverse_lazy('stocks:investment')

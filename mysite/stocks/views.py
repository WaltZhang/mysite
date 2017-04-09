from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import DeleteView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from .models import InvestmentModel
from .provision import create_investment


class InvestmentView(ListView):
    template_name = 'stocks/stocks.html'
    context_object_name = 'investment_list'

    def get_queryset(self):
        return InvestmentModel.objects.filter(user__username=self.request.user.username)

    def get(self, request, *args, **kwargs):
        if request.GET.get('stock_code'):
            try:
                investment = InvestmentModel.objects.get(code=request.GET.get('stock_code'))
            except ObjectDoesNotExist:
                return render(request, 'stocks/waiting.html', {'code': request.GET.get('stock_code')})
                # return redirect('stocks:waiting', code=request.GET.get('stock_code'))
            else:
                return redirect('stocks:stock', pk=investment.id)
        return super(InvestmentView, self).get(request, *args, **kwargs)


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
    success_url = reverse_lazy('stocks:investments')


class WaitingView(TemplateView):
    template_name = 'stocks/waiting.html'

    def get(self, request, *args, **kwargs):
        try:
            investment = create_investment(code=kwargs.get('code'), user=request.user)
        except Exception as e:
            messages.add_message(request, messages.INFO, 'Can not find stock with code: {}'.format(kwargs.get('code')))
        #     return render(request, 'stocks/waiting.html', )
            return super(WaitingView, self).get(request, *args, **kwargs)
        return redirect('stocks:stock', pk=investment.id)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)

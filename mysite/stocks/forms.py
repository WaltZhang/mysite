from django import forms


class StockForm(forms.Form):
    code = forms.CharField(max_length=10, label='Stock Code')

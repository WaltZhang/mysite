from django.db import models
from django.contrib.auth.models import User


class InvestmentModel(models.Model):
    user = models.ForeignKey(User)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.code

    def __repr__(self):
        return self.code


class StockModel(models.Model):
    investment = models.ForeignKey(InvestmentModel)
    code = models.CharField(max_length=10)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    adj_close = models.FloatField()

    def __str__(self):
        return self.code + ' : ' + self.date.strftime('%b %d %Y')

    def __repr__(self):
        return self.code + ' : ' + self.date.strftime('%b %d %Y')

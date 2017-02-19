from django.db import models


class StockModel(models.Model):
    code = models.CharField(max_length=10)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    adj_close = models.FloatField()

    def __str__(self):
        return self.code

    def __unicode__(self):
        return self.code

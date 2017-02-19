from datetime import datetime
from urllib import request, error
from .models import StockModel


class StockProvider(object):
    tmp_file = '/tmp/table.csv'
    stock_url = 'http://table.finance.yahoo.com/table.csv?s={}'

    def __init__(self, stock_code, start_date='1990-12-01'):
        self.stock_code = stock_code
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

    def _get_stock_csv(self):
        url = self.stock_url.format(self.stock_code)
        request.urlretrieve(url, self.tmp_file)

    def load_latest_data(self):
        self._get_stock_csv()
        with open(self.tmp_file) as csv:
            next(csv)
            for row in csv:
                columns = row.split(',')
                column_date = datetime.strptime(columns[0], '%Y-%m-%d').date()
                if column_date > self.start_date:
                    stock = StockModel()
                    stock.code = self.stock_code
                    stock.date = column_date
                    stock.open = float(columns[1])
                    stock.high = float(columns[2])
                    stock.low = float(columns[3])
                    stock.close = float(columns[4])
                    stock.volume = int(columns[5])
                    stock.adj_close = float(columns[6])
                    stock.save()

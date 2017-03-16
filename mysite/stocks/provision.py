from datetime import datetime, date
from urllib import request
from .models import StockModel, InvestmentModel


def create_investment(code, user):
    investment = InvestmentModel.objects.create(code=code, user=user)
    try:
        load_latest_data(investment=investment, code=code)
        return investment
    except:
        investment.delete()
        return None


def _get_stock_csv(code, tmp_file):
    stock_url = 'http://table.finance.yahoo.com/table.csv?s={}'
    url = stock_url.format(code)
    tmp_file, header = request.urlretrieve(url, tmp_file)
    print(header)


def load_latest_data(investment, code, start_date=date(1990, 12, 1)):
    qs = StockModel.objects.filter(code=code)
    if qs.count() == 0:
        tmp_file = '/tmp/table.csv'
        _get_stock_csv(code=code, tmp_file=tmp_file)
        with open(tmp_file) as csv:
            next(csv)
            for row in csv:
                columns = row.split(',')
                column_date = datetime.strptime(columns[0], '%Y-%m-%d').date()
                if column_date > start_date:
                    investment.stockmodel_set.create(
                        investment=investment,
                        code=code,
                        date=column_date,
                        open=float(columns[1]),
                        high=float(columns[2]),
                        low=float(columns[3]),
                        close=float(columns[4]),
                        volume=int(columns[5]),
                        adj_close=float(columns[6])
                    )
    else:
        for q in qs:
            q.investment = investment
            q.save()

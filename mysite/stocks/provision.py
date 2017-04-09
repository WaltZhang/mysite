from datetime import datetime, date
import requests
from .models import StockModel, InvestmentModel


def create_investment(code, user):
    investment = InvestmentModel.objects.create(code=code, user=user)
    try:
        load_stock_data(investment=investment, code=code)
        return investment
    except Exception as e:
        investment.delete()
        raise e


def load_stock_data(investment, code, start_date=date(1990, 12, 1)):
    qs = StockModel.objects.filter(code=code)
    if qs.count() == 0:
        rows = _get_stock_csv(investment=investment, code=code)
        StockModel.objects.bulk_create([
                            StockModel(investment=row['investment'],
                            code=row['code'],
                            date=row['date'],
                            open=row['open'],
                            high=row['high'],
                            low=row['low'],
                            close=row['close'],
                            volume=row['volume'],
                            adj_close=row['adj_close']) for row in rows
        ])
    else:
        qs.update(investment=investment)


def _get_stock_csv(investment, code):
    stock_url = 'http://table.finance.yahoo.com/table.csv?s={}'
    url = stock_url.format(code)
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return _extract_data(response.text, investment, code)
    else:
        raise Exception()


def _extract_data(text, investment, code):
    rows = []
    for line in text.strip().split('\n')[1:]:
        row = {}
        columns = line.split(',')
        row['investment'] = investment
        row['code'] = code
        row['date'] = datetime.strptime(columns[0], '%Y-%m-%d').date()
        row['open'] = float(columns[1])
        row['high'] = float(columns[2])
        row['low'] = float(columns[3])
        row['close'] = float(columns[4])
        row['volume'] = int(columns[5])
        row['adj_close'] = float(columns[6])
        rows.append(row)
    return rows

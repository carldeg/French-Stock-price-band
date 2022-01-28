import time

import yfinance as yf
import pandas_datareader.data as pdr
import datetime as dt


class Markets:

    def __init__(self, stock):
        self.stock = stock
        yf.pdr_override()

    def spot(self):
        end = dt.datetime.today()
        delta = dt.timedelta(days=10)
        beg = end - delta
        price_table = pdr.get_data_yahoo(self.stock, data_source='yahoo', start=beg, end=end, progress=False)['Close']
        spot = round(price_table.iloc[-1], 6)

        return spot


    def close_at(self,date_):

        end = dt.datetime.today()
        delta = dt.timedelta(days=360)
        beg = end - delta
        price_table = pdr.get_data_yahoo(self.stock, data_source='yahoo', start=beg, end=end, progress=False)['Close']

        temp = price_table.index.astype(str).to_list().index(date_)
        close = round(price_table[temp],6)
        return close

    def daily_price_table(self, nb_days):
        end = dt.datetime.today()
        delta = dt.timedelta(days=nb_days)
        beg = end - delta
        price_table = pdr.get_data_yahoo(self.stock, data_source='yahoo', start=beg, end=end, progress=False)['Adj Close']
        #price_table['Volume'] = price_table['Volume'] / 1000000

        return price_table

    def interval_price_table(self, period, interval):
        # period = 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        # interval = 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1w, 1mo, 3mo

        price_table = pdr.get_data_yahoo(
            self.stock,
            data_source='yahoo',
            progress=False,
            period=period,
            interval=interval
        )['Close'].reset_index()

        return price_table


class feed:

    def __init__(self,stock):

        while True:
            print(Markets(stock=stock).spot())

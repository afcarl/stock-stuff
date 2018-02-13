from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators

from pprint import pprint
from s_p_companies import s_p_companies
from utils import *
import threading
import time

alpha_vantage_key = 'ZEBSZMBM169YX5Z7'

KEY_TICKER = '1. symbol'
KEY_PRICE = '2. price'
KEY_VOLUME = '3. volume'
KEY_TIMESTAMP = '4. timestamp'


class ApiLock(object):

    def __init__(self):
        self._lock = threading.RLock()
        self.last_timestamp = 0

    def acquire(self):
        now = time.time()
        wait_time = 1.5 - (now - self.last_timestamp)
        if wait_time > 0.0:
            time.sleep(wait_time)
        self._lock.acquire()

    def release(self):
        self._lock.release()

    def __enter__(self):
        self.acquire()

    def __exit__(self, type, value, traceback):
        self.release()

api_lock = ApiLock()

def get_current_prices(stocks):
    ret = []
    ts = TimeSeries(key=alpha_vantage_key)

    for chunk in chunks(stocks,99):
        with api_lock:
          data, meta_data = ts.get_batch_stock_quotes(chunk)
        ret.extend([float(entry[KEY_PRICE]) for entry in data])
    return ret

def get_current_price(stock):
    return get_current_prices([stock])[0]

def get_s_p_current_prices():
    return get_current_prices(s_p_companies())

def get_rsi(stock, interval='daily', time_period=14, series_type='close'):
    ti = TechIndicators(key=alpha_vantage_key)
    with api_lock:
        data, metadata = ti.get_rsi(stock, interval=interval, time_period=time_period, series_type=series_type)
    pprint(data)

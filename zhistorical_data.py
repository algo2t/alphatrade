import json
from time import sleep
from datetime import datetime, timedelta

# pip install https://github.com/algo2t/alphatrade

from alphatrade import AlphaTrade

import config as config

sas = AlphaTrade(login_id=config.login_id,
                 password=config.password, twofa=config.TOTP)

usd_inr = sas.get_instrument_by_symbol('CDS', 'USDINR SEP FUT')
print(usd_inr)
# print(sas.get_balance())
start_time = datetime(2022, 1, 9, 9, 15, 0)
end_time = datetime.now()

# df = sas.get_historical_candles(
#     'MCX', 'NATURALGAS MAY FUT', start_time, end_time, 5)
# print(df)
# end_time = start_time + timedelta(days=5)
# df = sas.get_historical_candles(
#     'MCX', 'NATURALGAS APR FUT', start_time, end_time, 15)
# print(df)

# # Get Intraday Candles data based on interval - default 5 minute
# df = sas.get_intraday_candles('MCX', 'NATURALGAS MAY FUT')
# print(df)
df = sas.get_intraday_candles('MCX', 'NATURALGAS AUG FUT', 15)
print(df)

# # Get Historical candles data
# print(sas.get_historical_candles('MCX', 'NATURALGAS APR FUT',
#                                  datetime(2020, 10, 19), datetime.now(), interval=30))

# # Get Historical candle for Nifty Bank and India VIX
# india_vix_nse_index = sas.get_instrument_by_symbol('NSE', 'India VIX')
# print(sas.get_historical_candles(india_vix_nse_index.exchange,
#                                  india_vix_nse_index.symbol, datetime(2020, 11, 30), datetime.now(), interval=30, is_index=True))

nifty_bank_nse_index = sas.get_instrument_by_symbol('NSE', 'Nifty Bank')
# print(nifty_bank_nse_index)
print(sas.history(nifty_bank_nse_index, datetime(2022, 2, 2, 9, 15, 0), datetime.now(), interval=30, is_index=True))


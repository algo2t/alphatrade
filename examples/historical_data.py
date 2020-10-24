import json
from time import sleep
from datetime import datetime, timedelta

# pip install https://github.com/algo2t/alphatrade

from alphatrade import AlphaTrade

import config

sas = AlphaTrade(login_id=config.login_id, password=config.password, twofa=config.twofa)

usd_inr = sas.get_instrument_by_symbol('CDS', 'USDINR OCT FUT')
print(usd_inr)
print(sas.get_balance())
start_time = datetime(2020, 10, 19, 9, 15, 0)
end_time = datetime(2020, 10, 21, 16, 59, 0)

df = sas.get_historical_candles('MCX', 'NATURALGAS OCT FUT', start_time, end_time, 5)
print(df)
end_time = start_time + timedelta(days=5)
df = sas.get_historical_candles('MCX', 'NATURALGAS NOV FUT', start_time, end_time, 15)
print(df)

# Get Intraday Candles data based on interval - default 5 minute
df = sas.get_intraday_candles('MCX', 'NATURALGAS OCT FUT')
print(df)
df = sas.get_intraday_candles('MCX', 'NATURALGAS NOV FUT', 15)
print(df)

# Get Historical candles data
print(sas.get_historical_candles('MCX', 'NATURALGAS NOV FUT', datetime(2020, 10, 19), datetime.now() ,interval=30))

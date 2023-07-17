# Python APIs for SAS Online Alpha Trade Web Platform

# MAJOR CHANGES : NEW VERSION 1.0.0

## API endpoints are changed to match the new ones, bugs expected

1. Removed check for enabled exchanges, you can now download or search symbols from MCX as well if it is not enabled
2. TOTP SECRET or TOTP both can be given as argument while creating AlphaTrade object (if it is 6 digits it will conside TOTP else TOTP SECRET)
3. Added new search function to search scrips which will return json for found scrips, you need to process it further
4. More functions to come.
5. Check whether streaming websocket is working or not
6. The `examples` folder is removed and examples are renamed and kept in root directory for ease of development

# STEPS to work

1. Clone the repo locally - `git clone https://github.com/algo2t/alphatrade.git` 
2. Create a virtualenv - `python -m pip install virtualenv` and then `python -m virtualenv venv` and activate the `venv` environment.
3. Install dev-requirement.txt - `python -m pip install -r dev-requirements.txt` - this is to ensure `setuptools==57.5.0` is installed. There is a bug with `protlib`, target is to get reed of `protlib` in future
4. Install requirement.txt - `python -m pip install -r requirement.txt`
5. Create the `config.py` file in root of cloned repo with `login_id`, `password` and `TOTP` SECRET, you can add the `access_token.txt` if you want to use existing `access_token`.
6. Try the examples `python zlogin_example.py`, `python zexample_sas_login.py`, `python zhistorical_data.py` and `python zstreaming_data.py`
7. Expecting issues with the streaming data !!! :P


# NOTE:: This is Unofficial python module, don't ask SAS support team for help, use it AS-IS

The Python APIs for communicating with the SAS Online Alpha Trade Web Platform.

Alpha Trade Python library provides an easy to use python wrapper over the HTTPS APIs.

The HTTP calls have been converted to methods and JSON responses are wrapped into Python-compatible objects.

Websocket connections are handled automatically within the library.

This work is completely based on Python SDK / APIs for [AliceBlueOnline](https://github.com/krishnavelu/alice_blue.git).  
Thanks to [krishnavelu](https://github.com/krishnavelu/).  

- **Author: [algo2t](https://github.com/algo2t/)**
- **Github Repository: [alphatrade](https://github.com/algo2t/alphatrade.git)**

## Installation

This module is installed via pip:

```
pip install git+https://github.com/algo2t/alphatrade.git
```

It can also be installed from [pypi](https://pypi.org/project/alphatrade/1.0.0/)  

```
pip install alphatrade
```

To force upgrade existing installations:

```
pip uninstall alphatrade
pip --no-cache-dir install --upgrade alphatrade
```

### Prerequisites

Python 3.x

## Make sure to install `setuptools==57.5.0` for `protlib==1.5.0` to work properly

Also, you need the following modules:

- `setuptools==57.5.0`
- `protlib==1.5.0`
- `websocket-client==1.6.1`
- `requests==2.31.0`
- `pandas==2.0.3`
- `pyotp==2.8.0`

The modules can also be installed using `pip`

## Examples - Start Here - Important 

Please clone this repository and check the examples folder to get started.  
Check [here](https://algo2t.github.io/alphatrade/#working-with-examples)

## Getting started with API

### Overview

There is only one class in the whole library: `AlphaTrade`. When the `AlphaTrade` object is created an access token from the SAS Online alpha trade server is stored in text file `access_token.txt` in the same directory. An access token is valid for 24 hours. See the examples folder with `config.py` file to see how to store your credentials.
With an access token, you can instantiate an AlphaTrade object again. Ideally you only need to create an access_token once every day.

### REST Documentation

The original REST API that this SDK is based on is available online.
[Tradelabs API documentation](http://primusapi.tradelab.in/webapi/)

## Using the API

### Logging

The whole library is equipped with python‘s `logging` module for debugging. If more debug information is needed, enable logging using the following code.

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Get an access token

1. Import alphatrade

```python
from alphatrade import *
```

2. Create `config.py` file  
Always keep credentials in a separate file
```python
login_id = "XXXXX"
password = "XXXXXXXX"
Totp = 'XXXXXXXXXXXXXXXX'

try:
    access_token = open('access_token.txt', 'r').read().rstrip()
except Exception as e:
    print('Exception occurred :: {}'.format(e))
    access_token = None
```

3. Import the config
```python
import config
```

### Create AlphaTrade Object

1. Create `AlphaTrade` object with your `login_id`, `password`, `TOTP` / `TOTP_SECRET` and/or `access_token`.

Use `config` object to get `login_id`, `password`, `TOTP` and `access_token`.  

```python
from alphatrade import AlphaTrade
import config
import pyotp
Totp = config.Totp
pin = pyotp.TOTP(Totp).now()
totp = f"{int(pin):06d}" if len(pin) <=5 else pin   
sas = AlphaTrade(login_id=config.login_id, password=config.password, twofa=totp, access_token=config.access_token)

```

## OR

```python
## filename config.py

login_id = "RR24XX"
password = "SuperSecretPassword!!!"
TOTP_SECRET = 'YOURTOTPSECRETEXTERNALAUTH'

try:
    access_token = open('access_token.txt', 'r').read().rstrip()
except Exception as e:
    print(f'Exception occurred :: {e}')
    access_token = None

```


```python
from alphatrade import AlphaTrade
import config
import pyotp
sas = AlphaTrade(login_id=config.login_id, password=config.password, twofa=config.TOTP_SECRET, access_token=config.access_token)

```


2. You can run commands here to check your connectivity

```python
print(sas.get_balance()) # get balance / margin limits
print(sas.get_profile()) # get profile
print(sas.get_daywise_positions()) # get daywise positions
print(sas.get_netwise_positions()) # get netwise positions
print(sas.get_holding_positions()) # get holding positions
```

### Get master contracts

Getting master contracts allow you to search for instruments by symbol name and place orders.
Master contracts are stored as an OrderedDict by token number and by symbol name. Whenever you get a trade update, order update, or quote update, the library will check if master contracts are loaded. If they are, it will attach the instrument object directly to the update. By default all master contracts of all enabled exchanges in your personal profile will be downloaded. i.e. If your profile contains the following as enabled exchanges `['NSE', 'BSE', 'CDS', 'MCX', NFO']` all contract notes of all exchanges will be downloaded by default. If you feel it takes too much time to download all exchange, or if you don‘t need all exchanges to be downloaded, you can specify which exchange to download contract notes while creating the AlphaTrade object.

```python
sas = AlphaTrade(login_id=config.login_id, password=config.password, twofa=totp, access_token=config.access_token, master_contracts_to_download=['NSE', 'BSE'])
```

This will reduce a few milliseconds in object creation time of AlphaTrade object.

### Get tradable instruments

Symbols can be retrieved in multiple ways. Once you have the master contract loaded for an exchange, you can get an instrument in many ways.

Get a single instrument by it‘s name:

```python
tatasteel_nse_eq = sas.get_instrument_by_symbol('NSE', 'TATASTEEL')
reliance_nse_eq = sas.get_instrument_by_symbol('NSE', 'RELIANCE')
ongc_bse_eq = sas.get_instrument_by_symbol('BSE', 'ONGC')
india_vix_nse_index = sas.get_instrument_by_symbol('NSE', 'India VIX')
sensex_nse_index = sas.get_instrument_by_symbol('BSE', 'SENSEX')
```

Get a single instrument by it‘s token number (generally useful only for BSE Equities):

```python
ongc_bse_eq = sas.get_instrument_by_token('BSE', 500312)
reliance_bse_eq = sas.get_instrument_by_token('BSE', 500325)
acc_nse_eq = sas.get_instrument_by_token('NSE', 22)
```

Get FNO instruments easily by mentioning expiry, strike & call or put.

```python
bn_fut = sas.get_instrument_for_fno(symbol = 'BANKNIFTY', expiry_date=datetime.date(2019, 6, 27), is_fut=True, strike=None, is_call = False)
bn_call = sas.get_instrument_for_fno(symbol = 'BANKNIFTY', expiry_date=datetime.date(2019, 6, 27), is_fut=False, strike=30000, is_call = True)
bn_put = sas.get_instrument_for_fno(symbol = 'BANKNIFTY', expiry_date=datetime.date(2019, 6, 27), is_fut=False, strike=30000, is_call = False)
```

### Search for symbols

Search for multiple instruments by matching the name. This works case insensitive and returns all instrument which has the name in its symbol.

```python
all_sensex_scrips = sas.search_instruments('BSE', 'sEnSeX')
print(all_sensex_scrips)
```

The above code results multiple symbol which has ‘sensex’ in its symbol.

```
[Instrument(exchange='BSE', token=1, symbol='SENSEX', name='SENSEX', expiry=None, lot_size=None), Instrument(exchange='BSE', token=540154, symbol='IDFSENSEXE B', name='IDFC Mutual Fund', expiry=None, lot_size=None), Instrument(exchange='BSE', token=532985, symbol='KTKSENSEX B', name='KOTAK MAHINDRA MUTUAL FUND', expiry=None, lot_size=None), Instrument(exchange='BSE', token=538683, symbol='NETFSENSEX B', name='NIPPON INDIA ETF SENSEX', expiry=None, lot_size=None), Instrument(exchange='BSE', token=535276, symbol='SBISENSEX B', name='SBI MUTUAL FUND - SBI ETF SENS', expiry=None, lot_size=None)]
```

Search for multiple instruments by matching multiple names

```python
multiple_underlying = ['BANKNIFTY','NIFTY','INFY','BHEL']
all_scripts = sas.search_instruments('NFO', multiple_underlying)
```

#### Instrument object

Instruments are represented by instrument objects. These are named-tuples that are created while getting the master contracts. They are used when placing an order and searching for an instrument. The structure of an instrument tuple is as follows:

```python
Instrument = namedtuple('Instrument', ['exchange', 'token', 'symbol',
                                      'name', 'expiry', 'lot_size'])
```

All instruments have the fields mentioned above. Wherever a field is not applicable for an instrument (for example, equity instruments don‘t have strike prices), that value will be `None`

### Quote update

Once you have master contracts loaded, you can easily subscribe to quote updates.

#### Four types of feed data are available

You can subscribe any one type of quote update for a given scrip. Using the `LiveFeedType` enum, you can specify what type of live feed you need.

- `LiveFeedType.MARKET_DATA`
- `LiveFeedType.COMPACT`
- `LiveFeedType.SNAPQUOTE`
- `LiveFeedType.FULL_SNAPQUOTE`

Please refer to the original documentation [here](http://primusapi.tradelab.in/webapi/) for more details of different types of quote update.

#### Subscribe to a live feed

```python
sas.subscribe(sas.get_instrument_by_symbol('NSE', 'TATASTEEL'), LiveFeedType.MARKET_DATA)
sas.subscribe(sas.get_instrument_by_symbol('BSE', 'RELIANCE'), LiveFeedType.COMPACT)
```

Subscribe to multiple instruments in a single call. Give an array of instruments to be subscribed.

```python
sas.subscribe([sas.get_instrument_by_symbol('NSE', 'TATASTEEL'), sas.get_instrument_by_symbol('NSE', 'ACC')], LiveFeedType.MARKET_DATA)
```

Note: There is a limit of 250 scrips that can be subscribed on total. Beyond this point the server may disconnect web-socket connection.

Start getting live feed via socket

```python
socket_opened = False
def event_handler_quote_update(message):
    print(f"quote update {message}")

def open_callback():
    global socket_opened
    socket_opened = True

sas.start_websocket(subscribe_callback=event_handler_quote_update,
                      socket_open_callback=open_callback,
                      run_in_background=True)
while(socket_opened==False):
    pass
sas.subscribe(sas.get_instrument_by_symbol('NSE', 'ONGC'), LiveFeedType.MARKET_DATA)
sleep(10)
```

#### Unsubscribe to a live feed

Unsubscribe to an existing live feed

```python
sas.unsubscribe(sas.get_instrument_by_symbol('NSE', 'TATASTEEL'), LiveFeedType.MARKET_DATA)
sas.unsubscribe(sas.get_instrument_by_symbol('BSE', 'RELIANCE'), LiveFeedType.COMPACT)
```

Unsubscribe to multiple instruments in a single call. Give an array of instruments to be unsubscribed.

```python
sas.unsubscribe([sas.get_instrument_by_symbol('NSE', 'TATASTEEL'), sas.get_instrument_by_symbol('NSE', 'ACC')], LiveFeedType.MARKET_DATA)
```

#### Get All Subscribed Symbols

```python
sas.get_all_subscriptions() # All
```

### Market Status messages & Exchange messages.

Subscribe to market status messages

```python
sas.subscribe_market_status_messages()
```

Getting market status messages.

```python
print(sas.get_market_status_messages())
```

Example result of `get_market_status_messages()`

```
[{'exchange': 'NSE', 'length_of_market_type': 6, 'market_type': b'NORMAL', 'length_of_status': 31, 'status': b'The Closing Session has closed.'}, {'exchange': 'NFO', 'length_of_market_type': 6, 'market_type': b'NORMAL', 'length_of_status': 45, 'status': b'The Normal market has closed for 22 MAY 2020.'}, {'exchange': 'CDS', 'length_of_market_type': 6, 'market_type': b'NORMAL', 'length_of_status': 45, 'status': b'The Normal market has closed for 22 MAY 2020.'}, {'exchange': 'BSE', 'length_of_market_type': 13, 'market_type': b'OTHER SESSION', 'length_of_status': 0, 'status': b''}]
```

Note: As per `alice blue` [documentation](http://antplus.aliceblueonline.com/#market-status) all market status messages should be having a timestamp. But in actual the server doesn‘t send timestamp, so the library is unable to get timestamp for now.

Subscribe to exchange messages

```python
sas.subscribe_exchange_messages()
```

Getting market status messages.

```python
print(sas.get_exchange_messages())
```

Example result of `get_exchange_messages()`

```
[{'exchange': 'NSE', 'length': 32, 'message': b'DS : Bulk upload can be started.', 'exchange_time_stamp': 1590148595}, {'exchange': 'NFO', 'length': 200, 'message': b'MARKET WIDE LIMIT FOR VEDL IS 183919959. OPEN POSITIONS IN VEDL HAVE REACHED 84 PERCENT OF THE MARKET WIDE LIMIT.                                                                                       ', 'exchange_time_stamp': 1590146132}, {'exchange': 'CDS', 'length': 54, 'message': b'DS : Regular segment Bhav copy broadcast successfully.', 'exchange_time_stamp': 1590148932}, {'exchange': 'MCX', 'length': 7, 'message': b'.......', 'exchange_time_stamp': 1590196159}]
```

#### Market Status messages & Exchange messages through callbacks

```python
socket_opened = False
def market_status_messages(message):
    print(f"market status messages {message}")

def exchange_messages(message):
    print(f"exchange messages {message}")

def open_callback():
    global socket_opened
    socket_opened = True

sas.start_websocket(market_status_messages_callback=market_status_messages,
					  exchange_messages_callback=exchange_messages,
                      socket_open_callback=open_callback,
                      run_in_background=True)
while(socket_opened==False):
    pass
sas.subscribe_market_status_messages()
sas.subscribe_exchange_messages()
sleep(10)
```

### Place an order

Place limit, market, SL, SL-M, AMO, BO, CO orders

```python
print (sas.get_profile())

# TransactionType.Buy, OrderType.Market, ProductType.Delivery

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%1%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   sas.place_order(transaction_type = TransactionType.Buy,
                     instrument = sas.get_instrument_by_symbol('NSE', 'INFY'),
                     quantity = 1,
                     order_type = OrderType.Market,
                     product_type = ProductType.Delivery,
                     price = 0.0,
                     trigger_price = None,
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
   )

# TransactionType.Buy, OrderType.Market, ProductType.Intraday

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%2%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   sas.place_order(transaction_type = TransactionType.Buy,
                     instrument = sas.get_instrument_by_symbol('NSE', 'INFY'),
                     quantity = 1,
                     order_type = OrderType.Market,
                     product_type = ProductType.Intraday,
                     price = 0.0,
                     trigger_price = None,
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
)

# TransactionType.Buy, OrderType.Market, ProductType.CoverOrder

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%3%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   sas.place_order(transaction_type = TransactionType.Buy,
                     instrument = sas.get_instrument_by_symbol('NSE', 'INFY'),
                     quantity = 1,
                     order_type = OrderType.Market,
                     product_type = ProductType.CoverOrder,
                     price = 0.0,
                     trigger_price = 7.5, # trigger_price Here the trigger_price is taken as stop loss (provide stop loss in actual amount)
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
)


# TransactionType.Buy, OrderType.Limit, ProductType.BracketOrder
# OCO Order can't be of type market

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%4%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   sas.place_order(transaction_type = TransactionType.Buy,
                     instrument = sas.get_instrument_by_symbol('NSE', 'INFY'),
                     quantity = 1,
                     order_type = OrderType.Limit,
                     product_type = ProductType.BracketOrder,
                     price = 8.0,
                     trigger_price = None,
                     stop_loss = 6.0,
                     square_off = 10.0,
                     trailing_sl = None,
                     is_amo = False)
)

# TransactionType.Buy, OrderType.Limit, ProductType.Intraday

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%5%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   sas.place_order(transaction_type = TransactionType.Buy,
                     instrument = sas.get_instrument_by_symbol('NSE', 'INFY'),
                     quantity = 1,
                     order_type = OrderType.Limit,
                     product_type = ProductType.Intraday,
                     price = 8.0,
                     trigger_price = None,
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
)


# TransactionType.Buy, OrderType.Limit, ProductType.CoverOrder

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%6%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   sas.place_order(transaction_type = TransactionType.Buy,
                     instrument = sas.get_instrument_by_symbol('NSE', 'INFY'),
                     quantity = 1,
                     order_type = OrderType.Limit,
                     product_type = ProductType.CoverOrder,
                     price = 7.0,
                     trigger_price = 6.5, # trigger_price Here the trigger_price is taken as stop loss (provide stop loss in actual amount)
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
)

###############################

# TransactionType.Buy, OrderType.StopLossMarket, ProductType.Delivery

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%7%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   sas.place_order(transaction_type = TransactionType.Buy,
                     instrument = sas.get_instrument_by_symbol('NSE', 'INFY'),
                     quantity = 1,
                     order_type = OrderType.StopLossMarket,
                     product_type = ProductType.Delivery,
                     price = 0.0,
                     trigger_price = 8.0,
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
)


# TransactionType.Buy, OrderType.StopLossMarket, ProductType.Intraday

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%8%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   sas.place_order(transaction_type = TransactionType.Buy,
                     instrument = sas.get_instrument_by_symbol('NSE', 'INFY'),
                     quantity = 1,
                     order_type = OrderType.StopLossMarket,
                     product_type = ProductType.Intraday,
                     price = 0.0,
                     trigger_price = 8.0,
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
)



# TransactionType.Buy, OrderType.StopLossMarket, ProductType.CoverOrder
# CO order is of type Limit and And Market Only

# TransactionType.Buy, OrderType.StopLossMarket, ProductType.BO
# BO order is of type Limit and And Market Only

###################################

# TransactionType.Buy, OrderType.StopLossLimit, ProductType.Delivery

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%9%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   sas.place_order(transaction_type = TransactionType.Buy,
                     instrument = sas.get_instrument_by_symbol('NSE', 'INFY'),
                     quantity = 1,
                     order_type = OrderType.StopLossMarket,
                     product_type = ProductType.Delivery,
                     price = 8.0,
                     trigger_price = 8.0,
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
)


# TransactionType.Buy, OrderType.StopLossLimit, ProductType.Intraday

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%10%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   sas.place_order(transaction_type = TransactionType.Buy,
                     instrument = sas.get_instrument_by_symbol('NSE', 'INFY'),
                     quantity = 1,
                     order_type = OrderType.StopLossLimit,
                     product_type = ProductType.Intraday,
                     price = 8.0,
                     trigger_price = 8.0,
                     stop_loss = None,
                     square_off = None,
                     trailing_sl = None,
                     is_amo = False)
)



# TransactionType.Buy, OrderType.StopLossLimit, ProductType.CoverOrder
# CO order is of type Limit and And Market Only


# TransactionType.Buy, OrderType.StopLossLimit, ProductType.BracketOrder

print ("%%%%%%%%%%%%%%%%%%%%%%%%%%%%11%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
print(
   sas.place_order(transaction_type = TransactionType.Buy,
                     instrument = sas.get_instrument_by_symbol('NSE', 'INFY'),
                     quantity = 1,
                     order_type = OrderType.StopLossLimit,
                     product_type = ProductType.BracketOrder,
                     price = 8.0,
                     trigger_price = 8.0,
                     stop_loss = 1.0,
                     square_off = 1.0,
                     trailing_sl = 20,
                     is_amo = False)
)
```

### Place basket order

Basket order is used to buy or sell group of securities simultaneously.

```python
order1 = {  "instrument"        : sas.get_instrument_by_symbol('NSE', 'INFY'),
            "order_type"        : OrderType.Market,
            "quantity"          : 1,
            "transaction_type"  : TransactionType.Buy,
            "product_type"      : ProductType.Delivery}
order2 = {  "instrument"        : sas.get_instrument_by_symbol('NSE', 'SBIN'),
            "order_type"        : OrderType.Limit,
            "quantity"          : 2,
            "price"             : 280.0,
            "transaction_type"  : TransactionType.Sell,
            "product_type"      : ProductType.Intraday}
order = [order1, order2]
print(sas.place_basket_order(orders))
```

### Cancel an order

```python
sas.cancel_order('170713000075481') #Cancel an open order
```

### Getting order history and trade details

#### Get order history of a particular order

```python
print(sas.get_order_history('170713000075481'))
```

#### Get order history of all orders.

```python
print(sas.get_order_history())
```

#### Get trade book

```python
print(sas.get_trade_book())
```

#### Get historical candles data

This will provide historical data but **not for current day**.  
This returns a `pandas` `DataFrame` object which be used with `pandas_ta` to get various indicators values.  

```python
from datetime import datetime
print(sas.get_historical_candles('MCX', 'NATURALGAS NOV FUT', datetime(2020, 10, 19), datetime.now() ,interval=30))
```

Output 

```console
Instrument(exchange='MCX', token=224365, symbol='NATURALGAS NOV FUT', name='', expiry=datetime.date(2020, 11, 24), lot_size=None)
                            open   high    low  close  volume
date
2020-10-19 09:00:00+05:30  238.9  239.2  238.4  239.0     373
2020-10-19 09:30:00+05:30  239.0  239.0  238.4  238.6     210
2020-10-19 10:00:00+05:30  238.7  238.7  238.1  238.1     213
2020-10-19 10:30:00+05:30  238.0  238.4  238.0  238.1     116
2020-10-19 11:00:00+05:30  238.1  238.2  238.0  238.0      69
...                          ...    ...    ...    ...     ...
2020-10-23 21:00:00+05:30  237.5  238.1  237.3  237.6     331
2020-10-23 21:30:00+05:30  237.6  238.5  237.6  237.9     754
2020-10-23 22:00:00+05:30  237.9  238.1  237.2  237.9     518
2020-10-23 22:30:00+05:30  237.9  238.7  237.7  238.1     897
2020-10-23 23:00:00+05:30  238.2  238.3  236.3  236.5    1906

```

Better way to get historical data, first get the latest version from github  

`python -m pip install git+https://github.com/algo2t/alphatrade.git`

```python
from datetime import datetime
india_vix_nse_index = sas.get_instrument_by_symbol('NSE', 'India VIX')
print(sas.get_historical_candles(india_vix_nse_index.exchange, india_vix_nse_index.symbol, datetime(2020, 10, 19), datetime.now() ,interval=30))
```


#### Get intraday candles data

This will give candles data for **current day only**.  
This returns a `pandas` `DataFrame` object which be used with `pandas_ta` to get various indicators values.  

```python
print(sas.get_intraday_candles('MCX', 'NATURALGAS NOV FUT', interval=15))
```

Better way to get intraday data, first get the latest version from github  

`python -m pip install git+https://github.com/algo2t/alphatrade.git`

```python
from datetime import datetime
nifty_bank_nse_index = sas.get_instrument_by_symbol('NSE', 'Nifty Bank')
print(sas.get_intraday_candles(nifty_bank_nse_index.exchange, nifty_bank_nse_index.symbol, datetime(2020, 10, 19), datetime.now(), interval=10))
```

### Order properties as enums

Order properties such as TransactionType, OrderType, and others have been safely classified as enums so you don‘t have to write them out as strings

#### TransactionType

Transaction types indicate whether you want to buy or sell. Valid transaction types are of the following:

- `TransactionType.Buy` - buy
- `TransactionType.Sell` - sell

#### OrderType

Order type specifies the type of order you want to send. Valid order types include:

- `OrderType.Market` - Place the order with a market price
- `OrderType.Limit` - Place the order with a limit price (limit price parameter is mandatory)
- `OrderType.StopLossLimit` - Place as a stop loss limit order
- `OrderType.StopLossMarket` - Place as a stop loss market order

#### ProductType

Product types indicate the complexity of the order you want to place. Valid product types are:

- `ProductType.Intraday` - Intraday order that will get squared off before market close
- `ProductType.Delivery` - Delivery order that will be held with you after market close
- `ProductType.CoverOrder` - Cover order
- `ProductType.BracketOrder` - One cancels other order. Also known as bracket order

## Working with examples

[Here](https://github.com/algo2t/alphatrade), examples directory there are 3 files `zlogin_example.py`, `zstreaming_data.py` and `stop.txt`

### Steps

- Clone the repository to your local machine `git clone https://github.com/algo2t/alphatrade.git`
- Copy the examples directory to any location where you want to write your code
- Install the `alphatrade` module using `pip` => `python -m pip install https://github.com/algo2t/alphatrade.git`
- Open the examples directory in your favorite editor, in our case it is [VSCodium](https://vscodium.com/)
- Open the `zlogin_example.py` file in the editor
- Now, create `config.py` file as per instructions given below and in the above file
- Provide correct login credentials like login_id, password and 16 digit totp code (find below qr code)
- This is generally set from the homepage of alpha web trading platform [here](https://alpha.sasonline.in/)
- Click on `FORGET PASSWORD?` => Select `Reset 2FA` radio button.  ![image](https://raw.githubusercontent.com/algo2t/alphatrade/main/snaps/forget_password.png)
- Enter the CLIENT ID (LOGIN_ID), EMAIL ID and PAN NUMBER, click on `RESET` button.  ![image](https://raw.githubusercontent.com/algo2t/alphatrade/main/snaps/reset_two_fa.png)
- Click on `BACK TO LOGIN` and enter `CLIENT ID` and `PASSWORD`, click on `SECURED SIGN-IN`
- Set same answers for 5 questions and click on `SUBMIT` button.  ![image](https://raw.githubusercontent.com/algo2t/alphatrade/main/snaps/set_answers.png)

`config.py`
```python
login_id = "XXXXX"
password = "XXXXXXXX"
Totp = 'XXXXXXXXXXXXXXXX'

try:
    access_token = open('access_token.txt', 'r').read().rstrip()
except Exception as e:
    print('Exception occurred :: {}'.format(e))
    access_token = None
```

## Example strategy using alpha trade API

[Here](https://github.com/algo2t/alphatrade/blob/main/zstreaming_data.py) is an example moving average strategy using alpha trade web API.
This strategy generates a buy signal when 5-EMA > 20-EMA (golden cross) or a sell signal when 5-EMA < 20-EMA (death cross).

## Example for getting historical and intraday candles data

[Here](https://github.com/algo2t/alphatrade/blob/main/zhistorical_data.py) is an example for getting historical data using alpha trade web API.

For historical candles data `start_time` and `end_time` must be provided in format as shown below.
It can also be provided as `timedelta`. Check the script `zhistorical_data.py` in examples.

```python
from datetime import datetime, timedelta
start_time = datetime(2020, 10, 19, 9, 15, 0)
end_time = datetime(2020, 10, 21, 16, 59, 0)

df = sas.get_historical_candles('MCX', 'NATURALGAS OCT FUT', start_time, end_time, 5)
print(df)
end_time = start_time + timedelta(days=5)
df = sas.get_historical_candles('MCX', 'NATURALGAS NOV FUT', start_time, end_time, 15)
print(df)
```

For intraday or today‘s / current day‘s candles data.  

```python
df = sas.get_intraday_candles('MCX', 'NATURALGAS OCT FUT')
print(df)
df = sas.get_intraday_candles('MCX', 'NATURALGAS NOV FUT', 15)
print(df)
```


## Read this before creating an issue

Before creating an issue in this library, please follow the following steps.

1. Search the problem you are facing is already asked by someone else. There might be some issues already there, either solved/unsolved related to your problem. Go to [issues](https://github.com/algo2t/alphatrade/issues) page, use `is:issue` as filter and search your problem. ![image](https://user-images.githubusercontent.com/38440742/85207058-376ee400-b2f4-11ea-91ad-c8fd8a682a12.png)
2. If you feel your problem is not asked by anyone or no issues are related to your problem, then create a new issue.
3. Describe your problem in detail while creating the issue. If you don‘t have time to detail/describe the problem you are facing, assume that I also won‘t be having time to respond to your problem.
4. Post a sample code of the problem you are facing. If I copy paste the code directly from issue, I should be able to reproduce the problem you are facing.
5. Before posting the sample code, test your sample code yourself once. Only sample code should be tested, no other addition should be there while you are testing.
6. Have some print() function calls to display the values of some variables related to your problem.
7. Post the results of print() functions also in the issue.
8. Use the insert code feature of github to inset code and print outputs, so that the code is displayed neat. ![image](https://user-images.githubusercontent.com/38440742/85207234-4dc96f80-b2f5-11ea-990c-df013dd69cf2.png)

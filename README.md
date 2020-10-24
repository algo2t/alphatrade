# Python APIs for SAS Online Alpha Trade Web Platform

The Python APIs for communicating with the SAS Online Alpha Trade Web Platform.

Alpha Trade Python library provides an easy to use wrapper over the HTTPS APIs.

The HTTP calls have been converted to methods and JSON responses are wrapped into Python-compatible objects.

Websocket connections are handled automatically within the library.

- **Author: [algo2t](https://github.com/algo2t/)**

## Installation

This module is installed via pip:

```
pip install https://github.com/algo2t/alphatrade
```

To force upgrade existing installations:

```
pip uninstall alphatrade
pip --no-cache-dir install --upgrade alphatrade
```

### Prerequisites

Python 3.x

Also, you need the following modules:

- `protlib`
- `websocket_client`
- `requests`

The modules can also be installed using `pip`

## Getting started with API

### Overview

There is only one class in the whole library: `AlphaTrade`. When the `AlphaTrade` object is created an access token from the SAS Online alpha trade server is stored in text file `access_token.txt` in the same directory. An access token is valid for 24 hours. See the examples folder with `config.py` file to see how to store your credentials.
With an access token, you can instantiate an AlphaTrade object again. Ideally you only need to create an access_token once every day.

### REST Documentation

The original REST API that this SDK is based on is available online.
[Alice Blue API REST documentation](http://antplus.aliceblueonline.com/#introduction)

## Using the API

### Logging

The whole library is equipped with python's `logging` module for debugging. If more debug information is needed, enable logging using the following code.

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Get an access token

1. Import alphatrade

```python
from alphatrade import *
```

### Create AlphaTrade Object

1. Create `AlphaTrade` object with your `login_id`, `password`, `2FA` or `access_token`.

```python
sas = AlphaTrade(login_id='login_id', password='password', twofa='a', access_token=access_token)
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
Master contracts are stored as an OrderedDict by token number and by symbol name. Whenever you get a trade update, order update, or quote update, the library will check if master contracts are loaded. If they are, it will attach the instrument object directly to the update. By default all master contracts of all enabled exchanges in your personal profile will be downloaded. i.e. If your profile contains the following as enabled exchanges `['NSE', 'BSE', 'CDS', 'MCX', NFO']` all contract notes of all exchanges will be downloaded by default. If you feel it takes too much time to download all exchange, or if you don't need all exchanges to be downloaded, you can specify which exchange to download contract notes while creating the AlphaTrade object.

```python
sas = AlphaTrade(login_id='login_id', password='password', twofa='a', access_token=access_token, master_contracts_to_download=['NSE', 'BSE'])
```

This will reduce a few milliseconds in object creation time of AlphaTrade object.

### Get tradable instruments

Symbols can be retrieved in multiple ways. Once you have the master contract loaded for an exchange, you can get an instrument in many ways.

Get a single instrument by it's name:

```python
tatasteel_nse_eq = sas.get_instrument_by_symbol('NSE', 'TATASTEEL')
reliance_nse_eq = sas.get_instrument_by_symbol('NSE', 'RELIANCE')
ongc_bse_eq = sas.get_instrument_by_symbol('BSE', 'ONGC')
india_vix_nse_index = sas.get_instrument_by_symbol('NSE', 'India VIX')
sensex_nse_index = sas.get_instrument_by_symbol('BSE', 'SENSEX')
```

Get a single instrument by it's token number (generally useful only for BSE Equities):

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

The above code results multiple symbol which has 'sensex' in its symbol.

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

All instruments have the fields mentioned above. Wherever a field is not applicable for an instrument (for example, equity instruments don't have strike prices), that value will be `None`

### Quote update

Once you have master contracts loaded, you can easily subscribe to quote updates.

#### Four types of feed data are available

You can subscribe any one type of quote update for a given scrip. Using the `LiveFeedType` enum, you can specify what type of live feed you need.

- `LiveFeedType.MARKET_DATA`
- `LiveFeedType.COMPACT`
- `LiveFeedType.SNAPQUOTE`
- `LiveFeedType.FULL_SNAPQUOTE`

Please refer to the original documentation [here](http://antplus.aliceblueonline.com/#marketdata) for more details of different types of quote update.

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

Note: As per `alice blue` [documentation](http://antplus.aliceblueonline.com/#market-status) all market status messages should be having a timestamp. But in actual the server doesn't send timestamp, so the library is unable to get timestamp for now.

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

### Order properties as enums

Order properties such as TransactionType, OrderType, and others have been safely classified as enums so you don't have to write them out as strings

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

## Example strategy using alpha trade API

[Here](https://github.com/algo2t/alphatrade) is an example moving average strategy using alpha trade web API.
This strategy generates a buy signal when 5-EMA > 20-EMA (golden cross) or a sell signal when 5-EMA < 20-EMA (death cross).

## Read this before creating an issue

Before creating an issue in this library, please follow the following steps.

1. Search the problem you are facing is already asked by someone else. There might be some issues already there, either solved/unsolved related to your problem. Go to [issues](https://github.com/algo2t/alphatrade/issues) page, use `is:issue` as filter and search your problem. ![image](https://user-images.githubusercontent.com/38440742/85207058-376ee400-b2f4-11ea-91ad-c8fd8a682a12.png)
2. If you feel your problem is not asked by anyone or no issues are related to your problem, then create a new issue.
3. Describe your problem in detail while creating the issue. If you don't have time to detail/describe the problem you are facing, assume that I also won't be having time to respond to your problem.
4. Post a sample code of the problem you are facing. If I copy paste the code directly from issue, I should be able to reproduce the problem you are facing.
5. Before posting the sample code, test your sample code yourself once. Only sample code should be tested, no other addition should be there while you are testing.
6. Have some print() function calls to display the values of some variables related to your problem.
7. Post the results of print() functions also in the issue.
8. Use the insert code feature of github to inset code and print outputs, so that the code is displayed neat. ![image](https://user-images.githubusercontent.com/38440742/85207234-4dc96f80-b2f5-11ea-990c-df013dd69cf2.png)

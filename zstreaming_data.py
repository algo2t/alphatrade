import statistics
import datetime
import config
import json
from time import sleep

# pip install https://github.com/algo2t/alphatrade

from alphatrade import AlphaTrade, LiveFeedType

sas = AlphaTrade(login_id=config.login_id, password=config.password,
                 twofa=config.TOTP, access_token=config.access_token, master_contracts_to_download=['MCX', 'NFO'])


ins_scrip = sas.get_instrument_by_symbol('MCX', 'NATURALGAS AUG FUT')

print(ins_scrip)

ltp = 0.0
socket_opened = False
count_s = 0
count_b = 0


def event_handler_quote_update(message):
    global ltp
    # ltp = message['ltp']
    # tick = json.loads(message, indent=1)
    print(f'ticks :: {message}')


def open_callback():
    global socket_opened
    socket_opened = True


def run_strategy():
    global ltp
    minute_close = []

    sas.start_websocket(subscribe_callback=event_handler_quote_update,
                        socket_open_callback=open_callback,
                        run_in_background=True)
    while (socket_opened is False):    # wait till socket open & then subscribe
        pass
    sas.subscribe(ins_scrip, LiveFeedType.COMPACT)
    # sas.subscribe(ins_scrip, LiveFeedType.MARKET_DATA)
    # sas.subscribe(ins_scrip, LiveFeedType.SNAPQUOTE)
    # sas.subscribe(ins_scrip, LiveFeedType.FULL_SNAPQUOTE)

    print("Script Start Time :: " + str(datetime.datetime.now()))
    while True:
        print('current price is :: '+str(ltp))
        if datetime.datetime.now().second in [0, 30]:
            # NOTE This is just an example to stop script without using `control + c` Keyboard Interrupt
            # It checks whether the stop.txt has word stop
            # This check is done every 30 seconds
            stop_script = open('zstop.txt', 'r').read().strip()
            print(stop_script + " time :: " + str(datetime.datetime.now()))
            if (stop_script == 'stop'):
                print('exiting script')
                break
        # LTP is stored in the minute_close array and then mean is found on close to get SMA_5 and SMA_20
        if (datetime.datetime.now().second == 0):
            minute_close.append(ltp)
            print('current price is :: '+str(ltp))
            if (len(minute_close) > 20):
                sma_5 = statistics.mean(minute_close[-5:])
                sma_20 = statistics.mean(minute_close[-20:])
                print('current price is :: '+str(ltp))
                if (sma_5 > sma_20) and (status != 'bought'):
                    # buy_signal(ins_scrip)
                    print('buy signal crossover :: ' + str(count_b))
                    status = 'bought'
                    count_b = count_b+1
                elif (sma_5 < sma_20) and (status != 'sold'):
                    # sell_signal(ins_scrip)
                    print('sell signal crossover :: ' + str(counts))
                    status = 'sold'
                    counts = counts + 1
            sleep(1)
        sleep(0.2)  # sleep for 200ms


run_strategy()

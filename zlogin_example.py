
from alphatrade import AlphaTrade
import config
import pyotp
Totp = config.TOTP
pin = pyotp.TOTP(Totp).now()
totp = f"{int(pin):06d}" if len(pin) <= 5 else pin
print(totp)
sas = AlphaTrade(login_id=config.login_id, password=config.password,
                 twofa=totp, access_token=config.access_token, master_contracts_to_download=['MCX', 'NFO'])
# print(sas.get_profile())
print(sas.get_balance())
print(sas.get_trade_book())
# print(sas.orders('complete'))
# print(sas.orders('pending'))
print(sas.orders())
# print(sas.get_daywise_positions())
# print(sas.get_holding_positions())
# print(sas.get_netwise_positions())
print(sas.search('Nifty Bank','NSE'))
print(sas.search('TCS','BSE'))
print(sas.search('TCS', 'NFO'))
print(sas.search('TCS-EQ'))
print(sas.positions())
print(sas.positions('historical'))

print(sas.get_exchanges())
print(sas.get_master_contract('MCX'))


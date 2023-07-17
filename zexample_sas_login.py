import datetime
import json
from time import sleep

# pip install https://github.com/algo2t/alphatrade

from alphatrade import AlphaTrade, LiveFeedType

import config
# NOTE create a config.py file in the same directory as sas_login_eg.py file
# Contents of the config.py must be as below, config.py is used for storing credentials
#### config.py START ####
# login_id = "RR"
# password = "SAS@131"
# TOTP = "EXAMPLETOTPSECRET"

# try:
#     access_token = open('zaccess_token.txt', 'r').read().rstrip()
# except Exception as e:
#     print('Exception occurred :: {}'.format(e))
#     access_token = None
#### config.py END ####

sas = AlphaTrade(login_id=config.login_id, password=config.password, twofa=config.TOTP)

# NOTE access_token can be supplied if already available
# sas = AlphaTrade(login_id=config.login_id, password=config.password,
#                  twofa=config.twofa, access_token=config.access_token)

# NOTE access_token can be supplied if already available and master_contracts to download
# sas = AlphaTrade(login_id=config.login_id, password=config.password,
#                  twofa=config.twofa, access_token=config.access_token, master_contracts_to_download=['CDS'])


print(sas.get_profile())
usd_inr = sas.get_instrument_by_symbol('NSE', 'PAYTM')
print(usd_inr)
print(sas.get_balance())

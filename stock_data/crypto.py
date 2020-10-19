import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from flask import flash
import json

from stock_data.config import Config


class CoinMarket:

    def __init__(self):
        self.api_key = Config.COINMARKET_API_KEY
        self.quotas = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        self.map_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"
        self.latest_listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.parameters = {
          # 'start': '1',
          # 'limit': '90',
          # 'convert': 'DKK',
        }
        self.headers = {
          'Accept': 'application/json',
          'Accept-Encoding': 'deflate, gzip',
          'X-CMC_PRO_API_KEY': self.api_key,
        }

    def get_cur_symol_id(self):
        with open("currencies-info.txt", mode='r') as jsonfile:
            info = json.load(jsonfile)
        data = info['data']
        id_symbol = {}
        for curr in data:
            id_symbol[curr['id']] = curr['symbol']
        return id_symbol

    def get_crypto_portfolio(self, symbolsogamount):
        id_symbol_dict = self.get_cur_symol_id()
        invalid_symbols = []
        for sym in symbolsogamount:
            if sym not in id_symbol_dict.values():
                invalid_symbols.append(sym)
                # raise ValueError("Invalid symbol %s" %sym)
        flash("Invalid symbol %s" %invalid_symbols)
        for k in invalid_symbols:
            symbolsogamount.pop(k, None)
        listToStr = ','.join([str(elem) for elem in symbolsogamount])
        self.parameters["symbol"] = listToStr
        self.parameters["convert"] = "DKK"
        try:
            response = requests.get(self.quotas, params=self.parameters, headers=self.headers)
            content = response.json()
            return self.extract_portfolio_data(data=content['data'],
                                               sym_amount_dict=symbolsogamount)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            raise e

    def extract_portfolio_data(self, data, sym_amount_dict):
        portfolio_data = []
        if data:
            for k, v in sym_amount_dict.items():
                currency = data[k]
                convert = currency['quote']['DKK']
                values_dict = {
                    "Symbol": k,
                    "Name": currency['name'],
                    "Price": round(float(convert['price']), 3),
                    "Value": round(float(convert['price']) * int(v), 3),
                    "percent_change_24h": round(float(convert['percent_change_24h']), 3),
                    "percent_change_7d": round(float(convert['percent_change_7d']), 3)
                }
                portfolio_data.append(values_dict)
        return portfolio_data

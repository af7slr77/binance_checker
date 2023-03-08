import requests


def get_ticker(symbol, interval):
    kline_url = 'https://www.binance.com/api/v3/klines'
    params = {'symbol': symbol,
              'interval': interval}
    kline = requests.get(kline_url, params=params).json()[-1]
    data = {
        'current_price': float(kline[4]),
        'open_price': float(kline[1]),
        'difference': round(float(kline[4]) - float(kline[1]), 2)
    }

    return data


def max_min_price_for_the_last_24_hr(symbol):
    last_24_hr_url = "https://www.binance.com/api/v3/ticker/24hr"
    params = {'symbol': symbol}
    tiker_24hr = requests.get(last_24_hr_url, params).json()
    data = {
        'max_price': float(tiker_24hr['highPrice']),
        'min_price': float(tiker_24hr['lowPrice'])
    }
    return data


symbol = "ETHUSDT"
interval = "15m"


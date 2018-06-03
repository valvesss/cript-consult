#!/usr/bin/env python3
import requests, json, sys, time

def query(url):
    response = requests.get(url=url).json()
    return response

def coinstats():
    currency = sys.argv[1]
    url = []
    if (currency == 'btc') or (currency == 'BTC'):
        url.append("https://api.kraken.com/0/public/Ticker?pair=XBTUSD")
        url.append("https://yobit.net/api/3/ticker/btc_usd")
    else:
        url.append("https://api.kraken.com/0/public/Ticker?pair=%sUSD" % currency)
        url.append("https://yobit.net/api/3/ticker/%s_usd" % currency)
    url.append("https://www.okcoin.com/api/v1/ticker.do?symbol=%s_usd" % currency)
    url.append("https://bittrex.com/api/v1.1/public/getticker?market=usdt-%s" % currency)
    return webconsult(currency,url)

def webconsult(currency,url):
    aux = len(url)
    matrix = [[ 0 for x in range(2)] for y in range(aux)]
    for i in range(aux):
        response = query(url[i])
        if "kraken" in url[i]:
            if (currency == 'btc') or (currency == 'BTC'):
                field = 'XXBTZUSD'
            else:
                field = 'X' + currency.upper() + 'ZUSD'
            bitcoinvalue = response['result'][field]['c'][0]
            exchange = "kraken"
        if "okcoin" in url[i]:
            bitcoinvalue = response['ticker']['last']
            exchange = "okcoin"
        if "bittrex" in url[i]:
            bitcoinvalue = response['result']['Last']
            exchange = "bittrex"
        if "yobit" in url[i]:
            if (currency == 'btc') or (currency == 'BTC'):
                field = 'btc_usd'
            else:
                field = currency + '_usd'
            bitcoinvalue = response[field]['last']
            exchange = "yobit"
        matrix[i][0] = exchange
        matrix[i][1] = round(float(bitcoinvalue),2)
    matrix.sort(key=lambda x:x[1],reverse=True)
    presentation(matrix,currency)

def presentation(matrix,currency):
    print("\nPreço do %s em USD:\n" % currency.upper())
    for i in range(len(matrix)):
        print(matrix[i][0].title() + ":  \t",round(float(matrix[i][1]),8))
        time.sleep(0.5)
    size = len(matrix)-1
    diff = round((matrix[0][1]-matrix[size][1]),2)
    print("\nThe biggest difference is between %s and %s with a %s gap of: %s USD." % ((matrix[0][0]).title(),(matrix[size][0]).title(),currency.upper(),diff))
    return

if len(sys.argv) < 2:
    print("Moeda inexistente. Modo de usar: \'./coinconsult.py btc\'.")
    exit()

coinstats()

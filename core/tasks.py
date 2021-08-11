from celery import shared_task
import requests
from .models import CoinPair

# def filter_usd_coins(response):

#     usd_list = [{"symbol" : f'{response[i]["symbol"]}USD', 'vol':  response[i]["price"]} for i in range(len(response))]

#     return usd_list

# def filter_coins(response_data):
#     btc_list = []
#     eth_list = []
#     usdt_list = []
#     for i in range(475):
#         if str(response_data[i]["symbol"])[len(str(response_data[i]["symbol"]))-3:] == "BTC":

#             btc_list.append({"symbol": response_data[i]["symbol"], "vol": response_data[i]["volume"]})

#         elif str(response_data[i]["symbol"])[len(str(response_data[i]["symbol"]))-4:] == "USDT":

#             usdt_list.append({"symbol": response_data[i]["symbol"], "vol": response_data[i]["volume"]})

#         elif str(response_data[i]["symbol"])[len(str(response_data[i]["symbol"]))-3:] == "ETH":

#             eth_list.append({"symbol": response_data[i]["symbol"], "vol": response_data[i]["volume"]})
            

#     return btc_list[:30], usdt_list[:30], eth_list[:30]


@shared_task(bind = True)
def call_binance_api(self):
    
    r = requests.get(url = 'https://api1.binance.com/api/v3/ticker/24hr')

    res = requests.get(url = 'https://api.nomics.com/v1/currencies/ticker?key=5ef7e9af2e6024515be2b06d18f336c0aaec6499&per-page=30&page=1')
    res_for_usd = res.json()

    usd_list = [{"symbol" : f'{res_for_usd[i]["symbol"]}USD', 'vol':  res_for_usd[i]["price"]} for i in range(len(res_for_usd))]
    

    response_data = r.json()

    btc_list = []
    eth_list = []
    usdt_list = []
    for i in range(475):
        if str(response_data[i]["symbol"])[len(str(response_data[i]["symbol"]))-3:] == "BTC":

            btc_list.append({"symbol": response_data[i]["symbol"], "vol": response_data[i]["volume"]})

        elif str(response_data[i]["symbol"])[len(str(response_data[i]["symbol"]))-4:] == "USDT":

            usdt_list.append({"symbol": response_data[i]["symbol"], "vol": response_data[i]["volume"]})

        elif str(response_data[i]["symbol"])[len(str(response_data[i]["symbol"]))-3:] == "ETH":

            eth_list.append({"symbol": response_data[i]["symbol"], "vol": response_data[i]["volume"]})

    all_coins = []
    all_coins.extend(btc_list[:30])
    all_coins.extend(usdt_list[:30])
    all_coins.extend(eth_list[:30])
    all_coins.extend(usd_list)
    
    l = [CoinPair(pair_name = all_coins[i]["symbol"], pair_vol = all_coins[i]["vol"], coin_price  = 150) for i in range(len(all_coins))]

    try:
        # if CoinPair.objects.all().count()==0:
        CoinPair.objects.bulk_create(l)
        # pass

    except Exception as e:
        print(e)
        key_list = []
        for i in range(120):
            coin_obj = CoinPair.objects.get(pair_name = all_coins[i]["symbol"])
            coin_obj.pair_vol  = all_coins[i]["vol"]
            coin_obj.coin_price  = 150
            key_list.append(coin_obj)

        CoinPair.objects.bulk_update(key_list, ['pair_vol', 'coin_price'])
    return None
import json
from django.core import serializers
from django.db.models.constraints import BaseConstraint
from django.http import response, JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import View
import requests
from .models import CoinPair, Currency_Wallet



def get_all_the_assets():
    r = requests.get('https://api.wazirx.com/api/v2/market-status')
    response = r.json()
    funds_list = [{'name' : response['assets'][i]['name'], 'type' : response['assets'][i]['type']} for i in range(len(response['assets']))]
    return funds_list

# Create your views here.
#(_______________________________________________________Index view_________________________________________________________)

class Index(View):
    template_name = 'core/index.html'
    def get(self, request, *args, **kwargs):
    #     res = requests.get(url = 'https://api.pro.coinbase.com/products')
    #     res = res.json()
    #     count = 0
    #     l = []
    #     for i in range(len(res)):
    #         if res[i]['quote_currency'] == 'USD':
    #             l.append({'sym': res[i]['id'], 'vol' : res[i]['base_increment']})
    #             count = count + 1

        return render(request, template_name = self.template_name)


from django.views.decorators.vary import vary_on_headers

class ExchangeView(View):

    template_name = 'core/exchange.html'
    
    @vary_on_headers('X-Requested-With')
    def get(self, request, *args, **kwargs):

        if request.method == 'GET':

                                    
            all_coins_obj = CoinPair.objects.filter().values('pair_name', 'pair_vol', 'coin_price').order_by('id')
            btc_list = list(all_coins_obj)[:30]
            usdt_list = list(all_coins_obj)[30:60]
            eth_list = list(all_coins_obj)[60:90]
            usd_list = list(all_coins_obj)[90:]
            # btc_list = serializers.serialize('json', btc_list)
            # usdt_list = serializers.serialize('json', usdt_list)
            # eth_list = serializers.serialize('json', eth_list)

            pair_name = kwargs.get('pair_name', 'BTCUSDT')
            print(pair_name,'dsfsdafsdfsdfsdfsdf')
            if request.is_ajax():
                # return JsonResponse({'pair_name': pair_name, 'btc_list': btc_list})
                return JsonResponse({'pair_name': pair_name, 'btc_list': btc_list, 'len_btc' : len(btc_list), 'usdt_list': usdt_list, 'eth_list': eth_list, 'len_eth' : len(eth_list), 'len_usdt' : len(usdt_list), 'usd_list': usd_list, 'url':'/exchange'}, safe = False)

        # render_to_response
        return render(request, self.template_name,{'pair_name': pair_name} )
        # return redirect('/exchange/')


class P2pView(View):
    template_name = 'core/p2p.html'
    login_template_name = 'core/p2plogin.html'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, template_name = self.login_template_name)
        return render(request, template_name = self.template_name)
    
 
class STFView(View):
    template_name = 'core/stf.html'
    def get(self, request, *args, **kwargs):

        return render(request, template_name = self.template_name)   


class FundsView(View):
    template_name = 'core/funds.html'
    def get(self, request, *args, **kwargs):
        all_assets = get_all_the_assets()
        # wallet_obj = Currency_Wallet.objects.filter(user , = request.user)
        return render(request,self.template_name, {'all_assets' : all_assets})  

class AccountView(View):
    template_name = 'core/account.html'
    def get(self, request, *args, **kwargs):

        return render(request, template_name = self.template_name)  
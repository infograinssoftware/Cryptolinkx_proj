from django.contrib import admin

from .models import CoinPair, Currency_Wallet, Wallet_Service
admin.site.register(CoinPair)
admin.site.register(Currency_Wallet)
admin.site.register(Wallet_Service)
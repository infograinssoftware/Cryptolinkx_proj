from django.db import models
from users.models import Custom_User

class CoinPair(models.Model):
    pair_name = models.CharField(max_length = 20, unique = True)
    pair_vol = models.FloatField(max_length = 18)
    # pair_symbol = models.ImageField()
    coin_price = models.FloatField(max_length = 18)

    def __str__(self):
        return self.pair_name
    
class Currency_Wallet(models.Model):
    user = models.ForeignKey(Custom_User, on_delete = models.CASCADE)
    coin_pair = models.ForeignKey(CoinPair, on_delete = models.CASCADE)
    public_key = models.CharField(max_length = 500)
    available_bal = models.IntegerField()
    wallet_address = models.CharField(max_length = 500)
    locked_bal =  models.IntegerField()
    total_bal =  models.IntegerField()
    usdt_bal =  models.IntegerField()

    def __str__(self):
        return f'{self.user}---------{self.coin_pair}'

class Wallet_Service(models.Model):
    user_wallet = models.ForeignKey(Currency_Wallet, on_delete = models.CASCADE)
    deposit_date = models.DateTimeField(auto_now_add = True)

class P2p_Seller(models.Model):
    coin_placer = models.ForeignKey(Custom_User, on_delete = models.CASCADE, related_name = 'p2p_sender')
    unit_sell_price = models.FloatField()
    sell_volume = models.FloatField()
    sell_date = models.DateTimeField(auto_now_add = True)
    user_cid_name = models.CharField(max_length = 20)
    
    





import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import CoinPair
from django.core.serializers import serialize
from asgiref.sync import sync_to_async
import time 

class ExchangeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'exchange_pairs'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

        self.all_coins =  await self.get_all_the_coins()
        self.all_coins_json = await sync_to_async(serialize)('json', self.all_coins)

    # Receive message from WebSocket
    async def receive(self, text_data):
        
        self.all_coins =  await self.get_all_the_coins()
        # self.all_coins_json = await sync_to_async(serialize)('json', self.all_coins)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'exchange_coins',
                'message': json.loads(text_data)['msg'],
                'all_coins' : self.all_coins_json
            }
        )

    # Receive message from room group
    async def exchange_coins(self, event):
        message = event['message']
        all_coins = event['all_coins']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'all_coins': all_coins
        }))



    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def get_all_the_coins(self):
        all_coins =  CoinPair.objects.all().order_by('id')
        print(all_coins)
        return all_coins


#(___________________________________________P2P Consumer______________________________________________ )


class P2PConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'p2p_group'


        self.pair_name =  self.scope['url_route']['kwargs']['pair_name']

        if not self.pair_name:
            self.pair_name = 'BTCUSDT'

        self.single_coin =  await self.getting_single_pair_name()
        self.json_single_coin = await sync_to_async(serialize)('json', [self.single_coin])

       

        # Join room group
        await self.channel_layer.group_add(
            
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print('connected')

        self.fetched_pairs = await self.get_some_pairs()
        self.json_fetched_pairs = await sync_to_async(serialize)('json', self.fetched_pairs)


    async def receive(self, text_data):

#       checking that user is selling or not
        # print(json.loads(text_data)['msg'])
        if  json.loads(text_data)['msg'] == "sell":
            self.current_user = json.loads(text_data)['current_user'] 
            self.unit_sell_price = json.loads(text_data)['unit_sell_price']
            self.sell_volume = json.loads(text_data)['sell_volume'] 
            self.sell_total_price = json.loads(text_data)['sell_total_price'] 
            self.user_cid_name = json.loads(text_data)['user_cid_name']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type' : 'p2p_sell_data_save',
                    'current_user' : self.current_user,
                    'unit_sell_price' : self.unit_sell_price,
                    'sell_volume' : self.sell_volume,
                    'sell_total_price' : self.sell_total_price,
                    'user_cid_name' : self.user_cid_name,
                    'msg' : 'sell_done'
                }
            )


        if not self.pair_name:
            self.pair_name = 'BTCUSDT'
        
        self.single_coin =  await self.getting_single_pair_name()
        # print(self.single_coin.pair_vol)
        self.json_single_coin = await sync_to_async(serialize)('json', [self.single_coin])

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type' : 'p2p_pairs',
                'msg'  : json.loads(text_data)['msg'],
                'fetched_pairs' : self.json_fetched_pairs, 
                'single_pair' : self.json_single_coin 
            }
        )


    async def p2p_pairs(self, event):
        msg = event['msg']
        fetched_pairs = event['fetched_pairs']
        single_pair = event['single_pair']

        await self.send(text_data = json.dumps({

                'msg' : 'connected', 
                'fetched_pairs' : self.json_fetched_pairs, 
                'single_pair' : self.json_single_coin 
        }))

    async def p2p_sell_data_save(self, event):
        

        current_user = event['current_user']
        unit_sell_price = event['unit_sell_price']
        sell_volume = event['sell_volume']
        sell_total_price = event['sell_total_price']
        user_cid_name = event['user_cid_name']
        print(current_user, unit_sell_price, sell_volume, sell_total_price, user_cid_name)
        
        await self.send(text_data = json.dumps({

                'msg' : 'sold', 
                'current_user' : current_user,
                'unit_sell_price' : unit_sell_price,
                'sell_volume' : sell_volume,
                'sell_total_price' : sell_total_price,
                'user_cid_name' : user_cid_name,
        }))

#   getting some pairs to for p2p pairs

    @database_sync_to_async
    def get_some_pairs(self):

        p2p_pair_option = CoinPair.objects.filter(pair_name__endswith = 'USDT')

        return p2p_pair_option

#   getting single coin and its price
    @database_sync_to_async
    def getting_single_pair_name(self):
        single_obj = CoinPair.objects.get(pair_name = self.pair_name)
        return single_obj


    async def disconnect(self, close_code):
        print('disconnected')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
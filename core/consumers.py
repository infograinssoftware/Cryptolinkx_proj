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

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print('connected')

        self.fetched_pairs = await self.get_some_pairs()
        self.json_fetched_pairs = await sync_to_async(serialize)('json', self.fetched_pairs)

        await self.send(text_data = json.dumps({'msg' : 'connected', 'fetched_pairs' : self.json_fetched_pairs}))

    async def receive(self, text_data):
        pass

    async def disconnect(self, close_code):
        pass
    

#   getting some pairs to for p2p pairs

    @database_sync_to_async
    def get_some_pairs(self):

        p2p_pair_option = CoinPair.objects.filter(pair_name__endswith = 'USDT')

        return p2p_pair_option

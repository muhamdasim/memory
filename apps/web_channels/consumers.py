import json
from random import randint
from time import sleep
from asgiref.sync import async_to_sync

# from channels.generic.websocket import WebsocketConsumer, SyncConsumer
from channels.consumer import SyncConsumer


class TherapyConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print(f"[{self.channel_name}] - just joined")
        self.room_name = "bcast"
        self.send({"type": "websocket.accept"})
        async_to_sync(self.channel_layer.group_add)(self.room_name, self.channel_name)

    def websocket_receive(self, event):
        print(f"[{self.channel_name}] - received {event['text']}")
        async_to_sync(self.channel_layer.group_send)(self.room_name, {
            "type": "websocket.message",
            "text": event["text"]
        })

    def websocket_message(self, event):
        print(f"[{self.channel_name}] - sent {event['text']}")
        self.send({
            "type": "websocket.send",
            "text": event["text"]
        })

    def websocket_disconnect(self, event):
        print("websocket_disconnect:", event)
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)


# class WSConsumer(WebsocketConsumer):
#
#     def connect(self):
#         self.accept()
#         for i in range(1, 10):
#             self.send(json.dumps({'message': randint(1, 100)}))
#             sleep(5)

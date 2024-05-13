from channels.generic.websocket import AsyncWebsocketConsumer
import json

class SiparisDurumuConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Bağlantıyı kabul et
        await self.accept()

        # "siparis_durumu" grubuna katıl
        await self.channel_layer.group_add("siparis_durumu", self.channel_name)

    async def disconnect(self, close_code):
        # Bağlantıyı sonlandır
        await self.channel_layer.group_discard("siparis_durumu", self.channel_name)

    async def siparis_durumu_update(self, event):
        message = event['message']
        message_type = event['type']
        firma_kod = event['firma_kod']  # Eklenecek olan firma kodu

        await self.send(text_data=json.dumps({
            'type': message_type,
            'message': message,
            'firma_kod': firma_kod  # Eklendi
        }))
# class SiparisGeldiConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Bağlantıyı kabul et
#         await self.accept()

#         # "siparis_geldi" grubuna katıl
#         await self.channel_layer.group_add("siparis_geldi", self.channel_name)

#     async def disconnect(self, close_code):
#         # Bağlantıyı sonlandır
#         await self.channel_layer.group_discard("siparis_geldi", self.channel_name)

#     async def siparis_geldi_update(self, event):  # <-- 'siparis_geldi_update' olarak değiştirildi
#         message = event['message']
#         message_type = event['type']
#         firma_kod = event['firma_kod']  # Eklenecek olan firma kodu

#         await self.send(text_data=json.dumps({
#             'type': message_type,
#             'message': message,
#             'firma_kod': firma_kod
#         }))
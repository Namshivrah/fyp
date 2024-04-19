#creating a websocket consumer

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import FingerPrints

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Process received message (fingerprint data)
        fingerprint_data = json.loads(text_data)
        
        # Store the fingerprint data in the database
        FingerprintData.objects.create(
            fingerprint_id=fingerprint_data['id'],
            fingerprint_template=fingerprint_data['template'],
            # Add other fields as needed
        )
        
        # Send a confirmation message back to Arduino
        await self.send(text_data=json.dumps({'message': 'Fingerprint data received and stored.'}))
           
        

    async def send_message(self, text_data=None, bytes_data=None):
        # Send a message to the WebSocket connection
        if bytes_data:
            await self.send_bytes(bytes_data)
        elif text_data:
            # Send binary data if needed
            pass
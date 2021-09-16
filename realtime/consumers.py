from channels.generic.websocket import AsyncWebsocketConsumer
from blog.models import NotificationListener
from account.models import User, Friend, Message
from asgiref.sync import sync_to_async
import json

@sync_to_async
def create_notification_listener(username, notification_group_name):
	user = User.objects.get(username=username)
	if not NotificationListener.objects.filter(user=user).exists():
		NotificationListener.objects.create(user=user, notification_group_name=notification_group_name)

class NotificationConsumer(AsyncWebsocketConsumer):

	async def connect(self):
		username = self.scope['url_route']['kwargs']['username']
		self.notification_group_name = "notification_" + username

		await create_notification_listener(username=username, notification_group_name=self.notification_group_name)

		await self.channel_layer.group_add(
			self.notification_group_name,
			self.channel_name
		)

		await self.accept()

	async def disconnect(self):
	
		await self.channel_layer.group_discard(

			self.notification_group_name,
			self.channel_name
		)

	async def notification_message(self, event):
		message = event['message']
		await self.send(text_data=message)

@sync_to_async
def check_friendship(first_user, second_user):

	first_user  = User.objects.get(username=first_user)
	second_user = User.objects.get(username=second_user)

	if Friend.objects.filter(first_user=first_user, second_user=second_user).exists():
		chat_id = Friend.objects.get(first_user=first_user, second_user=second_user).chat_id
		return chat_id
	elif Friend.objects.filter(first_user=second_user, second_user=first_user).exists():
		chat_id = Friend.objects.get(first_user=second_user, second_user=first_user).chat_id
		return chat_id

@sync_to_async
def create_message(content, sender, receiver):

	sender   = User.objects.get(username=sender)
	receiver = User.objects.get(username=receiver)

	Message.objects.create(sender=sender, receiver=receiver, content=content)

class PrivateChatConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		first_user  = self.scope['url_route']['kwargs']['first_user']
		second_user = self.scope['url_route']['kwargs']['second_user']

		chat_id     = await check_friendship(first_user=first_user, second_user=second_user)

		if chat_id:

			self.group_name = 'private_chat_' + chat_id

			await self.channel_layer.group_add(

				self.group_name,
				self.channel_name
			)

			await self.accept()

	async def disconnect(self):
		await self.channel_layer.group_discard(

			self.group_name,
			self.channel_name
		)

	async def receive(self, text_data):

		cleared = json.loads(text_data)

		await create_message(content=cleared['content'], sender=cleared['sender'], receiver=cleared['receiver'])

		await self.channel_layer.group_send(

			self.group_name,
			{

				"type": "send_message",
				"message": cleared['content']
			}
		)

	async def send_message(self, event):	
		message = event['message']
		await self.send(text_data=message)
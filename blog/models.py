from django.db import models
from account.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# Create your models here.

class Post(models.Model):

	user    = models.ForeignKey(User, on_delete=models.CASCADE)
	caption = models.TextField(default='')
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user)

class Like(models.Model):

	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)		

	def __str__(self):
		return str(self.user)

class Comment(models.Model):
	
	user        = models.ForeignKey(User, on_delete=models.CASCADE)
	post        = models.ForeignKey(Post, on_delete=models.CASCADE)
	description = models.TextField(default='')
	created     = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user)

class Save(models.Model):

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.post)

class Notification(models.Model):

	noti_types = {

		('like', 'like')
	}

	noti_type = models.CharField(max_length=100)
	from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
	to_user   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')

	def __str__(self):
		return str(self.from_user)

	def push_notification(self, notification_group_name, message_inner):

		channel_layer = get_channel_layer()

		async_to_sync(channel_layer.group_send)(
			notification_group_name,
			{
				"type": "notification_message",
				"message": json.dumps(message_inner)
			}
		)	

class NotificationListener(models.Model):
	user                    = models.ForeignKey(User, on_delete=models.CASCADE)
	notification_group_name = models.CharField(max_length=300)

	def __str__(self):
		return self.notification_group_name

	def push_notification(self, message_inner):

		if message_inner:
			channel_layer = get_channel_layer()

			async_to_sync(channel_layer.group_send)(
				self.notification_group_name,
				{
					"type": "notification_message",
					"message": json.dumps(message_inner)
				}
			)
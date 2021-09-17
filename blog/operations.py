from .models import Notification, NotificationListener
from account.models import User

def CreatePushNotification(sender, receiver):
	# Creating a notification
	Notification.objects.create(noti_type=noti_type, sender=sender, receiver=receiver)

	# pushing the notification
	if NotificationListener.objects.filter(user=receiver).exists():
		notification_listener = NotificationListener.objects.filter(user=receiver)[0]
		message_inner = {"noti_type": noti_type,"sender": sender.username,"receiver": receiver.username}
		notification_listener.push_notification(message_inner=message_inner)
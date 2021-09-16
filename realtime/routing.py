from django.urls import path
from . import consumers

websocket_urlpatterns = [
	path("ws/notification/<username>/", consumers.NotificationConsumer.as_asgi()),
	path("ws/chat/private/<first_user>/<second_user>/", consumers.PrivateChatConsumer.as_asgi()),
]
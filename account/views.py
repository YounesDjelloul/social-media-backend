from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from blog.operations import CreatePushNotification

# Create your views here.

class SignUpView(APIView):
	serializer_class = UserSerializer

	def post(self, request):
		data       = request.data
		serializer = self.serializer_class(data=data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=201)

class GetProfileDataView(APIView):
	serializer_class = ProfileSerializer

	def get(self, request):
		query      = User.objects.get(username=request.data['username']).profile
		serializer = self.serializer_class(query)

		return Response(serializer.data, status=200)

class UpdateProfileDataView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		user      = request.user
		fullname  = request.data.get('fullname')
		bio       = request.data.get('bio')
		birthdate = request.data.get('birthdate')

		if fullname:
			user.profile.fullname = fullname
		if birthdate:
			user.profile.birthdate = birthdate
		if bio:
			user.profile.bio = bio

		user.profile.save()

		return Response('Profile Updated .', status=200)

class LogoutView(APIView):

	permission_classes = [IsAuthenticated]

	def post(self, request):
		token = Token.objects.get(user=request.user)
		token.delete()

		return Response('Logout successfully', status=200)


class CreateFriendRequestView(APIView):
	
	serializer_class   = FriendRequestSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		data = request.data
		user = request.user

		serializer = self.serializer_class(data=data)
		serializer.is_valid(raise_exception=True)
		
		data['receiver'] = User.objects.get(id=data['receiver'])

		FriendRequest.objects.create(sender=user, **data)

		CreatePushNotification(sender=user, receiver=data['receiver'], noti_type='request')

		return Response('Request Created Successfully', status=201)

class GetFriendRequestView(APIView):

	serializer_class   = FriendRequestSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		user  = request.user
		query = FriendRequest.objects.filter(receiver=user)
		serializer = self.serializer_class(query, many=True)

		return Response(serializer.data, status=200)

class ResponseFriendRequestView(APIView):

	permission_classes = [IsAuthenticated]

	def post(self, request):
		user              = request.user
		friend_request_id = request.data.get('request_id')
		response          = request.data.get('response')

		if not friend_request_id:
			return Response('request ID is required', status=400)

		if not response:
			return Response('Response for this request is required', status=400)

		friend_request = FriendRequest.objects.get(id=friend_request_id)
		
		if friend_request.receiver != user:
			return Response('Sorry, you do not have permission for this.', status=401)

		if response == "yes":
			chat_id = str(friend_request.receiver.username) + str(friend_request.sender.username)
			Friend.objects.create(first_user=friend_request.receiver, second_user=friend_request.sender, chat_id=chat_id)

			friend_request.delete()

			return Response('Friend Added Successfully', status=201)
		if response == "no":
			friend_request.delete()
			return Response('Request Denied Successfully', status=200)

class LoadOwnMessagesView(APIView):

	serializer_class   = MessageSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		user     = request.user
		receiver = request.data.get('receiver')

		if not receiver:
			return Response('receiver is required', status=400)

		receiver_obj = User.objects.get(id=receiver)
		query = Message.objects.filter(sender=user, receiver=receiver_obj)

		serializer = self.serializer_class(query, many=True)

		return Response(serializer.data, status=200)

class LoadOtherMessagesView(APIView):

	serializer_class   = MessageSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):
		user     = request.user
		sender   = request.data.get('sender')

		if not sender:
			return Response('sender is required', status=400)

		sender_obj = User.objects.get(id=sender)
		query = Message.objects.filter(sender=sender_obj, receiver=user)

		serializer = self.serializer_class(query, many=True)

		return Response(serializer.data, status=200)		
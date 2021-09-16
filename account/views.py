from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

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
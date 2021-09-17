from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model  = Profile
		fields = ['id', 'fullname', 'bio', 'birthdate']

class UserSerializer(serializers.ModelSerializer):

	password1 = serializers.CharField(max_length=100, write_only=True)
	password2 = serializers.CharField(max_length=100, write_only=True)
	profile   = ProfileSerializer(read_only=True)

	class Meta:
		model  = User
		fields = ['id', 'profile', 'username', 'password1', 'password2']

	def validate(self, attrs):
		
		if not attrs.get('username'):
			raise serializers.ValidationError('Username is required to create an account')
		if not attrs.get('password1'):
			raise serializers.ValidationError('Username is required to create an account')
		if not attrs.get('password2'):
			raise serializers.ValidationError('Username is required to create an account')
		if attrs.get('password1') != attrs.get('password2'):
			raise serializers.ValidationError("Passwords didn't matched")

		return attrs

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)

class FriendRequestSerializer(serializers.ModelSerializer):

	sender = UserSerializer(read_only=True)

	class Meta:
		model  = FriendRequest
		fields = ['id', 'sender', 'receiver']

	def validate(self, attrs):
		if not attrs.get('receiver'):
			raise serializers.ValidationError('Receiver User is required')

		return attrs

class MessageSerializer(serializers.ModelSerializer):

	sender   = UserSerializer(read_only=True)
	receiver = UserSerializer()

	class Meta:
		model  = Message
		fields = ['id', 'sender', 'receiver', 'content']
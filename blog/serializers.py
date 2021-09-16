from rest_framework import serializers
from .models import *
from account.models import User
from account.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):

	user = UserSerializer(read_only=True)

	class Meta:
		model  = Post
		fields = ['id', 'user', 'caption', 'created']

	def validate(self, attrs):
		caption = attrs.get('caption')

		if not caption:
			raise serializers.ValidationError('caption is required to create a post')

		return attrs

class CommentSerializer(serializers.ModelSerializer):

	user = UserSerializer(read_only=True)
	post = PostSerializer(read_only=True)

	class Meta:
		model  = Comment
		fields = ['id', 'user', 'post', 'description', 'created']

	def validate(self, attrs):

		if not attrs.get('description'):
			raise serializers.ValidationError('description is required to create a comment')

		return attrs

class SaveSerializer(serializers.ModelSerializer):

	user = UserSerializer(read_only=True)
	post = PostSerializer(read_only=True)

	class Meta:
		model  = Comment
		fields = ['id', 'user', 'post']
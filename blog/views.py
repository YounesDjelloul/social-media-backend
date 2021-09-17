from django.shortcuts import render
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from account.models import User
from .models import *
from .operations import CreatePushNotification

# Create your views here.

class CreatePostView(APIView):

	serializer_class   = PostSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		user       = request.user
		data       = request.data

		serializer = self.serializer_class(data=data)
		serializer.is_valid(raise_exception=True)
		
		post       = Post.objects.create(user=user, **data)

		return Response('Post Created Succesfully', status=201)

class AllPostsView(APIView):

	serializer_class   = PostSerializer

	def get(self, request):

		query      = Post.objects.all()
		serializer = self.serializer_class(query, many=True)

		return Response(serializer.data, status=200)

class CreateCommentView(APIView):

	serializer_class   = CommentSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		user = request.user
		data = request.data

		serializer = self.serializer_class(data=data)
		serializer.is_valid(raise_exception=True)
		
		data['post'] = Post.objects.get(id=request.data.get('post'))

		Comment.objects.create(user=user, **data)

		return Response('Comment Created Successfully', status=201)

class AllCommentsView(APIView):
	
	serializer_class   = CommentSerializer

	def get(self, request):
		query = Comment.objects.all()
		serializer = self.serializer_class(query, many=True)
		return Response(serializer.data, status=200)

class CreateSaveView(APIView):

	permission_classes = [IsAuthenticated]

	def post(self, request):

		user = request.user
		data = request.data

		data['post'] = Post.objects.get(id=request.data.get('post'))
		Save.objects.create(user=user, **data)

		return Response('The Post Saved Successfully', status=201)

class AllSavesView(APIView):

	serializer_class   = SaveSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):

		query      = Save.objects.filter(user=request.user)
		serializer = self.serializer_class(query, many=True)
		
		return Response(serializer.data, status=200)

class CreateLikeView(APIView):

	permission_classes = [IsAuthenticated]

	def post(self, request):
		data = request.data
		user = request.user

		if not data.get('post'):
			return Response('Post is required to create a like')

		post = Post.objects.get(id=data['post'])
		Like.objects.create(post=post, user=user)

		CreatePushNotification(from_user=user, to_user=post.user, noti_type='like')

		return Response('Like Added Successfully', status=201)
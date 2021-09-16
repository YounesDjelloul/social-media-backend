from django.urls import path
from .views import *

urlpatterns = [
    path('post/create/', CreatePostView.as_view(), name='createpost'),
    path('post/all/', AllPostsView.as_view(), name='allposts'),

    path('comment/create/', CreateCommentView.as_view(), name='createcomment'),
    path('comment/all/', AllCommentsView.as_view(), name='allcomments'),

    path('save/create/', CreateSaveView.as_view(), name='createsave'),
    path('save/all/', AllSavesView.as_view(), name='allsaves'),

    path('like/create/', CreateLikeView.as_view(), name='createlike'),
]
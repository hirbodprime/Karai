from django.urls import path

from . import views as custom_views


urlpatterns = [
    path('post/create/', custom_views.PostCreateAPIView.as_view(), name='post_create'),
    path('post/list/', custom_views.PostListAPIView.as_view(), name='post_list'),
    path('post/get/<int:pk>/', custom_views.PostDetailAPIView.as_view(), name='post_detail'),
    path('comment/create/', custom_views.CommentCreateAPIView.as_view(), name='comment_create'),
    path('comment/list/<int:pk>/', custom_views.CommentListAPIView.as_view(), name='comment_list'),
    path('comment/reply/create/', custom_views.CommentReplyCreateAPIView.as_view(), name='comment_reply_create'),
    path('comment/reply/list/<int:pk>/', custom_views.CommentReplyListAPIView.as_view(), name='comment_reply_list'),
]

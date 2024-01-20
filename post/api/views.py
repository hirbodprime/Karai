from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers as custom_serializer
from post.models import PostModel, CommentModel, CommentReplyModel


class PostCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializer.PostCreateSerializer


class PostListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializer.PostListSerializer
    queryset = PostModel.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {'data': serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)
    

class PostDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializer.PostDetailSerializer
    queryset = PostModel.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {'data': serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)
    

class CommentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializer.CommentCreateSerializer
    

class CommentListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializer.CommentSerializer
    
    def get_queryset(self):
        try:
            PostModel.objects.get(pk=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            raise ValidationError(f"Post with id {self.kwargs.get('pk')} does not exists.")
        return CommentModel.objects.filter(post=self.kwargs.get('pk')).exclude(commentreplymodel__isnull=False)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {'data': serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)
    

class CommentReplyCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializer.CommentReplyCreateSerializer
    

class CommentReplyListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = custom_serializer.CommentReplySerializer
    
    def get_queryset(self):
        try:
            CommentModel.objects.get(pk=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            raise ValidationError(f"Comment with id {self.kwargs.get('pk')} does not exists.")
        return CommentReplyModel.objects.filter(parent_comment=self.kwargs.get('pk'))        
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = {'data': serializer.data}
        return Response(response_data, status=status.HTTP_200_OK)
    
from django.conf import settings
from django.db.models import Count

from rest_framework import serializers

from post.models import PostModel, CommentModel, CommentReplyModel
from accounts.api.serializers import UserDetailSerializer


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['id', 'user', 'ai_generated', 'location', 'caption', 'image']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['id', 'user', 'post', 'text']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    

class CommentReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReplyModel
        fields = ['id', 'user', 'post', 'parent_comment', 'text']
        read_only_fields = ['id', 'user', 'post']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['post'] = validated_data['parent_comment'].post
        return super().create(validated_data)    


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['id', 'user', 'text', 'likes_count', 'created_at', 'updated_at']

    user = UserDetailSerializer()
    likes_count = serializers.SerializerMethodField(read_only=True)

    def get_likes_count(self, obj):
        return obj.likes.count()
    

class CommentReplySerializer(serializers.ModelSerializer):
    class Meta():
        model = CommentReplyModel
        fields = ['id', 'user', 'post', 'parent_comment', 'text', 'likes_count', 'created_at', 'updated_at', 'replies']

    user = UserDetailSerializer()
    likes_count = serializers.SerializerMethodField(read_only=True)
    replies = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_replies(self, obj):
        replies = CommentReplyModel.objects.filter(parent_comment=obj)
        return CommentReplySerializer(replies, many=True).data


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['id', 'user', 'ai_generated', 'location', 'caption', 'created_at', 'updated_at', 'image', 
                  'views_count', 'likes_count', 'comments_count', 'recent_likes', 'top_comments']

    user = UserDetailSerializer()
    top_comments = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    recent_likes = serializers.SerializerMethodField(read_only=True)

    def get_image(self, obj):
        if obj.image:
            return settings.SITE_DOMAIN + obj.image.url
        return

    def get_views_count(self, obj):
        return obj.views.count()
    
    def get_comments_count(self, obj):
        return CommentModel.objects.filter(post=obj).count()

    def get_top_comments(self, obj):
        if obj.post_comments:
            # top 3 liked comments (without replis)
            top_comments = obj.post_comments.exclude(commentreplymodel__isnull=False).annotate(likes_count=Count('likes')).order_by('-likes_count')[:3]
            return CommentSerializer(top_comments, many=True).data
        return

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_recent_likes(self, obj):
        recent_likes = obj.likes.order_by('pk')[:3]
        return [settings.SITE_DOMAIN + user_likes.profile_image.url for user_likes in recent_likes]


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['id', 'user', 'ai_generated', 'location', 'caption', 'created_at', 'updated_at', 'image']

    user = UserDetailSerializer()

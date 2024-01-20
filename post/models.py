from datetime import datetime
from django.db import models

from django.contrib.auth import get_user_model


UserModel = get_user_model()

def image_upload_path(instance, filename):
    return f'{instance.user.email}/posts/{datetime.now().strftime("%Y/%B/%d")}/{filename}'


class PostModel(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    user = models.ForeignKey(UserModel, related_name='posts', on_delete=models.CASCADE)
    ai_generated = models.BooleanField(default=True)
    image = models.ImageField(upload_to=image_upload_path)
    caption = models.TextField()
    location = models.CharField(max_length=255)
    views = models.ManyToManyField(UserModel, related_name='viewed_posts', blank=True)
    likes = models.ManyToManyField(UserModel, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk}. {self.user.email}: {self.caption[:20]}...'


class CommentModel(models.Model):
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    user = models.ForeignKey(UserModel, related_name='user_comments', on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, related_name='post_comments', on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.ManyToManyField(UserModel, related_name='comment_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk}. {self.user.email}: {self.text[:20]}...'


class CommentReplyModel(CommentModel, models.Model):
    class Meta:
        verbose_name = 'Comment Reply'
        verbose_name_plural = 'Comment Replies'

    parent_comment = models.ForeignKey(CommentModel, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk}. {self.parent_comment.pk}. {self.parent_comment.text[:20]}...: {self.user.email}: {self.text[:20]}...'

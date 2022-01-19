from django.db import models

from user.models import Profile


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField( blank=True, null=True)
    image = models.ImageField(upload_to = 'post/')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)


class Comment(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Likes(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')



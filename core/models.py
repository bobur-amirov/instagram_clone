from django.db import models
from django.db.models.signals import post_save
from django.utils.text import slugify

from user.models import Profile


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='post/')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_post')
    tags = models.ManyToManyField(Tag, related_name='tag_post', null=True, blank=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='follower')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='following')


class Stream(models.Model):
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='stream_following')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def add_post(sender, instance, *args, **kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.filter(following=user)
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.created_at, following=user)
            stream.save()


class Comment(models.Model):
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_comment')

    def __str__(self):
        return self.text


class Likes(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')


post_save.connect(Stream.add_post, sender=Post)

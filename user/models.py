from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    bio = models.CharField(max_length=100,null=True, blank=True)
    image = models.ImageField(upload_to='users/',null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=30,null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username


class Following(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='user')
    user_from = models.ManyToManyField(Profile, related_name='followed')
    user_to = models.ManyToManyField(Profile, related_name='follower')

    @classmethod
    def follow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.followed.add(another_account)
        print("followed")

    @classmethod
    def unfollow(cls, user, another_account):
        obj, create = cls.objects.get_or_create(user=user)
        obj.followed.remove(another_account)
        print("unfollowed")

    def __str__(self):
        return f'{self.user.username} Profile'
from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    bio = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='users/', null=True, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=30, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    favorites = models.ManyToManyField("core.Post", related_name='post_profile', blank=True, null=True)

    def __str__(self):
        return self.username

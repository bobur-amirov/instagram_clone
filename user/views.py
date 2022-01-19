from django.shortcuts import render

from core.models import Post
from .models import Profile


def profile(request, username):
    profile = Profile.objects.get(username=username)
    profile_posts = Post.objects.filter(user=profile)

    context = {
        'profile': profile,
        'profile_posts': profile_posts,
    }
    return render(request, 'profile.html', context)

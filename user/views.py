from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.urls import resolve

from core.models import Post, Follow, Stream
from .models import Profile
from .forms import ProfileForm, ProfileEditForm


def profile(request, username):
    profile = Profile.objects.get(username=username)
    url_name = resolve(request.path).url_name

    if url_name == 'profile':
        posts = Post.objects.filter(user=profile).order_by('-created_at')
    else:
        posts = profile.favorites.all()

    follow_status = Follow.objects.filter(following=profile, follower=request.user).exists()

    context = {
        'profile': profile,
        'posts': posts,
        'url_name': url_name,
        'follow_status': follow_status,
    }
    return render(request, 'profile.html', context)


class LoginPage(LoginView):
    template_name = 'registration/login.html'


def signup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.phone = form.cleaned_data['phone']
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('home')
    else:
        form = ProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/signup.html', context)


def follow(request, username, option):
    user = request.user
    following = get_object_or_404(Profile, username=username)

    try:
        f, created = Follow.objects.get_or_create(follower=user, following=following)
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=following, user=user).all().delete()
        else:
            posts = Post.objects.all().filter(user=following)[:10]

            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, following=following, date=post.created_at)
                    stream.save()
        return redirect('profile', username)
    except Profile.DoesNotExist:
        return redirect('profile', username)



def edit_profile(request, username):
    profile = get_object_or_404(Profile, username=username)
    form = ProfileEditForm(instance=profile)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('profile', username)

    context = {
        'form': form,
    }

    return render(request, 'registration/edit_profile.html', context)

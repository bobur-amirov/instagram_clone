from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import resolve

from core.models import Post, Follow
from .models import Profile
from .forms import ProfileForm


def profile(request, username):
    profile = Profile.objects.get(username=username)
    url_name = resolve(request.path).url_name

    if url_name == 'profile':
        posts = Post.objects.filter(user=profile).order_by('-created_at')
    else:
        posts = profile.favorites.all()

    context = {
        'profile': profile,
        'posts': posts,
        'url_name': url_name,
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

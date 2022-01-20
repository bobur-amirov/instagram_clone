from django.shortcuts import render, redirect

from core.models import Post
from .models import Profile
from .forms import ProfileForm


def profile(request, username):
    profile = Profile.objects.get(username=username)
    profile_posts = Post.objects.filter(user=profile)

    context = {
        'profile': profile,
        'profile_posts': profile_posts,
    }
    return render(request, 'user/profile.html', context)


def signup(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.phone = form.cleaned_data['phone']
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('profile', user.username)
    else:
        form = ProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'user/signup.html', context)

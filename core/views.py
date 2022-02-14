from django.shortcuts import render, redirect, get_object_or_404

from .models import Post, Comment, Likes, Stream, Tag
from .forms import CommentForm, PostForm
from user.models import Profile


def home(request):
    user = request.user
    post_stream = Stream.objects.filter(user=user)

    gruop_ids = []
    for post in post_stream:
        gruop_ids.append(post.post_id)

    posts = Post.objects.filter(id__in=gruop_ids).order_by('-created_at')

    context = {
        'posts': posts
    }

    return render(request, 'core/home.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    favorite = False

    if request.user.is_authenticated:
        profile = Profile.objects.get(username=request.user.username)

        if profile.favorites.filter(id=pk).exists():
            favorite = True

    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form_comment = form.save(commit=False)
            form_comment.profile = request.user
            form_comment.post = post
            form_comment.save()
            return redirect('post_detail', post.id)

    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'favorite': favorite,
    }

    return render(request, 'core/post_detail.html', context)


def new_post(request):
    user = request.user
    tags_obj = []

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            image = form.cleaned_data.get('image')
            tags_req = form.cleaned_data.get('tags')
            tag_list = list(tags_req.split(','))

            for tag in tag_list:
                t, created = Tag.objects.get_or_create(name=tag)
                tags_obj.append(t)

            p, created = Post.objects.get_or_create(title=title, content=content, image=image, user=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('home')
    else:
        form = PostForm()

    context = {
        'form': form
    }

    return render(request, 'core/post_add.html', context)


def tags(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag).order_by('-created_at')

    context = {
        'tag': tag,
        'posts': posts,
    }

    return render(request, 'core/tags.html', context)


def likes(request, pk):
    user = request.user
    post = Post.objects.get(pk=pk)
    current_like = post.likes

    liked = Likes.objects.filter(user=user, post=post).count()

    if not liked:
        like = Likes.objects.create(user=user, post=post)
        like.save()
        current_like = current_like + 1

    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_like = current_like - 1

    post.likes = current_like
    post.save()

    return redirect('post_detail', post.id)


def favorite(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    profile = Profile.objects.get(username=user.username)

    if profile.favorites.filter(id=pk).exists():
        profile.favorites.remove(post)
    else:
        profile.favorites.add(post)

    return redirect('post_detail', post.id)

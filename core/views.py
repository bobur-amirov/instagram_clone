from django.shortcuts import render, redirect

from .models import Post, Comment, Likes, Stream, Tag
from .forms import CommentForm, PostForm


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




def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        post_id = request.POST.get('post_id')
        if form.is_valid():
            form_comment = form.save(commit=False)
            form_comment.profile = request.user
            form_comment.post = Post.objects.get(id=post_id)
            form_comment.save()
            return redirect('post_detail', post.id)

    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }

    return render(request, 'core/post_detail.html', context)


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

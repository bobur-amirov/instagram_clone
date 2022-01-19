from django.shortcuts import render, redirect

from .models import Post, Comment, Likes
from .forms import CommentForm, PostForm


def post_list(request):
    posts = Post.objects.all()
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        post_id = request.POST.get('post_id')
        if form.is_valid():
            form_comment = form.save(commit=False)
            form_comment.profile = request.user
            form_comment.post = Post.objects.get(id=post_id)
            form_comment.save()
            # return redirect('post_list')

    context = {
        'posts': posts,
        'form': form,
    }

    return render(request, 'core/home.html', context)


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
        'comments':comments,
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

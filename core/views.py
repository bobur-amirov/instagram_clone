from django.shortcuts import render, redirect

from .models import Post
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
            return redirect('post_list')


    context = {
        'posts': posts,
        'form':form,
    }

    return render(request, 'core/home.html', context)


def post_detail(request, pk):
    post = Post.objects.get(pk=pk)    


    context = {
        'post': post,
    }

    return render(request, 'core/post_detail.html', context)

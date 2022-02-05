from dataclasses import field
from django import forms
from .models import Post,Comment


class PostForm(forms.ModelForm):
    title = forms.CharField(required=True)
    content = forms.CharField(required=True)
    image = forms.ImageField(required=True)
    tags = forms.CharField(required=True)
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tags']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
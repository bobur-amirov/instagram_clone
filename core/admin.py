from django.contrib import admin

from .models import Post, Comment, Follow, Stream, Tag


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Stream)

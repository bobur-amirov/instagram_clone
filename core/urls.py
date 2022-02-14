from django.urls import path


from .views import home, new_post, post_detail, likes, favorite, tags

urlpatterns = [
    path('', home, name='home'),
    path('add/', new_post, name='new_post'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('tag/<slug:slug>/', tags, name='tags'),
    path('like/<int:pk>/', likes, name='likes'),
    path('favorite/<int:pk>/', favorite, name='favorite'),
]

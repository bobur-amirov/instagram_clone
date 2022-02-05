from django.urls import path


from .views import home, new_post, post_detail, likes

urlpatterns = [
    path('', home, name='home'),
    path('add/', new_post, name='new_post'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('like/<int:pk>/', likes, name='likes'),
]

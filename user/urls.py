from django.urls import path


from .views import profile

urlpatterns = [
    path('<slug:username>', profile, name='profile'),
]

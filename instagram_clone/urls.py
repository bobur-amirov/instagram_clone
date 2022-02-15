from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from user.views import profile, follow

urlpatterns = [
    path('admin_/', admin.site.urls),
    path('', include('core.urls')),
    path('user/', include('user.urls')),
    path('<username>/', profile, name='profile'),
    path('<username>/saved', profile, name='profile_favorites'),
    path('<username>/follow<option>', follow, name='follow'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
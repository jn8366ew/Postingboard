from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from posting.views import base_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base_views.index, name='index'),
    path('posting/', include('posting.urls')),
    path('account/', include('account.urls')),
    path('user_profile/', include('user_profile.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

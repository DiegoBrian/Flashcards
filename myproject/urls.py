from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('language.urls')),
    path('russian/', include('russian.urls')),
    path('chinese/', include('chinese.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
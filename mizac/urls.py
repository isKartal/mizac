"""mizac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from main import views
from django.conf.urls.static import static

# Admin panel özelleştirmeleri
admin.site.site_header = "Mizac Yönetim Paneli"
admin.site.site_title = "Mizac Admin"
admin.site.index_title = "Hoş Geldiniz - Mizac Yönetim Paneli"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('temperaments/', include('temperaments.urls')),
    path('profiles/', include('profiles.urls')),
    path('testing_algorithm/', include('testing_algorithm.urls')),
    path('nested_admin/', include('nested_admin.urls')),
    path("google/login/", views.google_login, name="google_login"),
    path("oauth2callback/", views.google_callback, name="google_callback"),
    # Allauth satırını kaldırdık - çakışma yaratıyordu
]

# Static ve media dosyalarını sunmak için
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Hata sayfaları için handler'lar (opsiyonel)
# handler404 = 'main.views.error_404'
# handler500 = 'main.views.error_500'
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('temperaments/', include('temperaments.urls')),
    path('profiles/', include('profiles.urls')),
    path('testing_algorithm/', include('testing_algorithm.urls')),
    path('nested_admin/', include('nested_admin.urls')),
]
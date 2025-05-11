# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('google/login/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('social/', views.social_accounts, name='social_accounts'),
    path('social/connect/google/', views.connect_google, name='connect_google'),
    path('social/disconnect/<str:provider>/', views.disconnect_social, name='disconnect_social'),
    path('set-password/', views.set_password, name='set_password'),
]
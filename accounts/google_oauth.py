import os
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
import time

# Development ortamında HTTPS zorunluluğunu devre dışı bırak
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def get_google_auth_flow():
    """Google OAuth Flow'u oluşturur"""
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
                "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_OAUTH_REDIRECT_URI],
                "javascript_origins": ["http://localhost:8000"],
            }
        },
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
        ],
    )
    flow.redirect_uri = settings.GOOGLE_OAUTH_REDIRECT_URI
    return flow

def get_user_info(credentials):
    """Google OAuth token'dan kullanıcı bilgilerini alır"""
    request = requests.Request()
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            id_info = id_token.verify_oauth2_token(
                credentials.id_token, 
                request, 
                settings.GOOGLE_OAUTH_CLIENT_ID,
                clock_skew_in_seconds=60
            )
            return id_info
        except ValueError as e:
            if "Token used too early" in str(e) and attempt < max_retries - 1:
                time.sleep(1)  # 1 saniye bekle
                continue
            raise e
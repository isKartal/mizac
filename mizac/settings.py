# mizac/settings.py - PRODUCTION READY VERSION (FIXED)
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ================================
# SECURITY SETTINGS
# ================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure--7$tmakopcdtqrpjvl##@f-$qu&84)(&110&9+@#@-iey#5^hy')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# ALLOWED_HOSTS - Production/Development için dinamik
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
else:
    ALLOWED_HOSTS = ['4mizac1234.pythonanywhere.com', 'www.4mizac1234.pythonanywhere.com']

# ================================
# APPLICATION DEFINITION
# ================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Google OAuth için gerekli

    # Custom apps
    'main',
    'accounts',
    'profiles',
    'temperaments',
    'testing_algorithm',
    'nested_admin',

    # Performance & Optimization
    'imagekit',  # WebP optimization

    # OAuth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

# Sites framework için gerekli
SITE_ID = 1

# MIDDLEWARE - Production güvenlik optimizasyonu
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]

# GZip compression (production için)
if not DEBUG:
    MIDDLEWARE.append('django.middleware.gzip.GZipMiddleware')

MIDDLEWARE.extend([
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',  # Django-allauth için gerekli
])

ROOT_URLCONF = 'mizac.urls'

# ================================
# TEMPLATES CONFIGURATION
# ================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',  # Allauth için gerekli
            ],
        },
    },
]

WSGI_APPLICATION = 'mizac.wsgi.application'

# ================================
# DATABASE CONFIGURATION (FIXED)
# ================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Database optimization - Production için (SQLite uyumlu)
if not DEBUG:
    DATABASES['default'].update({
        'CONN_MAX_AGE': 600,  # 10 dakika connection reuse
        'OPTIONS': {
            'timeout': 60,  # SQLite için timeout
        }
    })

# ================================
# AUTHENTICATION & OAUTH (FIXED)
# ================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django-allauth authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Django-allauth configuration (Updated for latest version)
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_AUTHENTICATION_METHOD = "email"

ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'

# Social account configuration
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'OAUTH_PKCE_ENABLED': True,
        'APP': {
            'client_id': 'GOOGLE_OAUTH_CLIENT_ID',
            'secret': 'GOOGLE_OAUTH_CLIENT_SECRET',
            'key': ''
        }
    }
}


# Login/logout URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Allauth URL configuration
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True

# ================================
# PASSWORD VALIDATION
# ================================

# Production için güçlendirilmiş password validation
if not DEBUG:
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 8,
            }
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]
else:
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

# ================================
# INTERNATIONALIZATION
# ================================

LANGUAGE_CODE = 'tr'  # Türkçe
TIME_ZONE = 'Europe/Istanbul'  # Türkiye saati
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ================================
# STATIC & MEDIA FILES
# ================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# File upload settings - Güvenlik optimizasyonu
if not DEBUG:
    FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB (production için azaltıldı)
    DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
    DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000   # Azaltıldı
else:
    FILE_UPLOAD_MAX_MEMORY_SIZE = 26214400  # 25MB (development için)
    DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

FILE_UPLOAD_PERMISSIONS = 0o644

# Static files optimization - Production için
if not DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
    STATICFILES_FINDERS = [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]

# ================================
# REDIS CACHE CONFIGURATION
# ================================

# Redis connection settings
REDIS_ENABLED = os.getenv('USE_REDIS_CACHE', 'False').lower() == 'true'
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6380/1')

if REDIS_ENABLED:
    print("🚀 Redis Cache AKTIF - Maximum Performance Mode!")

    # Redis Cache Configuration
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 150,  # High performance
                    'retry_on_timeout': True,
                    'health_check_interval': 30,
                },
                'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
                'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            },
            'KEY_PREFIX': 'mizac_cache',
            'VERSION': 1,
            'TIMEOUT': 900,  # 15 minutes default
        },
        # Secondary cache for sessions
        'sessions': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL.replace('/1', '/2'),  # Different DB
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 50,
                    'retry_on_timeout': True,
                },
            },
            'KEY_PREFIX': 'mizac_session',
            'TIMEOUT': 3600,  # 1 hour for sessions
        }
    }

    # Use Redis for sessions
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'sessions'
    SESSION_COOKIE_AGE = 86400  # 24 hours
    SESSION_SAVE_EVERY_REQUEST = False  # Performance optimization

    # Template caching for maximum speed
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]
    TEMPLATES[0]['APP_DIRS'] = False  # Required when using cached loader

else:
    print("⚠️ Redis KAPALI - Local Memory Cache kullanılıyor")

    # Fallback: Local memory cache - Production için optimize edildi
    cache_max_entries = 5000 if not DEBUG else 2000
    cache_timeout = 600 if not DEBUG else 300

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'mizac-fallback-cache',
            'OPTIONS': {
                'MAX_ENTRIES': cache_max_entries,
                'CULL_FREQUENCY': 3,
            },
            'TIMEOUT': cache_timeout,
        }
    }

# ================================
# CACHE OPTIMIZATION SETTINGS
# ================================

# Cache key versioning for easy invalidation
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600  # 10 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'mizac'

# Cache-related settings - Production için optimize edildi
if not DEBUG:
    CACHE_TTL = {
        'element_suggestions': 1800,     # 30 dakika (arttırıldı)
        'user_test_results': 3600,      # 1 saat (arttırıldı)
        'temperament_pages': 1800,      # 30 dakika (arttırıldı)
        'api_responses': 300,           # 5 dakika (arttırıldı)
        'profile_stats': 900,           # 15 dakika (arttırıldı)
        'anonymous_pages': 3600,        # 1 saat (arttırıldı)
        'static_content': 86400,        # 24 saat (yeni)
    }
else:
    CACHE_TTL = {
        'element_suggestions': 600,      # 10 minutes
        'user_test_results': 1800,      # 30 minutes
        'temperament_pages': 900,       # 15 minutes
        'api_responses': 180,           # 3 minutes
        'profile_stats': 600,           # 10 minutes
        'anonymous_pages': 1800,        # 30 minutes
    }

# ================================
# WEBP IMAGE OPTIMIZATION
# ================================

# ImageKit configuration for WebP
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.JustInTime'
IMAGEKIT_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.source_name_dot_hash'
IMAGEKIT_SPEC_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.source_name_as_path'
IMAGEKIT_DEFAULT_CACHEFILE_BACKEND = 'imagekit.cachefiles.backends.Simple'

# WebP optimization settings - Production için optimize edildi
if not DEBUG:
    IMAGE_QUALITY_SETTINGS = {
        'webp_quality': 80,          # Küçük dosya boyutu için azaltıldı
        'webp_lossless': False,
        'jpeg_quality': 80,          # Küçük dosya boyutu için azaltıldı
        'png_compress_level': 9,     # Maksimum sıkıştırma
        'max_width': 1200,           # Küçük boyut
        'max_height': 600,           # Küçük boyut
        'progressive': True,
        'optimize': True,
    }
else:
    IMAGE_QUALITY_SETTINGS = {
        'webp_quality': 85,
        'webp_lossless': False,
        'jpeg_quality': 85,
        'png_compress_level': 6,
        'max_width': 1500,
        'max_height': 750,
        'progressive': True,
        'optimize': True,
    }

# ================================
# SESSION SECURITY - Production için
# ================================

if not DEBUG:
    SESSION_COOKIE_AGE = 86400  # 24 saat
    SESSION_SAVE_EVERY_REQUEST = False
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True  # HTTPS gerektirir
    SESSION_COOKIE_SAMESITE = 'Lax'

# ================================
# CSRF PROTECTION - Production için
# ================================

if not DEBUG:
    CSRF_COOKIE_AGE = 86400
    CSRF_USE_SESSIONS = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True  # HTTPS gerektirir
    CSRF_COOKIE_SAMESITE = 'Lax'

# ================================
# EMAIL CONFIGURATION
# ================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '4mizacinfo@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Email timeout ayarları
EMAIL_TIMEOUT = 30

# ================================
# LOGGING CONFIGURATION - İyileştirilmiş
# ================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'detailed': {
            'format': '{levelname} {asctime} {name} {module} {funcName} {lineno} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'mizac.log'),
            'formatter': 'verbose'
        },
        'cache_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'cache_performance.log'),
            'formatter': 'verbose'
        },
        'error_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'errors.log'),
            'formatter': 'detailed',
            'level': 'ERROR',
        },
        'security_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'security.log'),
            'formatter': 'detailed',
            'level': 'WARNING',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO' if DEBUG else 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'profiles.models': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django_redis': {
            'handlers': ['console', 'cache_file'],
            'level': 'INFO' if REDIS_ENABLED else 'WARNING',
            'propagate': False,
        },
        'mizac.cache': {
            'handlers': ['console', 'cache_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'mizac.errors': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# ================================
# PRODUCTION SECURITY SETTINGS - Güçlendirilmiş
# ================================

if not DEBUG:
    print("🔐 Production Security Settings AKTIF")

    # Security middleware settings
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # HTTPS settings (PythonAnywhere provides HTTPS)
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_HTTPONLY = True

    # Additional security headers
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # Content Security Policy (XSS koruması)
    CSP_DEFAULT_SRC = ("'self'",)
    CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
    CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
    CSP_IMG_SRC = ("'self'", "data:", "https:")
    CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")

else:
    print("🔧 Development Mode - Security relaxed")

    # Development'ta HTTPS ayarlarını kapat
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0

    # Bu ayarlar development'ta da güvenli
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_HTTPONLY = True

# ================================
# ADMIN PANEL GÜVENLİĞİ
# ================================

# Admin URL'sini gizle (production için)
ADMIN_URL = os.getenv('ADMIN_URL', 'admin/')

# Admin panel için IP kısıtlaması (isteğe bağlı)
ADMIN_ALLOWED_IPS = os.getenv('ADMIN_ALLOWED_IPS', '').split(',') if os.getenv('ADMIN_ALLOWED_IPS') else []

# ================================
# TEMPLATE OPTIMIZATION - Production için
# ================================

# Template cache loader (production'da)
if not DEBUG and not REDIS_ENABLED:  # Redis zaten template cache kullanıyor
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]
    TEMPLATES[0]['APP_DIRS'] = False

# ================================
# PERFORMANCE MONITORING - İyileştirilmiş
# ================================

# Performance settings
PERFORMANCE_MONITORING = {
    'cache_hit_rate_target': 90,    # %90 cache hit rate hedefi (arttırıldı)
    'max_response_time': 300,       # 300ms max response time (azaltıldı)
    'redis_max_memory': '256mb',
    'redis_eviction_policy': 'allkeys-lru',
    'db_connection_max_age': 600,   # 10 dakika
    'session_timeout': 86400,       # 24 saat
    'file_upload_max_size': 5242880,  # 5MB
}

# ================================
# RATE LIMITING - Güvenlik için
# ================================

# Rate limiting ayarları
RATELIMIT_ENABLE = not DEBUG
RATELIMIT_USE_CACHE = 'default'

# API rate limits
API_RATE_LIMITS = {
    'default': '100/hour',
    'login': '10/minute',
    'register': '5/minute',
    'contact': '20/hour',
    'test': '5/hour',
}

# ================================
# DEVELOPMENT HELPERS
# ================================

if DEBUG:
    # Development only settings
    INTERNAL_IPS = ['127.0.0.1', 'localhost']

    # Cache debugging
    CACHE_DEBUG = True

    # Django Debug Toolbar (isteğe bağlı)
    # INSTALLED_APPS.append('debug_toolbar')
    # MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    print("🔧 Development Mode:")
    print(f"   Redis Enabled: {REDIS_ENABLED}")
    print(f"   Cache Backend: {CACHES['default']['BACKEND']}")
    print(f"   Debug Mode: {DEBUG}")
    print(f"   Allowed Hosts: {ALLOWED_HOSTS}")

# ================================
# CACHE HEALTH CHECK
# ================================

def test_cache_connection():
    """Cache bağlantısını test et"""
    try:
        from django.core.cache import cache
        cache.set('health_check', 'OK', 30)
        result = cache.get('health_check')
        if result == 'OK':
            print("✅ Cache connection: HEALTHY")
            return True
        else:
            print("❌ Cache connection: FAILED")
            return False
    except Exception as e:
        print(f"❌ Cache connection error: {e}")
        return False

# Auto-test cache on startup (development only)
if DEBUG:
    import threading
    def delayed_cache_test():
        import time
        time.sleep(2)  # Django'nun başlaması için bekle
        test_cache_connection()

    thread = threading.Thread(target=delayed_cache_test)
    thread.daemon = True
    thread.start()

# ================================
# SECURITY HEADERS MIDDLEWARE
# ================================

# Custom security headers (isteğe bağlı)
SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'X-XSS-Protection': '1; mode=block',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'geolocation=(), camera=(), microphone=()',
}

# ================================
# BACKUP & MAINTENANCE
# ================================

# Backup settings (production için)
if not DEBUG:
    BACKUP_ENABLED = True
    BACKUP_LOCATION = os.path.join(BASE_DIR, 'backups')
    BACKUP_RETENTION_DAYS = 30

    # Maintenance mode
    MAINTENANCE_MODE = os.getenv('MAINTENANCE_MODE', 'False').lower() == 'true'
    MAINTENANCE_MESSAGE = "Site bakımda. Lütfen daha sonra tekrar deneyin."

# ================================
# HEALTH CHECK ENDPOINTS
# ================================

# Health check için basit endpoint
HEALTH_CHECK_ENABLED = True
HEALTH_CHECK_URL = '/health/'

# ================================
# CUSTOM ERROR PAGES
# ================================

# Custom error handlers
USE_CUSTOM_ERROR_PAGES = not DEBUG

# ================================
# FINAL PRODUCTION CHECKS
# ================================

# Production ortamında gerekli ayarların kontrolü
if not DEBUG:
    # Environment variables kontrolü
    required_env_vars = [
        'SECRET_KEY',
        'GOOGLE_CLIENT_ID',
        'GOOGLE_CLIENT_SECRET',
        'EMAIL_HOST_PASSWORD',
    ]

    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        print(f"⚠️  UYARI: Eksik environment variables: {missing_vars}")

    # Güvenlik kontrolleri
    if SECRET_KEY.startswith('django-insecure-'):
        print("⚠️  UYARI: Production'da güvenli SECRET_KEY kullanın!")

    print("✅ Production settings aktif - Site kullanıma hazır!")
    # ================================
# GOOGLE OAUTH - Basit Ayar Formatı
# ================================

GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID')
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')
GOOGLE_OAUTH_REDIRECT_URI = os.getenv('GOOGLE_OAUTH_REDIRECT_URI')

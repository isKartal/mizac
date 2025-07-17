# mizac/settings.py - REDIS OPTIMIZED VERSION
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

ALLOWED_HOSTS = ['4mizac1234.pythonanywhere.com', 'localhost', '127.0.0.1']

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
    # Custom apps
    'main',
    'accounts',
    'profiles',
    'temperaments',
    'testing_algorithm',
    'nested_admin',
    # Performance & Optimization
    'imagekit',  # WebP optimization
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
            ],
        },
    },
]

WSGI_APPLICATION = 'mizac.wsgi.application'

# ================================
# DATABASE CONFIGURATION
# ================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ================================
# PASSWORD VALIDATION
# ================================

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

# File upload settings - WebP optimizasyonu için artırıldı
FILE_UPLOAD_MAX_MEMORY_SIZE = 26214400  # 25MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
FILE_UPLOAD_PERMISSIONS = 0o644

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
    
    # Fallback: Local memory cache
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'mizac-fallback-cache',
            'OPTIONS': {
                'MAX_ENTRIES': 2000,
                'CULL_FREQUENCY': 3,
            },
            'TIMEOUT': 300,  # 5 minutes
        }
    }

# ================================
# CACHE OPTIMIZATION SETTINGS
# ================================

# Cache key versioning for easy invalidation
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600  # 10 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'mizac'

# Cache-related settings
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

# WebP optimization settings
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
# AUTHENTICATION & OAUTH
# ================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Google OAuth settings
GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_OAUTH_REDIRECT_URI = 'https://4mizac1234.pythonanywhere.com/accounts/google/callback/'

# Login URLs
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ================================
# EMAIL CONFIGURATION
# ================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '4mizacinfo@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# ================================
# LOGGING CONFIGURATION
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
    },
    'loggers': {
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
    },
}

# ================================
# PRODUCTION SECURITY SETTINGS
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
    
    # Additional security
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    
else:
    print("🔧 Development Mode - Security relaxed")

# ================================
# PERFORMANCE MONITORING
# ================================

# Performance settings
PERFORMANCE_MONITORING = {
    'cache_hit_rate_target': 85,  # %85 cache hit rate hedefi
    'max_response_time': 500,     # 500ms max response time
    'redis_max_memory': '256mb',
    'redis_eviction_policy': 'allkeys-lru',
}

# ================================
# DEVELOPMENT HELPERS
# ================================

if DEBUG:
    # Development only settings
    INTERNAL_IPS = ['127.0.0.1', 'localhost']
    
    # Cache debugging
    CACHE_DEBUG = True
    
    print("🔧 Development Mode:")
    print(f"   Redis Enabled: {REDIS_ENABLED}")
    print(f"   Cache Backend: {CACHES['default']['BACKEND']}")
    print(f"   Debug Mode: {DEBUG}")

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
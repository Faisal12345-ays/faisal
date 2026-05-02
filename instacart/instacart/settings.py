from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-v!y#0z3u*$b@*7q!dqbugzexqse1i93de_ci7!arb3y3gbfk##'

DEBUG = True

ALLOWED_HOSTS = []

# ==============================================================================
# APPS CONFIGURATION (JAZZMIN TOP PAR HONA CHAHIYE)
# ==============================================================================
INSTALLED_APPS = [
    'jazzmin',             # <--- NO. 1 PAR JAZZMIN
    'django.contrib.admin', # <--- NO. 2 PAR ADMIN
    'core',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Aapki Apps
    'products',
    'orders',
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

ROOT_URLCONF = 'instacart.urls'

# ==============================================================================
# TEMPLATES CONFIGURATION
# ==============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Templates folder link
        'APP_DIRS': True, # Iska TRUE hona zaroori hai Jazzmin ke liye
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'instacart.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================
# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (Uploaded Images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' # Ya os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# JAZZMIN CONFIGURATION (PROFESSIONAL DESIGN)
# ==============================================================================
JAZZMIN_SETTINGS = {
    "custom_css": "css/admin_custom.css",
    "site_title": "Instacart Admin",
    "site_header": "Instacart",
    "site_brand": "Instacart Grocery",
    "welcome_sign": "Welcome Faisal, Manage your Store!",
    "copyright": "Instacart Faisal 2026",
    "search_model": ["products.Product"],
    "show_ui_builder": False,
    "related_modal_active": False, # RECURSION ERROR FIX
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-primary",
    "navbar": "navbar-success navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-success",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_hover_elevate": False,
    "sidebar_activate_nav_child_group": True,
    "theme": "default",
}
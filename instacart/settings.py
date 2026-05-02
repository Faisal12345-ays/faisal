from pathlib import Path
import os

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-2h(av&iebp^)4t5ml!j*73sp98njm_-jklt^azy#yt4gd&+bkd'

DEBUG = True

ALLOWED_HOSTS = ['*'] # Taake koi bhi link se website khul sakay

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'rest_framework',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Local Apps
    'products',
    'orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'instacart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
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

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static & Media Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Ye line files ko compress karti hai taake site fast chale
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL CONFIGURATION
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 🔥 AUTH REDIRECTS (Signup/Login ke liye zaroori)
# settings.py

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'product_list'
LOGOUT_REDIRECT_URL = 'login'


# ==============================================================================
# JAZZMIN SETTINGS (RECURSION ERROR FIX & DESIGN)
# ==============================================================================
JAZZMIN_SETTINGS = {
    "site_title": "InstaCart Admin",
    "site_header": "InstaCart Dashboard 🚀",
    "site_brand": "InstaCart",
    "welcome_sign": "Welcome Faisal 👋",
    "copyright": "InstaCart Faisal 2026",

    # 🔗 Top Menu
    "topmenu_links": [
        {"name": "Home", "url": "admin:index"},
        {"name": "Dashboard", "url": "/cart/dashboard/"},
        {"name": "View Site", "url": "product_list"},
    ],

    # 🎨 Icons
    "icons": {
        "products.Product": "fas fa-box",
        "products.Category": "fas fa-tags",
        "orders.Order": "fas fa-shopping-cart",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },

    # 🌙 Theme & CSS
    "theme": "flatly",
    "custom_css": "css/admin_custom.css",

    # 📦 Sidebar
    "show_sidebar": True,
    "navigation_expanded": True,

    # 🎯 Order of apps
    "order_with_respect_to": ["products", "orders", "auth"],

    # 🧾 Change list style
    "changeform_format": "horizontal_tabs",

    # 🛑 RECURSION ERROR FIX (SAB SE ZAROORI)
    "related_modal_active": False, 
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
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
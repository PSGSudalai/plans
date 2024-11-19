from pathlib import Path
import environ
import os


env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent

# Load the .env file based on the environment
ENVIRONMENT = env.str("ENVIRONMENT", "local")
env_file = os.path.join(BASE_DIR, f".env.{ENVIRONMENT}")
env.read_env(env_file)

# Security settings
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

# Application definition
DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
OTHER_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
]
CUSTOM_APPS = [
    "apps.BASE",
    "apps.PLAN_ACCESS",
    "apps.PLAN_ADMIN",
]

INSTALLED_APPS = DEFAULT_APPS + OTHER_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # Use MySQL backend
#         'NAME': 'db_staging_erp',              # Database name
#         'USER': 'TestERP',                     # Your database username
#         'PASSWORD': 'TestERP@2024',            # Your database password
#         'HOST': '92.205.4.188',                # Host (use 'localhost' if hosted locally on cPanel)
#         'PORT': '3306',                        # Default MySQL port
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # MySQL database backend
#         'NAME': 'db_Roriri_ERP',               # The name of the MySQL database (updated)
#         'USER': 'roririERP',                   # MySQL username (updated)
#         'PASSWORD': 'RoririERP@2024',          # MySQL password (updated)
#         'HOST': '92.205.4.188',                # Server IP or hostname
#         'PORT': '3306',                        # Default MySQL port
#     }
# }
DATABASES = {
    "default": env.db("DATABASE_URL", default=f"sqlite:///{BASE_DIR}/db.sqlite3")
}

# Authentication and authorization
AUTH_USER_MODEL = "PLAN_ACCESS.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "https://online.nexemy.com",
    "https://admin.nexemy.com",
]


# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
}

# Time and language settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static and media files
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Email settings
EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")


# Backup
BACKUP_PASSWORD = env("BACKUP_PASSWORD", default="")
BACKUP_OTP = env("BACKUP_OTP", default="")

# External services
RAZORPAY_KEY_ID = env("RAZORPAY_KEY_ID", default="")
RAZORPAY_SECRET_KEY = env("RAZORPAY_SECRET_KEY", default="")

# Custom settings
BACKEND_URL = env("BACKEND_URL", default="http://127.0.0.1:8000")
FRONTEND_URL = env("FRONTEND_URL", default="http://localhost:5713")

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"request_id": {"()": "log_request_id.filters.RequestIDFilter"}},
    "formatters": {
        "aws": {
            "format": "%(levelname)-8s [%(asctime)s] %(request_id)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {},
    "loggers": {
        "Nexemy-logger": {
            "level": "DEBUG",
            "handlers": [],
            "propagate": True,
        },
    },
}


# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

"""
BLUS Web App — Django Settings

Environment-driven config using django-environ + dj-database-url.
- Local:   reads values from a .env file (DEBUG on, SQLite).
- Railway: env vars are injected directly; PostgreSQL via DATABASE_URL.
"""

from pathlib import Path
import os

import environ
import dj_database_url

# ── Paths ──────────────────────────────────────────────────────────────────────
# settings.py lives at  <project>/config/settings.py
# so .parent.parent == <project>/  (where manage.py and db.sqlite3 live).
BASE_DIR = Path(__file__).resolve().parent.parent

# ── Environ setup ──────────────────────────────────────────────────────────────
env = environ.Env()

# Load the .env file ONLY in local development. On Railway the file does not
# exist (env vars are injected), and calling read_env on a missing file would
# raise FileNotFoundError. The guard makes the same code safe in both places.
_env_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(_env_file):
    environ.Env.read_env(_env_file)

# ── Core flags ─────────────────────────────────────────────────────────────────
SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)

# Explicit production switch. Set IS_PRODUCTION=True on Railway.
# Drives SSL-require on the DB and all the security hardening at the bottom.
IS_PRODUCTION = env.bool("IS_PRODUCTION", default=False)

# ── Hosts / CSRF ───────────────────────────────────────────────────────────────
# Override these on Railway via env vars. Defaults cover local + the live domain.
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[
        "127.0.0.1",
        "localhost",
        "beijing-union-of-liberian-students.up.railway.app",
    ],
)

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "https://beijing-union-of-liberian-students.up.railway.app",
    ],
)

# Railway injects RAILWAY_PUBLIC_DOMAIN automatically. Add it to both lists so the
# app keeps working even if the domain changes or the env vars above are missing.
_railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
if _railway_domain:
    if _railway_domain not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_railway_domain)
    _railway_origin = f"https://{_railway_domain}"
    if _railway_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_railway_origin)

# Railway's internal healthcheck hits the service under this hostname.
if "healthcheck.railway.app" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("healthcheck.railway.app")

# ── Applications ───────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "jazzmin",  # must be before django.contrib.admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "corsheaders",
    # Project apps
    "apps.accounts",
    "apps.administration",
    "apps.students",
    "apps.events",
    "apps.finance",
    "apps.blog",
]

# ── Middleware ─────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise must be directly after SecurityMiddleware
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ── Templates ──────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "frontend" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.accounts.context_processors.admin_shell_stats",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ── Database ───────────────────────────────────────────────────────────────────
# DATABASE_URL set      → PostgreSQL (Railway injects this automatically).
# DATABASE_URL not set  → SQLite (local development fallback).
DATABASE_URL = env.str("DATABASE_URL", default=None)
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=IS_PRODUCTION,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ── Password validation ────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── Internationalisation ───────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ── Static files ───────────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Static files storage:
#   Production → WhiteNoise compressed + hashed (cache-busting) manifest storage.
#                Requires `collectstatic` and serves fingerprinted filenames.
#   Development → plain storage: serves files live from /static, no collectstatic,
#                edits appear on refresh. (Manifest storage in dev forces a
#                collectstatic after every CSS change — a common "stale CSS" trap.)
if IS_PRODUCTION:
    _staticfiles_backend = "whitenoise.storage.CompressedManifestStaticFilesStorage"
else:
    _staticfiles_backend = "django.contrib.staticfiles.storage.StaticFilesStorage"

# Media storage: local disk by default (fine for local dev). If
# AWS_STORAGE_BUCKET_NAME is set, switch to S3Storage — required in production
# because Railway's filesystem is ephemeral and uploads are lost on every
# redeploy otherwise. Works with real AWS S3 or any S3-compatible provider
# (Cloudflare R2, Backblaze B2, etc. — set AWS_S3_ENDPOINT_URL for those).
AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME", default="")

if AWS_STORAGE_BUCKET_NAME:
    _default_storage_backend = "storages.backends.s3.S3Storage"
    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID", default="")
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY", default="")
    AWS_S3_REGION_NAME = env.str("AWS_S3_REGION_NAME", default="auto")
    AWS_S3_ENDPOINT_URL = env.str("AWS_S3_ENDPOINT_URL", default=None)  # unset for real AWS S3
    AWS_S3_FILE_OVERWRITE = False   # preserve Django's automatic filename de-duplication
    AWS_QUERYSTRING_AUTH = False    # plain URLs — media is public today, no signed links
else:
    _default_storage_backend = "django.core.files.storage.FileSystemStorage"

STORAGES = {
    "default": {
        "BACKEND": _default_storage_backend,
    },
    "staticfiles": {
        "BACKEND": _staticfiles_backend,
    },
}

# ── Media files ────────────────────────────────────────────────────────────────
# Still used by the local-disk fallback above; harmless when S3Storage is active.
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ── Auth ───────────────────────────────────────────────────────────────────────
# Tells Django to use our custom user model everywhere instead of the default.
AUTH_USER_MODEL = "accounts.User"

LOGIN_REDIRECT_URL = "administration:dashboard"
LOGOUT_REDIRECT_URL = "accounts:login"
LOGIN_URL = "accounts:login"

# ── Django REST Framework ──────────────────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# ── CORS ───────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = True

# ── Logging ────────────────────────────────────────────────────────────────────
# Railway captures stdout, so a console handler is sufficient — no file handler.
LOG_LEVEL = env.str("LOG_LEVEL", default="DEBUG" if DEBUG else "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{asctime} {levelname} {name} {message}", "style": "{"},
        "simple": {"format": "{levelname} {name} {message}", "style": "{"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",   # 5xx / unhandled exceptions only — suppresses routine 4xx noise
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# ── Production security hardening (applied only when IS_PRODUCTION=True) ────────
if IS_PRODUCTION:
    # Trust the X-Forwarded-Proto header set by Railway's load balancer.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # OFF on Railway: the healthcheck sends plain HTTP and expects a 200.
    # A 301 redirect would fail the healthcheck. SSL is enforced at Railway's edge.
    SECURE_SSL_REDIRECT = False

    SECURE_HSTS_SECONDS = 31_536_000   # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "DENY"

# ── Misc ───────────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

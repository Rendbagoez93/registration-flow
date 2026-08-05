from .base import *  # noqa: F403

DEBUG = False

# SECURITY WARNING: fail fast if the app is misconfigured for production.
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ["localhost", "127.0.0.1"]:  # noqa: F405
    raise ValueError("ALLOWED_HOSTS must be explicitly configured in production.")

if not CSRF_TRUSTED_ORIGINS:  # noqa: F405
    raise ValueError("CSRF_TRUSTED_ORIGINS must be explicitly configured in production.")

# HTTPS / transport security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

# Trust the proxy-set scheme header when running behind a TLS-terminating
# load balancer / reverse proxy (e.g. nginx, ALB, Cloud Run).
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Serve pre-compressed, cache-busted static assets without extra infra.
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"  # noqa: F405

# Reuse database connections instead of opening one per request.
for _db_config in DATABASES.values():  # noqa: F405
    _db_config["CONN_MAX_AGE"] = 60
    _db_config["CONN_HEALTH_CHECKS"] = True
del _db_config


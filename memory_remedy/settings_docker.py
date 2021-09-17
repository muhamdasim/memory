from .settings import *

DOMAIN = "http://app.memoryremedy.io"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('redis', 6379)],
        },
    },
}

SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
REDIS_URL = 'redis://redis:6379'  # from docker compose file
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'memory_remedy',
        'USER': 'admin',
        'PASSWORD': 'testpass!',
        'HOST': 'db',  # from docker compose file
        'PORT': '5432',
    }
}

# populate this to configure sentry. should take the form: 'https://****@sentry.io/12345'
SENTRY_DSN = 'https://b075fbc3d5144f2884728218e0f4f147@o924133.ingest.sentry.io/5872083'


if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )
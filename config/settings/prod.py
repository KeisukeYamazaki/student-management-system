import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['DOMAIN_NAME', 'XXX.XXX.XXX.XXX', 'localhost', ]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'NAME',
        'USER': 'USER',
        'PASSWORD': 'PASSWORD',
        # 'USER': os.environ['DJANGO_SMS_DB_USER'],
        # 'PASSWORD': os.environ['DJANGO_SMS_DB_PASSWORD'],
        # 'HOST': os.environ['DJANGO_SMS_DB_HOST'],
        # 'PORT': os.environ['DJANGO_SMS_DB_PORT'],
    }
}

INSTALLED_APPS += (
    'gunicorn',
)

# セッションの設定
SESSION_COOKIE_AGE = 900   # 15分
SESSION_SAVE_EVERY_REQUEST = True   # 1リクエストごとにセッション情報を更新

ADMINS = [('Keisuke', 'MAIL_Address'), ]

SERVER_EMAIL = 'MAIL_Address'

# ロギング
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        # アプリケーションが利用するロガー
        'home': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'student': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'registry': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'download': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'zenken': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'cron': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },

    # ハンドラの設定
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'prod',
            'when': 'D',  # ログローテーション(新しいファイルへの切り替え)間隔の単位(D=日)
            'interval': 1,  # ログローテーション間隔(1日単位)
            'backupCount': 14,  # 保存しておくログファイル数
        },
    },

    # フォーマッタの設定
    'formatters': {
        'prod': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

sentry_sdk.init(
    dsn='SENTRY_DSN',
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# セキュリティ関連設定
# security.W004
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# security.W006
SECURE_CONTENT_TYPE_NOSNIFF = True
# security.W007
SECURE_BROWSER_XSS_FILTER = True
# security.W008
SECURE_SSL_REDIRECT = True
# security.W012
SESSION_COOKIE_SECURE = True
# security.W016
CSRF_COOKIE_SECURE = True
# security.W019
X_FRAME_OPTIONS = 'DENY'
# security.W021
SECURE_HSTS_PRELOAD = True

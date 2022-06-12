from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sms',
        'USER': 'sms_user',
        'PASSWORD': 'user',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# ロギング設定
LOGGING = {
    'version': 1,  # 1固定
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # アプリケーションが利用するロガー
        'home': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'student': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'registry': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'download': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'zenken': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'cron': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },

    # ハンドラの設定
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev'
        },
    },

    # フォーマッタの設定
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

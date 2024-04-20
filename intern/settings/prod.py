from .base import *

# 本番環境用の設定を記述
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 587  # 通常は587または465
# EMAIL_USE_TLS = True  # TLSを使用する場合
# EMAIL_USE_SSL = False  # SSLを使用する場合
# EMAIL_HOST_USER = 'hond'  # SMTPサーバーのユーザー名
# EMAIL_HOST_PASSWORD = 'hondhond'  # SMTPサーバーのパスワード

INSTALLED_APPS += ["django_ses"]

# 本番環境ではしっかりメールを送信
# Amazon SES関連設定
AWS_SES_ACCESS_KEY_ID = os.getenv('AWS_SES_ACCESS_KEY_ID')
AWS_SES_SECRET_ACCESS_KEY = os.getenv('AWS_SES_SECRET_ACCESS_KEY')
AWS_SES_REGION_NAME = 'ap-northeast-1'
AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'
EMAIL_BACKEND = 'django_ses.SESBackend'
ADMINS = [('hond', 'hty999a@gmail.com'),]




# 本番環境ではしっかりメールを送信
# Amazon SES関連設定
# AWS_SES_ACCESS_KEY_ID = os.getenv('AWS_SES_ACCESS_KEY_ID')
# AWS_SES_SECRET_ACCESS_KEY = os.getenv('AWS_SES_SECRET_ACCESS_KEY')
# AWS_SES_REGION_NAME = 'ap-northeast-1'
# AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'
# EMAIL_BACKEND = 'django_ses.SESBackend'
# INSTALLED_APPS += ['django_ses']


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
# 本番時のロギング設定
# LOGGING = {
#     'version': 1,  # 1固定
#     'disable_existing_loggers': False,

#     # ロガーの設定
#     'loggers': {
#         # Djangoが利用するロガー
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#         },
#         # myappアプリケーションが利用するロガー
#         'myapp': {
#             'handlers': ['file'],
#             'level': 'INFO',
#         },
#     },

#     # ハンドラの設定
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': os.path.join(BASE_DIR, 'logs/django.log'),
#             'formatter': 'prod',
#             'when': 'D',  # ログローテーション(新しいファイルへの切り替え)間隔の単位(D=日)
#             'interval': 1,  # ログローテーション間隔(1日単位)
#             'backupCount': 7,  # 保存しておくログファイル数
#         },
#     },

#     # フォーマッタの設定
#     'formatters': {
#         'prod': {
#             'format': '\t'.join([
#                 '%(asctime)s',
#                 '[%(levelname)s]',
#                 '%(pathname)s(Line:%(lineno)d)',
#                 '%(message)s'
#             ])
#         },
#     }
# }
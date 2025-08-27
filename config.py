import os

# 邮件配置
try:
    from mail_settings import CURRENT_MAIL_CONFIG
    MAIL_CONFIG = CURRENT_MAIL_CONFIG
except ImportError:
    # 如果导入失败，使用默认配置
    MAIL_CONFIG = {
        'MAIL_SERVER': 'smtp.gmail.com',
        'MAIL_PORT': 587,
        'MAIL_USE_TLS': True,
        'MAIL_USE_SSL': False,
        'MAIL_USERNAME': 'your-email@gmail.com',
        'MAIL_PASSWORD': 'your-app-password',
        'MAIL_DEFAULT_SENDER': 'your-email@gmail.com',
    }

# 支持的邮件服务器配置
SUPPORTED_MAIL_SERVERS = {
    'gmail': {
        'name': 'Gmail',
        'server': 'smtp.gmail.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
        'note': '需要开启应用专用密码'
    },
    'outlook': {
        'name': 'Outlook/Hotmail',
        'server': 'smtp-mail.outlook.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
        'note': '使用邮箱密码'
    },
    'qq': {
        'name': 'QQ邮箱',
        'server': 'smtp.qq.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
        'note': '需要开启SMTP服务并获取授权码'
    },
    '163': {
        'name': '163邮箱',
        'server': 'smtp.163.com',
        'port': 25,
        'use_tls': False,
        'use_ssl': False,
        'note': '需要开启SMTP服务并获取授权码'
    },
    'custom': {
        'name': '自定义SMTP服务器',
        'server': '',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
        'note': '请根据您的SMTP服务器配置'
    }
}


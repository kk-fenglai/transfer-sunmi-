# 邮件配置文件
# 支持多种邮箱配置

# Gmail配置
GMAIL_CONFIG = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USE_SSL': False,
    'MAIL_USERNAME': 'davin.lian@sunmi.tech',
    'MAIL_PASSWORD': 'adaw zktz lqgf wlqw',
    'MAIL_DEFAULT_SENDER': 'davin.lian@sunmi.tech',
}

# Outlook配置
OUTLOOK_CONFIG = {
    'MAIL_SERVER': 'smtp-mail.outlook.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USE_SSL': False,
    'MAIL_USERNAME': 'your-email@outlook.com',
    'MAIL_PASSWORD': 'your-outlook-password',
    'MAIL_DEFAULT_SENDER': 'your-email@outlook.com',
}

# QQ邮箱配置
QQ_CONFIG = {
    'MAIL_SERVER': 'smtp.qq.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USE_SSL': False,
    'MAIL_USERNAME': 'your-qq@qq.com',
    'MAIL_PASSWORD': 'your-qq-authorization-code',
    'MAIL_DEFAULT_SENDER': 'your-qq@qq.com',
}

# 163邮箱配置
MAIL_163_CONFIG = {
    'MAIL_SERVER': 'smtp.163.com',
    'MAIL_PORT': 465,
    'MAIL_USE_TLS': False,
    'MAIL_USE_SSL': True,
    'MAIL_USERNAME': 'your-email@163.com',
    'MAIL_PASSWORD': 'your-163-authorization-code',
    'MAIL_DEFAULT_SENDER': 'your-email@163.com',
}

# 自定义SMTP配置
CUSTOM_CONFIG = {
    'MAIL_SERVER': '',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USE_SSL': False,
    'MAIL_USERNAME': 'your-email@example.com',
    'MAIL_PASSWORD': 'your-password',
    'MAIL_DEFAULT_SENDER': 'your-email@example.com',
}

# 当前使用的配置 (通过 current_mail_config.py 动态选择)
try:
    from current_mail_config import CURRENT_PROVIDER
    if CURRENT_PROVIDER == 'gmail':
        CURRENT_MAIL_CONFIG = GMAIL_CONFIG
    elif CURRENT_PROVIDER == 'outlook':
        CURRENT_MAIL_CONFIG = OUTLOOK_CONFIG
    elif CURRENT_PROVIDER == 'qq':
        CURRENT_MAIL_CONFIG = QQ_CONFIG
    elif CURRENT_PROVIDER == '163':
        CURRENT_MAIL_CONFIG = MAIL_163_CONFIG
    elif CURRENT_PROVIDER == 'custom':
        CURRENT_MAIL_CONFIG = CUSTOM_CONFIG
    else:
        CURRENT_MAIL_CONFIG = GMAIL_CONFIG  # 默认使用Gmail
except ImportError:
    CURRENT_MAIL_CONFIG = GMAIL_CONFIG  # 如果导入失败，使用Gmail作为默认值

# 配置提供者映射
PROVIDER_CONFIGS = {
    'gmail': GMAIL_CONFIG,
    'outlook': OUTLOOK_CONFIG,
    'qq': QQ_CONFIG,
    '163': MAIL_163_CONFIG,
    'custom': CUSTOM_CONFIG
}

# 或者使用环境变量覆盖
import os
if os.environ.get('MAIL_USERNAME'):
    CURRENT_MAIL_CONFIG['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
if os.environ.get('MAIL_PASSWORD'):
    CURRENT_MAIL_CONFIG['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
if os.environ.get('MAIL_DEFAULT_SENDER'):
    CURRENT_MAIL_CONFIG['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

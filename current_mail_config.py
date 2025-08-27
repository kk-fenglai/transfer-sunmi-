# 当前使用的邮箱配置类型
# 这个文件用于存储当前激活的邮箱配置

CURRENT_PROVIDER = 'gmail'  # 可选值: gmail, outlook, qq, 163, custom

# 配置映射
PROVIDER_MAP = {
    'gmail': 'GMAIL_CONFIG',
    'outlook': 'OUTLOOK_CONFIG', 
    'qq': 'QQ_CONFIG',
    '163': 'MAIL_163_CONFIG',
    'custom': 'CUSTOM_CONFIG'
}

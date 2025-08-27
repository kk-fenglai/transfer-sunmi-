#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速配置邮件发送功能
支持多种邮箱配置
"""

import os
import sys

def setup_gmail():
    """配置Gmail邮箱"""
    print("📧 配置Gmail邮箱")
    print("=" * 50)
    
    email = input("请输入Gmail邮箱地址: ").strip()
    if not email or '@gmail.com' not in email:
        print("❌ 请输入有效的Gmail邮箱地址")
        return False
    
    password = input("请输入应用专用密码 (16位): ").strip()
    if len(password) != 16:
        print("❌ 应用专用密码必须是16位")
        return False
    
    # 更新配置文件
    update_mail_settings('gmail', email, password)
    print("✅ Gmail配置完成！")
    return True

def setup_outlook():
    """配置Outlook邮箱"""
    print("📧 配置Outlook邮箱")
    print("=" * 50)
    
    email = input("请输入Outlook邮箱地址: ").strip()
    if not email or '@outlook.com' not in email and '@hotmail.com' not in email:
        print("❌ 请输入有效的Outlook邮箱地址")
        return False
    
    password = input("请输入邮箱密码: ").strip()
    if not password:
        print("❌ 请输入密码")
        return False
    
    # 更新配置文件
    update_mail_settings('outlook', email, password)
    print("✅ Outlook配置完成！")
    return True

def setup_qq():
    """配置QQ邮箱"""
    print("📧 配置QQ邮箱")
    print("=" * 50)
    
    email = input("请输入QQ邮箱地址: ").strip()
    if not email or '@qq.com' not in email:
        print("❌ 请输入有效的QQ邮箱地址")
        return False
    
    password = input("请输入授权码 (16位): ").strip()
    if len(password) != 16:
        print("❌ 授权码必须是16位")
        return False
    
    # 更新配置文件
    update_mail_settings('qq', email, password)
    print("✅ QQ邮箱配置完成！")
    return True

def setup_163():
    """配置163邮箱"""
    print("📧 配置163邮箱")
    print("=" * 50)
    
    email = input("请输入163邮箱地址: ").strip()
    if not email or '@163.com' not in email:
        print("❌ 请输入有效的163邮箱地址")
        return False
    
    password = input("请输入授权码 (16位): ").strip()
    if len(password) != 16:
        print("❌ 授权码必须是16位")
        return False
    
    # 更新配置文件
    update_mail_settings('163', email, password)
    print("✅ 163邮箱配置完成！")
    return True

def setup_custom():
    """配置自定义SMTP服务器"""
    print("📧 配置自定义SMTP服务器")
    print("=" * 50)
    
    server = input("请输入SMTP服务器地址: ").strip()
    if not server:
        print("❌ 请输入SMTP服务器地址")
        return False
    
    port = input("请输入端口号 (默认587): ").strip()
    if not port:
        port = "587"
    
    email = input("请输入邮箱地址: ").strip()
    if not email or '@' not in email:
        print("❌ 请输入有效的邮箱地址")
        return False
    
    password = input("请输入密码/授权码: ").strip()
    if not password:
        print("❌ 请输入密码")
        return False
    
    use_tls = input("是否使用TLS加密? (y/n, 默认y): ").strip().lower()
    if use_tls not in ['n', 'no']:
        use_tls = True
    else:
        use_tls = False
    
    # 更新配置文件
    update_mail_settings('custom', email, password, server, port, use_tls)
    print("✅ 自定义SMTP配置完成！")
    return True

def update_mail_settings(provider, email, password, server=None, port=None, use_tls=None):
    """更新邮件配置文件"""
    config_file = 'mail_settings.py'
    
    # 读取现有配置
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        print(f"❌ 配置文件 {config_file} 不存在")
        return False
    
    # 根据提供商更新配置
    if provider == 'gmail':
        content = update_gmail_config(content, email, password)
    elif provider == 'outlook':
        content = update_outlook_config(content, email, password)
    elif provider == 'qq':
        content = update_qq_config(content, email, password)
    elif provider == '163':
        content = update_163_config(content, email, password)
    elif provider == 'custom':
        content = update_custom_config(content, email, password, server, port, use_tls)
    
    # 更新当前使用的配置
    content = update_current_config(content, provider)
    
    # 写入配置文件
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ 写入配置文件失败: {e}")
        return False

def update_gmail_config(content, email, password):
    """更新Gmail配置"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "'MAIL_USERNAME': 'your-gmail@gmail.com'" in line:
            lines[i] = f"    'MAIL_USERNAME': '{email}',"
        elif "'MAIL_PASSWORD': 'your-gmail-app-password'" in line:
            lines[i] = f"    'MAIL_PASSWORD': '{password}',"
        elif "'MAIL_DEFAULT_SENDER': 'your-gmail@gmail.com'" in line:
            lines[i] = f"    'MAIL_DEFAULT_SENDER': '{email}',"
    return '\n'.join(lines)

def update_outlook_config(content, email, password):
    """更新Outlook配置"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "'MAIL_USERNAME': 'your-email@outlook.com'" in line:
            lines[i] = f"    'MAIL_USERNAME': '{email}',"
        elif "'MAIL_PASSWORD': 'your-outlook-password'" in line:
            lines[i] = f"    'MAIL_PASSWORD': '{password}',"
        elif "'MAIL_DEFAULT_SENDER': 'your-email@outlook.com'" in line:
            lines[i] = f"    'MAIL_DEFAULT_SENDER': '{email}',"
    return '\n'.join(lines)

def update_qq_config(content, email, password):
    """更新QQ邮箱配置"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "'MAIL_USERNAME': 'your-qq@qq.com'" in line:
            lines[i] = f"    'MAIL_USERNAME': '{email}',"
        elif "'MAIL_PASSWORD': 'your-qq-authorization-code'" in line:
            lines[i] = f"    'MAIL_PASSWORD': '{password}',"
        elif "'MAIL_DEFAULT_SENDER': 'your-qq@qq.com'" in line:
            lines[i] = f"    'MAIL_DEFAULT_SENDER': '{email}',"
    return '\n'.join(lines)

def update_163_config(content, email, password):
    """更新163邮箱配置"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "'MAIL_USERNAME': 'your-email@163.com'" in line:
            lines[i] = f"    'MAIL_USERNAME': '{email}',"
        elif "'MAIL_PASSWORD': 'your-163-authorization-code'" in line:
            lines[i] = f"    'MAIL_PASSWORD': '{password}',"
        elif "'MAIL_DEFAULT_SENDER': 'your-email@163.com'" in line:
            lines[i] = f"    'MAIL_DEFAULT_SENDER': '{email}',"
    return '\n'.join(lines)

def update_custom_config(content, email, password, server, port, use_tls):
    """更新自定义SMTP配置"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "'MAIL_SERVER': ''" in line:
            lines[i] = f"    'MAIL_SERVER': '{server}',"
        elif "'MAIL_PORT': 587" in line:
            lines[i] = f"    'MAIL_PORT': {port},"
        elif "'MAIL_USERNAME': 'your-email@example.com'" in line:
            lines[i] = f"    'MAIL_USERNAME': '{email}',"
        elif "'MAIL_PASSWORD': 'your-password'" in line:
            lines[i] = f"    'MAIL_PASSWORD': '{password}',"
        elif "'MAIL_USE_TLS': True" in line:
            lines[i] = f"    'MAIL_USE_TLS': {use_tls},"
    return '\n'.join(lines)

def update_current_config(content, provider):
    """更新当前使用的配置"""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'CURRENT_MAIL_CONFIG = GMAIL_CONFIG' in line:
            if provider == 'gmail':
                lines[i] = 'CURRENT_MAIL_CONFIG = GMAIL_CONFIG'
            elif provider == 'outlook':
                lines[i] = 'CURRENT_MAIL_CONFIG = OUTLOOK_CONFIG'
            elif provider == 'qq':
                lines[i] = 'CURRENT_MAIL_CONFIG = QQ_CONFIG'
            elif provider == '163':
                lines[i] = 'CURRENT_MAIL_CONFIG = MAIL_163_CONFIG'
            elif provider == 'custom':
                lines[i] = 'CURRENT_MAIL_CONFIG = CUSTOM_CONFIG'
            break
    return '\n'.join(lines)

def main():
    """主函数"""
    print("🚀 邮件配置工具")
    print("=" * 50)
    print("支持以下邮箱类型：")
    print("1. Gmail")
    print("2. Outlook/Hotmail")
    print("3. QQ邮箱")
    print("4. 163邮箱")
    print("5. 自定义SMTP服务器")
    print("6. 退出")
    print("=" * 50)
    
    while True:
        try:
            choice = input("\n请选择邮箱类型 (1-6): ").strip()
            
            if choice == '1':
                setup_gmail()
            elif choice == '2':
                setup_outlook()
            elif choice == '3':
                setup_qq()
            elif choice == '4':
                setup_163()
            elif choice == '5':
                setup_custom()
            elif choice == '6':
                print("👋 再见！")
                break
            else:
                print("❌ 无效选择，请输入1-6")
                continue
            
            # 询问是否继续配置
            continue_setup = input("\n是否继续配置其他邮箱? (y/n): ").strip().lower()
            if continue_setup not in ['y', 'yes', '是']:
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 配置已取消")
            break
        except Exception as e:
            print(f"❌ 配置过程中出现错误: {e}")
            continue
    
    print("\n✅ 配置完成！现在可以启动应用测试邮件功能了。")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试邮件配置的脚本
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import MAIL_CONFIG

def test_mail_config():
    """测试邮件配置"""
    print("🧪 测试邮件配置...")
    
    # 获取当前邮件配置
    try:
        config = MAIL_CONFIG
        print(f"📧 邮件服务器: {config.get('MAIL_SERVER')}")
        print(f"🔌 端口: {config.get('MAIL_PORT')}")
        print(f"👤 用户名: {config.get('MAIL_USERNAME')}")
        print(f"🔒 TLS: {config.get('MAIL_USE_TLS')}")
        print(f"🔒 SSL: {config.get('MAIL_USE_SSL')}")
        print(f"📤 发件人: {config.get('MAIL_DEFAULT_SENDER')}")
        
        # 测试SMTP连接
        print(f"\n🔗 测试SMTP连接...")
        
        if config.get('MAIL_USE_SSL'):
            # 使用SSL连接
            print("使用SSL连接...")
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(config['MAIL_SERVER'], config['MAIL_PORT'], context=context) as server:
                print("✅ SSL连接成功!")
                
                # 尝试登录
                print("🔐 尝试登录...")
                try:
                    server.login(config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
                    print("✅ 登录成功!")
                except Exception as e:
                    print(f"❌ 登录失败: {e}")
                    return False
                    
        elif config.get('MAIL_USE_TLS'):
            # 使用TLS连接
            print("使用TLS连接...")
            with smtplib.SMTP(config['MAIL_SERVER'], config['MAIL_PORT']) as server:
                print("✅ 连接成功!")
                
                # 启动TLS
                server.starttls()
                print("✅ TLS启动成功!")
                
                # 尝试登录
                print("🔐 尝试登录...")
                try:
                    server.login(config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
                    print("✅ 登录成功!")
                except Exception as e:
                    print(f"❌ 登录失败: {e}")
                    return False
        else:
            # 普通连接
            print("使用普通连接...")
            with smtplib.SMTP(config['MAIL_SERVER'], config['MAIL_PORT']) as server:
                print("✅ 连接成功!")
                
                # 尝试登录
                print("🔐 尝试登录...")
                try:
                    server.login(config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
                    print("✅ 登录成功!")
                except Exception as e:
                    print(f"❌ 登录失败: {e}")
                    return False
        
        print("\n🎉 邮件配置测试成功!")
        return True
        
    except Exception as e:
        print(f"❌ 邮件配置测试失败: {e}")
        return False

def test_send_simple_email():
    """测试发送简单邮件"""
    print("\n🧪 测试发送简单邮件...")
    
    try:
        config = MAIL_CONFIG
        
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = config['MAIL_DEFAULT_SENDER']
        msg['To'] = 'test@example.com'  # 测试收件人
        msg['Subject'] = '测试邮件 - Sunmi系统'
        
        body = "这是一封测试邮件，用于验证邮件配置是否正确。"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 发送邮件
        if config.get('MAIL_USE_SSL'):
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(config['MAIL_SERVER'], config['MAIL_PORT'], context=context) as server:
                server.login(config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
                server.send_message(msg)
        elif config.get('MAIL_USE_TLS'):
            with smtplib.SMTP(config['MAIL_SERVER'], config['MAIL_PORT']) as server:
                server.starttls()
                server.login(config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
                server.send_message(msg)
        else:
            with smtplib.SMTP(config['MAIL_SERVER'], config['MAIL_PORT']) as server:
                server.login(config['MAIL_USERNAME'], config['MAIL_PASSWORD'])
                server.send_message(msg)
        
        print("✅ 测试邮件发送成功!")
        return True
        
    except Exception as e:
        print(f"❌ 测试邮件发送失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始测试邮件配置...")
    print("=" * 50)
    
    # 测试邮件配置
    config_ok = test_mail_config()
    
    if config_ok:
        print("\n💡 配置正确，可以尝试发送测试邮件")
        # 注意：这里不实际发送邮件，只是测试配置
        # test_send_simple_email()
    else:
        print("\n⚠️ 邮件配置有问题，请检查以下项目：")
        print("1. 邮件服务器地址和端口")
        print("2. 用户名和密码")
        print("3. SSL/TLS设置")
        print("4. 网络连接")
    
    print("\n" + "=" * 50)
    print("🏁 测试完成!")


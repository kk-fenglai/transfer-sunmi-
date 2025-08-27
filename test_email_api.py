#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试邮件发送API的脚本
"""

import requests
import json

def test_send_email():
    """测试发送邮件API"""
    print("🧪 测试邮件发送API...")
    
    # 测试数据
    test_data = {
        "recipient_email": "test@example.com",  # 请替换为真实的测试邮箱
        "subject": "测试邮件 - Sunmi系统",
        "message_type": "transfer_success",
        "custom_message": """设备转绑成功提醒：

转绑设备数量: 2 台
目标实体ID: TEST_ENTITY_123
转绑状态: 成功

设备序列号列表:
• P7B0000999976
• P7B0000999977

恭喜！您的设备转绑操作已成功完成。

如有疑问，请联系我们的技术支持团队。"""
    }
    
    try:
        print(f"📧 发送邮件到: {test_data['recipient_email']}")
        print(f"📝 邮件主题: {test_data['subject']}")
        print(f"📋 消息类型: {test_data['message_type']}")
        
        # 发送请求
        response = requests.post(
            'http://localhost:5000/api/send_email',
            headers={'Content-Type': 'application/json'},
            json=test_data,
            timeout=30
        )
        
        print(f"📡 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 邮件发送成功!")
                print(f"📨 响应消息: {result.get('message')}")
                print(f"👤 收件人: {result.get('recipient')}")
                print(f"📝 主题: {result.get('subject')}")
                print(f"🏷️ 消息类型: {result.get('message_type')}")
            else:
                print("❌ 邮件发送失败!")
                print(f"🚫 错误信息: {result.get('error')}")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"📄 响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误: 无法连接到Flask应用")
        print("💡 请确保Flask应用正在运行 (python app.py)")
    except requests.exceptions.Timeout:
        print("❌ 请求超时: 邮件发送操作超时")
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")

def test_send_test_email():
    """测试发送测试邮件API"""
    print("\n🧪 测试发送测试邮件API...")
    
    test_data = {
        "recipient_email": "test@example.com"  # 请替换为真实的测试邮箱
    }
    
    try:
        print(f"📧 发送测试邮件到: {test_data['recipient_email']}")
        
        response = requests.post(
            'http://localhost:5000/api/send_test_email',
            headers={'Content-Type': 'application/json'},
            json=test_data,
            timeout=30
        )
        
        print(f"📡 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 测试邮件发送成功!")
                print(f"📨 响应消息: {result.get('message')}")
                print(f"👤 收件人: {result.get('recipient')}")
            else:
                print("❌ 测试邮件发送失败!")
                print(f"🚫 错误信息: {result.get('error')}")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"📄 响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误: 无法连接到Flask应用")
    except requests.exceptions.Timeout:
        print("❌ 请求超时: 测试邮件发送操作超时")
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")

def test_get_mail_config():
    """测试获取邮件配置API"""
    print("\n🧪 测试获取邮件配置API...")
    
    try:
        response = requests.get(
            'http://localhost:5000/api/get_current_mail_config',
            timeout=10
        )
        
        print(f"📡 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ 邮件配置获取成功!")
                config = result.get('mail_config', {})
                print(f"📧 邮件服务器: {config.get('MAIL_SERVER')}")
                print(f"🔌 端口: {config.get('MAIL_PORT')}")
                print(f"👤 用户名: {config.get('MAIL_USERNAME')}")
                print(f"📤 发件人: {config.get('MAIL_DEFAULT_SENDER')}")
                print(f"🔒 TLS: {config.get('MAIL_USE_TLS')}")
                print(f"🔒 SSL: {config.get('MAIL_USE_SSL')}")
            else:
                print("❌ 邮件配置获取失败!")
                print(f"🚫 错误信息: {result.get('error')}")
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"📄 响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误: 无法连接到Flask应用")
    except requests.exceptions.Timeout:
        print("❌ 请求超时: 获取邮件配置操作超时")
    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")

if __name__ == "__main__":
    print("🚀 开始测试邮件发送功能...")
    print("=" * 50)
    
    # 测试获取邮件配置
    test_get_mail_config()
    
    # 测试发送测试邮件
    test_send_test_email()
    
    # 测试发送自定义邮件
    test_send_email()
    
    print("\n" + "=" * 50)
    print("🏁 测试完成!")
    print("\n💡 提示:")
    print("1. 请将测试邮箱地址替换为真实的邮箱地址")
    print("2. 确保Flask应用正在运行")
    print("3. 检查邮件配置是否正确")
    print("4. 查看Flask应用的控制台输出以获取详细信息")


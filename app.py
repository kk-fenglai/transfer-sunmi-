from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import requests
import time
import hmac
import hashlib
import json
import os
import re
import random
from dotenv import load_dotenv
from config import MAIL_CONFIG

# 加载环境变量
load_dotenv()

# 配置Flask应用
app = Flask(__name__)

# 从环境变量获取配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# 邮件配置
try:
    app.config.update(MAIL_CONFIG)
except ImportError:
    # 如果导入失败，使用环境变量配置
    app.config.update({
        'MAIL_SERVER': os.environ.get('MAIL_SERVER', 'smtp.gmail.com'),
        'MAIL_PORT': int(os.environ.get('MAIL_PORT', 587)),
        'MAIL_USE_TLS': os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true',
        'MAIL_USE_SSL': os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true',
        'MAIL_USERNAME': os.environ.get('MAIL_USERNAME', 'your-email@gmail.com'),
        'MAIL_PASSWORD': os.environ.get('MAIL_PASSWORD', 'your-app-password'),
        'MAIL_DEFAULT_SENDER': os.environ.get('MAIL_DEFAULT_SENDER', 'your-email@gmail.com'),
    })

# 初始化Flask-Mail
mail = Mail(app)

# 配置JSON处理
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# 添加CORS支持
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 确保Flask能正确处理JSON请求
@app.before_request
def before_request():
    if request.method == 'POST' and request.path.startswith('/api/'):
        if request.content_type and 'application/json' in request.content_type:
            try:
                # 尝试解析JSON数据
                if request.get_data():
                    request.get_json()
            except Exception as e:
                print(f"DEBUG - JSON parsing error: {e}")
                return jsonify({
                    'success': False,
                    'error': f'Invalid JSON data: {str(e)}'
                }), 400

# 添加健康检查端点
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Flask app is running'})


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/friend_list')
def friend_list():
    return render_template('friend_list.html')

@app.route('/friend_list_debug')
def friend_list_debug():
    return render_template('friend_list_debug.html')

@app.route('/test_simple')
def test_simple():
    return render_template('test_simple.html')

@app.route('/bind_sub_account')
def bind_sub_account_page():
    return render_template('bind_sub_account.html')



@app.route('/mail_config')
def mail_config():
    return render_template('mail_config.html')

@app.route('/unified_transfer')
def unified_transfer():
    return render_template('unified_transfer.html')

@app.route('/api/mail_config', methods=['GET'])
def get_mail_config():
    """Get current mail configuration"""
    try:
        from current_mail_config import CURRENT_PROVIDER
        from mail_settings import CURRENT_MAIL_CONFIG, PROVIDER_CONFIGS
        
        # 直接使用current_mail_config.py中指定的提供者
        current_provider = CURRENT_PROVIDER
        
        return jsonify({
            'success': True,
            'provider': current_provider,
            'email': CURRENT_MAIL_CONFIG.get('MAIL_USERNAME', 'Not configured'),
            'server': CURRENT_MAIL_CONFIG.get('MAIL_SERVER', 'Not configured')
        })
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'Mail configuration not found'
        }), 404

@app.route('/api/apply_mail_config', methods=['POST'])
def apply_mail_config():
    """Apply new mail configuration"""
    try:
        data = request.get_json()
        provider = data.get('provider', '')
        config = data.get('config', {})
        
        # 导入配置模块
        try:
            from mail_settings import PROVIDER_CONFIGS, CURRENT_MAIL_CONFIG
        except ImportError:
            return jsonify({
                'success': False,
                'error': 'Mail configuration module not found'
            }), 404
        
        # 根据提供者更新配置
        if provider == 'gmail':
            update_gmail_config(config)
        elif provider == 'outlook':
            update_outlook_config(config)
        elif provider == 'qq':
            update_qq_config(config)
        elif provider == '163':
            update_163_config(config)
        elif provider == 'custom':
            update_custom_config(config)
        else:
            return jsonify({
                'success': False,
                'error': f'Unknown provider: {provider}'
            }), 400
        
        # 更新当前提供者配置
        try:
            update_current_provider_config(provider)
        except Exception as e:
            print(f"Warning: Failed to update current provider config: {e}")
        
        return jsonify({
            'success': True,
            'message': f'{provider} configuration applied successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to apply configuration: {str(e)}'
        }), 500

@app.route('/api/switch_mail_config', methods=['POST'])
def switch_mail_config():
    """Switch to a different mail configuration"""
    try:
        data = request.get_json()
        provider = data.get('provider', '')
        
        # 导入配置模块
        try:
            from mail_settings import PROVIDER_CONFIGS, CURRENT_MAIL_CONFIG
        except ImportError:
            return jsonify({
                'success': False,
                'error': 'Mail configuration module not found'
            }), 404
        
        # 检查提供者是否存在
        if provider not in PROVIDER_CONFIGS:
            return jsonify({
                'success': False,
                'error': f'Unknown provider: {provider}'
            }), 400
        
        # 切换到指定配置
        try:
            # 更新配置文件
            update_current_provider_config(provider)
            
            return jsonify({
                'success': True,
                'message': f'Switched to {provider} configuration successfully'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to switch configuration: {str(e)}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to switch configuration: {str(e)}'
        }), 500

def update_gmail_config(config):
    """Update Gmail configuration"""
    try:
        from mail_settings import GMAIL_CONFIG
        GMAIL_CONFIG.update({
            'MAIL_USERNAME': config.get('email', ''),
            'MAIL_PASSWORD': config.get('password', ''),
            'MAIL_DEFAULT_SENDER': config.get('email', '')
        })
        
        # 重新加载配置模块以确保更改生效
        import importlib
        import mail_settings
        importlib.reload(mail_settings)
        
    except Exception as e:
        print(f"Failed to update Gmail config: {e}")

def update_outlook_config(config):
    """Update Outlook configuration"""
    try:
        from mail_settings import OUTLOOK_CONFIG
        OUTLOOK_CONFIG.update({
            'MAIL_USERNAME': config.get('email', ''),
            'MAIL_PASSWORD': config.get('password', ''),
            'MAIL_DEFAULT_SENDER': config.get('email', '')
        })
        
        # 重新加载配置模块以确保更改生效
        import importlib
        import mail_settings
        importlib.reload(mail_settings)
        
    except Exception as e:
        print(f"Failed to update Outlook config: {e}")

def update_qq_config(config):
    """Update QQ Mail configuration"""
    try:
        from mail_settings import QQ_CONFIG
        QQ_CONFIG.update({
            'MAIL_USERNAME': config.get('email', ''),
            'MAIL_PASSWORD': config.get('password', ''),
            'MAIL_DEFAULT_SENDER': config.get('email', '')
        })
        
        # 重新加载配置模块以确保更改生效
        import importlib
        import mail_settings
        importlib.reload(mail_settings)
        
    except Exception as e:
        print(f"Failed to update QQ config: {e}")

def update_163_config(config):
    """Update 163 Mail configuration"""
    try:
        from mail_settings import MAIL_163_CONFIG
        MAIL_163_CONFIG.update({
            'MAIL_USERNAME': config.get('email', ''),
            'MAIL_PASSWORD': config.get('password', ''),
            'MAIL_DEFAULT_SENDER': config.get('email', '')
        })
        
        # 重新加载配置模块以确保更改生效
        import importlib
        import mail_settings
        importlib.reload(mail_settings)
        
    except Exception as e:
        print(f"Failed to update 163 config: {e}")

def update_custom_config(config):
    """Update Custom SMTP configuration"""
    try:
        from mail_settings import CUSTOM_CONFIG
        CUSTOM_CONFIG.update({
            'MAIL_SERVER': config.get('server', ''),
            'MAIL_PORT': int(config.get('port', 587)),
            'MAIL_USERNAME': config.get('email', ''),
            'MAIL_PASSWORD': config.get('password', ''),
            'MAIL_DEFAULT_SENDER': config.get('email', ''),
            'MAIL_USE_TLS': config.get('tls', True)
        })
        
        # 重新加载配置模块以确保更改生效
        import importlib
        import mail_settings
        importlib.reload(mail_settings)
        
    except Exception as e:
        print(f"Failed to update custom config: {e}")

def update_current_provider_config(provider):
    """Update the current provider configuration file"""
    try:
        config_content = f"""# 当前使用的邮箱配置类型
# 这个文件用于存储当前激活的邮箱配置

CURRENT_PROVIDER = '{provider}'  # 可选值: gmail, outlook, qq, 163, custom

# 配置映射
PROVIDER_MAP = {{
    'gmail': 'GMAIL_CONFIG',
    'outlook': 'OUTLOOK_CONFIG', 
    'qq': 'QQ_CONFIG',
    '163': 'MAIL_163_CONFIG',
    'custom': 'CUSTOM_CONFIG'
}}
"""
        with open('current_mail_config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
    except Exception as e:
        print(f"Failed to update current provider config: {e}")
        raise e

@app.route('/api/test_mail_config', methods=['POST'])
def test_mail_config():
    """Test mail configuration"""
    try:
        data = request.get_json()
        provider = data.get('provider', '')
        
        # 获取指定提供者的配置
        try:
            from mail_settings import PROVIDER_CONFIGS
            from current_mail_config import CURRENT_PROVIDER
            
            # 如果请求的提供者与当前配置不同，使用请求的提供者配置
            if provider and provider in PROVIDER_CONFIGS:
                config = PROVIDER_CONFIGS[provider]
            else:
                # 否则使用当前配置
                from mail_settings import CURRENT_MAIL_CONFIG
                config = CURRENT_MAIL_CONFIG
                provider = CURRENT_PROVIDER
                
        except ImportError:
            return jsonify({
                'success': False,
                'error': 'Mail configuration not found'
            }), 404
        
        # 实际测试邮箱连接
        try:
            # 创建临时邮件配置
            temp_app = Flask(__name__)
            temp_app.config.update(config)
            temp_mail = Mail(temp_app)
            
            # 尝试发送测试邮件到自己的邮箱
            test_msg = Message(
                subject="Mail Configuration Test - Sunmi System",
                recipients=[config['MAIL_USERNAME']],  # 发送给自己
                body="This is a test email to verify your mail configuration is working correctly.",
                html="<h2>Mail Configuration Test</h2><p>Your mail configuration is working correctly!</p>"
            )
            
            with temp_app.app_context():
                temp_mail.send(test_msg)
            
            return jsonify({
                'success': True,
                'message': f'{provider} configuration test passed - Test email sent successfully to {config["MAIL_USERNAME"]}',
                'provider': provider,
                'email': config['MAIL_USERNAME'],
                'server': config['MAIL_SERVER']
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Mail connection failed: {str(e)}',
                'provider': provider,
                'email': config.get('MAIL_USERNAME', 'Unknown'),
                'server': config.get('MAIL_SERVER', 'Unknown')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Test failed: {str(e)}'
        }), 500



@app.route('/sub_account_list')
def sub_account_list():
    return render_template('sub_account_list.html')



@app.route('/api/validate_entity', methods=['POST'])
def validate_entity():
    """Validate target entity"""
    try:
        data = request.get_json()
        appid = data.get('appid', '')
        appkey = data.get('appkey', '')
        entity_id = data.get('entity_id', '')
        
        if not all([appid, appkey, entity_id]):
            return jsonify({
                'success': False,
                'error': 'Please provide App ID, App Key and target entity ID'
            }), 400
        
        # Prepare request parameters according to official documentation
        timestamp = str(int(time.time()))  # 10-digit timestamp
        nonce = str(random.randint(100000, 999999))  # 6-digit random number
        
        # Construct validation request body (using entity info API)
        payload = {
            "entity_id": entity_id
        }
        json_body = json.dumps(payload, separators=(',', ':'))
        
        # Generate HMAC signature according to official documentation:
        # Sunmi-Sign = hmacSHA256(request-json-body + appid + timestamp + nonce, appkey)
        sign_str = json_body + appid + timestamp + nonce
        sign = hmac.new(appkey.encode('utf-8'), sign_str.encode('utf-8'), hashlib.sha256).hexdigest()
        
        # Construct request headers
        headers = {
            "Content-Type": "application/json",
            "Sunmi-Appid": appid,
            "Sunmi-Nonce": nonce,
            "Sunmi-Timestamp": timestamp,
            "Sunmi-Sign": sign
        }
        
        # Send validation request (using entity info API)
        url = "https://openapi.sunmi.com/v2/mdm/open/open/entity/info"
        response = requests.post(url, headers=headers, data=json_body, timeout=30)
        
        return jsonify({
            'success': True,
            'status_code': response.status_code,
            'response': response.text,
            'entity_valid': response.status_code == 200
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Network request error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/get_friend_list', methods=['POST'])
def get_friend_list():
    """Get friend list from Sunmi API"""
    try:
        # 检查请求内容类型
        print(f"DEBUG - Request Content-Type: {request.content_type}")
        print(f"DEBUG - Request Headers: {dict(request.headers)}")
        print(f"DEBUG - Request Data: {request.get_data(as_text=True)}")
        
        if not request.is_json:
            print("DEBUG - Request is not JSON")
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        print(f"DEBUG - Parsed JSON data: {data}")
        
        if not data:
            print("DEBUG - No JSON data found")
            return jsonify({
                'success': False,
                'error': 'Invalid JSON data'
            }), 400
        
        appid = data.get('appid', '')
        appkey = data.get('appkey', '')
        
        print(f"DEBUG - App ID: {appid}")
        print(f"DEBUG - App Key: {'*' * len(appkey) if appkey else 'None'}")
        
        # Validate required parameters
        if not all([appid, appkey]):
            print("DEBUG - Missing App ID or App Key")
            return jsonify({
                'success': False,
                'error': 'Please provide App ID and App Key'
            }), 400
        
        # Prepare request parameters according to official documentation
        timestamp = str(int(time.time()))  # 10-digit timestamp
        nonce = str(random.randint(100000, 999999))  # 6-digit random number
        
        # Construct request body (empty for this API)
        payload = {}
        json_body = json.dumps(payload, separators=(',', ':'))
        
        # Generate HMAC signature according to official documentation:
        # Sunmi-Sign = hmacSHA256(request-json-body + appid + timestamp + nonce, appkey)
        sign_str = json_body + appid + timestamp + nonce
        signature = hmac.new(
            appkey.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Debug information
        print(f"DEBUG - Get Friend List - JSON Body: {json_body}")
        print(f"DEBUG - Get Friend List - AppID: {appid}")
        print(f"DEBUG - Get Friend List - Timestamp: {timestamp}")
        print(f"DEBUG - Get Friend List - Nonce: {nonce}")
        print(f"DEBUG - Get Friend List - Sign String: {sign_str}")
        print(f"DEBUG - Get Friend List - Generated Sign: {signature}")
        
        # Construct request headers
        headers = {
            "Content-Type": "application/json",
            "Sunmi-Appid": appid,
            "Sunmi-Nonce": nonce,
            "Sunmi-Timestamp": timestamp,
            "Sunmi-Sign": signature
        }
        
        # Send request
        url = "https://openapi.sunmi.com/v2/mdm/open/open/deviceCenter/partner/getFriendList"
        response = requests.post(url, headers=headers, data=json_body, timeout=30)
        
        # Parse response
        try:
            response_data = response.json()
            success = response_data.get('code') == 1
            
            # Parse error messages according to API documentation
            error_messages = {
                13010001: "Server error",
                13010002: "Parameter error",
                30001: "Cannot get ability - SUNMI Remote capability not enabled",
                40000: "Signature verification error",
                20000: "Missing request headers"
            }
            
            if not success:
                error_code = response_data.get('code')
                error_msg = error_messages.get(error_code, response_data.get('msg', 'Unknown error'))
                return jsonify({
                    'success': False,
                    'error': f'Error code {error_code}: {error_msg}',
                    'status_code': response.status_code,
                    'response': response.text
                })
            
            return jsonify({
                'success': True,
                'status_code': response.status_code,
                'response': response.text,
                'data': response_data
            })
            
        except json.JSONDecodeError:
            return jsonify({
                'success': True,
                'status_code': response.status_code,
                'response': response.text
            })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Network request error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/bind_sub_account', methods=['POST'])
def bind_sub_account():
    """Bind devices to sub account"""
    try:
        data = request.get_json()
        appid = data.get('appid', '')
        appkey = data.get('appkey', '')
        sn_list = data.get('sn_list', [])
        entity_id = data.get('entity_id', '')
        
        # Validate required parameters
        if not all([appid, appkey, sn_list, entity_id]):
            return jsonify({
                'success': False,
                'error': 'Please provide App ID, App Key, SN List and Entity ID'
            }), 400
        
        # Validate target entity ID format
        if not entity_id or len(entity_id.strip()) == 0:
            return jsonify({
                'success': False,
                'error': 'Entity ID cannot be empty'
            }), 400
        
        # Prepare request parameters according to official documentation
        timestamp = str(int(time.time()))  # 10-digit timestamp
        nonce = str(random.randint(100000, 999999))  # 6-digit random number
        
        # Construct request body
        payload = {
            "sn_list": sn_list,
            "entity_id": entity_id
        }
        json_body = json.dumps(payload, separators=(',', ':'))
        
        # Generate HMAC signature according to official documentation:
        # Sunmi-Sign = hmacSHA256(request-json-body + appid + timestamp + nonce, appkey)
        sign_str = json_body + appid + timestamp + nonce
        sign = hmac.new(appkey.encode('utf-8'), sign_str.encode('utf-8'), hashlib.sha256).hexdigest()
        
        # Debug information
        print(f"DEBUG - Bind Sub Account - JSON Body: {json_body}")
        print(f"DEBUG - Bind Sub Account - AppID: {appid}")
        print(f"DEBUG - Bind Sub Account - Timestamp: {timestamp}")
        print(f"DEBUG - Bind Sub Account - Nonce: {nonce}")
        print(f"DEBUG - Bind Sub Account - Sign String: {sign_str}")
        print(f"DEBUG - Bind Sub Account - Generated Sign: {sign}")
        
        # Construct request headers
        headers = {
            "Content-Type": "application/json",
            "Sunmi-Appid": appid,
            "Sunmi-Nonce": nonce,
            "Sunmi-Timestamp": timestamp,
            "Sunmi-Sign": sign
        }
        
        # Send request
        url = "https://openapi.sunmi.com/v2/mdm/open/open/deviceCenter/subAccount/device/bound"
        response = requests.post(url, headers=headers, data=json_body, timeout=30)
        
        # Parse response
        try:
            response_data = response.json()
            success = response_data.get('code') == 1
            
            # Parse error messages according to API documentation
            error_messages = {
                13010001: "Server error",
                13010002: "Parameter error",
                10105001: "Device not found",
                10105008: "Sub account not found",
                10105004: "Device freeze",
                10105006: "Device give num exceed 3000",
                30001: "Cannot get ability - SUNMI Remote capability not enabled",
                40000: "Signature verification error",
                20000: "Missing request headers"
            }
            
            if not success:
                error_code = response_data.get('code')
                error_msg = error_messages.get(error_code, response_data.get('msg', 'Unknown error'))
                return jsonify({
                    'success': False,
                    'error': f'Error code {error_code}: {error_msg}',
                    'status_code': response.status_code,
                    'response': response.text
                })
            
            return jsonify({
                'success': True,
                'status_code': response.status_code,
                'response': response.text,
                'data': response_data
            })
            
        except json.JSONDecodeError:
            return jsonify({
                'success': True,
                'status_code': response.status_code,
                'response': response.text
            })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Network request error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/send_email_notification', methods=['POST'])
def send_email_notification():
    """Send email notification without performing device transfer"""
    try:
        data = request.get_json()
        sn_list = data.get('sn_list', [])
        entity_id = data.get('entity_id', '')
        customer_email = data.get('customer_email', '')
        
        # Validate required parameters
        if not all([sn_list, customer_email]):
            return jsonify({
                'success': False,
                'error': 'Please provide SN List and Customer Email'
            }), 400
        
        # Validate SN list
        if not isinstance(sn_list, list) or len(sn_list) == 0:
            return jsonify({
                'success': False,
                'error': 'SN List must be a non-empty array'
            }), 400
        
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", customer_email):
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400
        
        # 只发送邮件，不执行转绑操作
        email_sent = False
        email_error = None
        
        try:
            # 发送邮件通知
            msg = Message(
                subject="Device Transfer Notification - Sunmi Device Transfer Notification",
                recipients=[customer_email],
                body=f"""
Hello!

This is a device transfer notification email.

Device Information:
- Device Count: {len(sn_list)} device(s)
- Target Entity ID: {entity_id}
- Send Time: {time.strftime('%Y-%m-%d %H:%M:%S')}

Device Serial Number List:
{chr(10).join(sn_list)}

Please Note: This email is for notification purposes only and does not involve actual device transfer operations.

If you have any questions, please contact our technical support team.

Best regards!
Sunmi Technical Support Team
                """,
                html=f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #2196f3; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9fa; padding: 20px; border-radius: 0 0 10px 10px; }}
        .info {{ color: #2196f3; font-weight: bold; }}
        .details {{ background: white; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #2196f3; }}
        .device-list {{ background: #f8f9fa; padding: 10px; border-radius: 5px; font-family: monospace; }}
        .note {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; color: #856404; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📧 Device Transfer Notification</h1>
        </div>
        <div class="content">
            <p>Hello!</p>
            <p>This is a device transfer notification email.</p>
            
            <div class="details">
                <h3>Device Information:</h3>
                <p><strong>Device Count:</strong> <span class="info">{len(sn_list)} device(s)</span></p>
                <p><strong>Target Entity ID:</strong> {entity_id}</p>
                <p><strong>Send Time:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="details">
                <h3>Device Serial Number List:</h3>
                <div class="device-list">
                    {chr(10).join(f'• {sn}' for sn in sn_list)}
                </div>
            </div>
            
            <div class="note">
                <h4>⚠️ Important Notice:</h4>
                <p>This email is for notification purposes only and does not involve actual device transfer operations.</p>
            </div>
            
            <p>If you have any questions, please contact our technical support team.</p>
            <p>Best regards!<br>Sunmi Technical Support Team</p>
        </div>
    </div>
</body>
</html>
                """
            )
            mail.send(msg)
            email_sent = True
        except Exception as e:
            email_error = str(e)
            print(f"Failed to send email: {e}")
        
        if email_sent:
            return jsonify({
                'success': True,
                'message': 'Email notification sent successfully',
                'email_sent': True,
                'email_to': customer_email,
                'devices_count': len(sn_list),
                'entity_id': entity_id
            })
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to send email: {email_error}',
                'email_sent': False,
                'email_error': email_error
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/transfer', methods=['POST'])
def transfer_devices():
    """Unified device transfer API - supports both friend transfer and sub account transfer"""
    try:
        data = request.get_json()
        appid = data.get('appid', '')
        appkey = data.get('appkey', '')
        sn_list = data.get('sn_list', [])
        entity_id = data.get('entity_id', '')
        customer_email = data.get('customer_email', '')  # Customer email for notifications
        transfer_type = data.get('transfer_type', 'friend')  # 'friend' or 'subaccount'
        
        # Validate required parameters
        if not all([appid, appkey, sn_list, entity_id]):
            return jsonify({
                'success': False,
                'error': 'Please provide App ID, App Key, SN List and Entity ID'
            }), 400
        
        # Validate SN list
        if not isinstance(sn_list, list) or len(sn_list) == 0:
            return jsonify({
                'success': False,
                'error': 'SN List must be a non-empty array'
            }), 400
        
        # Validate entity ID
        if not entity_id or len(entity_id.strip()) == 0:
            return jsonify({
                'success': False,
                'error': 'Entity ID cannot be empty'
            }), 400
        
        # Prepare request parameters according to official documentation
        timestamp = str(int(time.time()))  # 10-digit timestamp
        nonce = str(random.randint(100000, 999999))  # 6-digit random number
        
        # Construct request body
        payload = {
            "sn_list": sn_list,
            "entity_id": entity_id
        }
        json_body = json.dumps(payload, separators=(',', ':'))
        
        # Generate HMAC signature according to official documentation:
        # Sunmi-Sign = hmacSHA256(request-json-body + appid + timestamp + nonce, appkey)
        sign_str = json_body + appid + timestamp + nonce
        sign = hmac.new(appkey.encode('utf-8'), sign_str.encode('utf-8'), hashlib.sha256).hexdigest()
        
        # Debug information
        print(f"DEBUG - Device Transfer - JSON Body: {json_body}")
        print(f"DEBUG - Device Transfer - AppID: {appid}")
        print(f"DEBUG - Device Transfer - Timestamp: {timestamp}")
        print(f"DEBUG - Device Transfer - Nonce: {nonce}")
        print(f"DEBUG - Device Transfer - Sign String: {sign_str}")
        print(f"DEBUG - Device Transfer - Generated Sign: {sign}")
        
        # Construct request headers
        headers = {
            "Content-Type": "application/json",
            "Sunmi-Appid": appid,
            "Sunmi-Nonce": nonce,
            "Sunmi-Timestamp": timestamp,
            "Sunmi-Sign": sign
        }
        
        # Choose API endpoint based on transfer type
        if transfer_type == 'subaccount':
            url = "https://openapi.sunmi.com/v2/mdm/open/open/deviceCenter/subAccount/device/bound"
        else:  # friend transfer (default)
            url = "https://openapi.sunmi.com/v2/mdm/open/open/deviceCenter/device/transfer"
        
        # Send request
        response = requests.post(url, headers=headers, data=json_body, timeout=30)
        
        # Parse response
        try:
            response_data = response.json()
            success = response_data.get('code') == 1
            
            # Parse error messages according to API documentation
            error_messages = {
                13010001: "Server error",
                13010002: "Parameter error",
                10105001: "Device not found",
                10105002: "Friend not found",
                10105004: "Device freeze",
                10105006: "Device transfer count exceeds 3000",
                30001: "Cannot get ability - SUNMI Remote capability not enabled",
                40000: "Signature verification error",
                20000: "Missing request headers"
            }
            
            if not success:
                error_code = response_data.get('code')
                error_msg = error_messages.get(error_code, response_data.get('msg', 'Unknown error'))
                return jsonify({
                    'success': False,
                    'error': f'Error code {error_code}: {error_msg}',
                    'status_code': response.status_code,
                    'response': response.text
                })
            
            # If transfer is successful, try to send email notification
            email_sent = False
            email_error = None
            
            # Get customer email from request
            if customer_email:
                try:
                    # Send transfer success email
                    msg = Message(
                        subject="Device Transfer Success Notification - Sunmi Device Transfer Success",
                        recipients=[customer_email],
                        body=f"""
Hello!

Your device transfer operation has been completed successfully.

Transfer Details:
- Transfer Device Count: {len(sn_list)} device(s)
- Target Entity ID: {entity_id}
- Transfer Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
- Transfer Status: Success

Device Serial Number List:
{chr(10).join(sn_list)}

If you have any questions, please contact our technical support team.

Best regards!
Sunmi Technical Support Team
                        """,
                        html=f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #667eea; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9fa; padding: 20px; border-radius: 0 0 10px 10px; }}
        .success {{ color: #28a745; font-weight: bold; }}
        .details {{ background: white; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #667eea; }}
        .device-list {{ background: #f8f9fa; padding: 10px; border-radius: 5px; font-family: monospace; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Device Transfer Success Notification</h1>
        </div>
        <div class="content">
            <p>Hello!</p>
            <p>Your device transfer operation has been completed successfully.</p>
            
            <div class="details">
                <h3>Transfer Details:</h3>
                <p><strong>Transfer Device Count:</strong> <span class="success">{len(sn_list)} device(s)</span></p>
                <p><strong>Target Entity ID:</strong> {entity_id}</p>
                <p><strong>Transfer Time:</strong> {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Transfer Status:</strong> <span class="success">Success</span></p>
            </div>
            
            <div class="details">
                <h3>Device Serial Number List:</h3>
                <div class="device-list">
                    {chr(10).join(f'• {sn}' for sn in sn_list)}
                </div>
            </div>
            
            <p>If you have any questions, please contact our technical support team.</p>
            <p>Best regards!<br>Sunmi Technical Support Team</p>
        </div>
    </div>
</body>
</html>
                        """
                    )
                    mail.send(msg)
                    email_sent = True
                except Exception as e:
                    email_error = str(e)
                    print(f"Failed to send email: {e}")
            
            return jsonify({
                'success': True,
                'status_code': response.status_code,
                'response': response.text,
                'data': response_data,
                'email_sent': email_sent,
                'email_error': email_error,
                'transfer_type': transfer_type
            })
            
        except json.JSONDecodeError:
            return jsonify({
                'success': True,
                'status_code': response.status_code,
                'response': response.text
            })
        
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Network request error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/get_sub_account_list', methods=['POST'])
def get_sub_account_list():
    """Get Sub Account list API endpoint"""
    try:
        # Get data from both form and JSON (support both methods)
        app_id = None
        app_key = None
        
        if request.is_json:
            # Try to get from JSON first
            data = request.get_json()
            app_id = data.get('app_id') if data else None
            app_key = data.get('app_key') if data else None
        
        # Fallback to form data if JSON data not available
        if not app_id:
            app_id = request.form.get('app_id')
        if not app_key:
            app_key = request.form.get('app_key')
        
        # Validate required fields
        if not app_id or not app_key:
            return jsonify({
                'success': False,
                'error': 'App ID and App Key are required'
            }), 400
        
        # Generate signature parameters according to official documentation
        timestamp = str(int(time.time()))
        nonce = str(random.randint(100000, 999999))
        
        # Create payload (empty for this API)
        payload = {}
        json_body = json.dumps(payload, separators=(',', ':'))
        
        # Generate signature according to official documentation:
        # Sunmi-Sign = hmacSHA256(request-json-body + appid + timestamp + nonce, appkey)
        sign_str = json_body + app_id + timestamp + nonce
        signature = hmac.new(
            app_key.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Debug prints
        print(f"DEBUG - Get Sub Account List - Request Content-Type: {request.content_type}")
        print(f"DEBUG - Get Sub Account List - Request Headers: {dict(request.headers)}")
        print(f"DEBUG - Get Sub Account List - JSON Body: {json_body}")
        print(f"DEBUG - Get Sub Account List - AppID: {app_id}")
        print(f"DEBUG - Get Sub Account List - Timestamp: {timestamp}")
        print(f"DEBUG - Get Sub Account List - Nonce: {nonce}")
        print(f"DEBUG - Get Sub Account List - Sign String: {sign_str}")
        print(f"DEBUG - Get Sub Account List - Generated Sign: {signature}")
        
        # Prepare headers
        headers = {
            'Content-Type': 'application/json',
            'Sunmi-Appid': app_id,
            'Sunmi-Nonce': nonce,
            'Sunmi-Timestamp': timestamp,
            'Sunmi-Sign': signature
        }
        
        # Make API request
        url = 'https://openapi.sunmi.com/v2/mdm/open/open/deviceCenter/partner/getSubAccountList'
        print(f"DEBUG - Making request to: {url}")
        print(f"DEBUG - Request headers: {headers}")
        response = requests.post(url, headers=headers, data=json_body, timeout=30)
        
        print(f"DEBUG - Response status code: {response.status_code}")
        print(f"DEBUG - Response headers: {dict(response.headers)}")
        print(f"DEBUG - Response text: {response.text}")
        
        # Parse response
        try:
            response_data = response.json()
            print(f"DEBUG - Parsed response data: {response_data}")
        except json.JSONDecodeError as e:
            print(f"DEBUG - Failed to parse JSON response: {e}")
            return jsonify({
                'success': False,
                'error': f'Invalid JSON response from Sunmi API: {response.text}',
                'status_code': response.status_code,
                'raw_response': response.text
            }), 500
        
        if response.status_code == 200:
            if response_data.get('code') == 1:
                # Success
                sub_accounts = response_data.get('data', {}).get('sub_entity_list', [])
                return jsonify({
                    'success': True,
                    'status_code': response.status_code,
                    'response_code': response_data.get('code'),
                    'response_message': response_data.get('msg'),
                    'sub_accounts_count': len(sub_accounts),
                    'sub_accounts': sub_accounts,
                    'full_response': response_data
                })
            else:
                # API error - parse error messages according to API documentation
                error_code = response_data.get('code')
                error_messages = {
                    13010001: "Server error",
                    13010002: "Parameter error",
                    30001: "Cannot get ability - SUNMI Remote capability not enabled",
                    40000: "Signature verification error",
                    20000: "Missing request headers"
                }
                error_msg = error_messages.get(error_code, response_data.get('msg', 'Unknown error'))
                
                return jsonify({
                    'success': False,
                    'status_code': response.status_code,
                    'error_code': error_code,
                    'error_message': error_msg,
                    'full_response': response_data
                })
        else:
            # HTTP error
            return jsonify({
                'success': False,
                'status_code': response.status_code,
                'error': f'HTTP Error: {response.status_code}',
                'full_response': response_data
            })
            
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'error': 'Request timeout - please try again'
        }), 408
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Network error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }), 500

@app.route('/api/send_email', methods=['POST'])
def send_email():
    """Send email notification API endpoint"""
    try:
        data = request.get_json()
        
        # 获取邮件参数
        recipient_email = data.get('recipient_email', '')
        subject = data.get('subject', 'Sunmi System Notification')
        message_type = data.get('message_type', 'general')  # general, transfer_success, transfer_notification
        custom_message = data.get('custom_message', '')
        
        # 验证必要参数
        if not recipient_email:
            return jsonify({
                'success': False,
                'error': 'Recipient email is required'
            }), 400
        
        # 根据消息类型生成邮件内容
        if message_type == 'transfer_success':
            # Transfer success notification
            body = f"""
Hello!

Your device transfer operation has been completed successfully.

{custom_message}

If you have any questions, please contact our technical support team.

Best regards!
Sunmi Technical Support Team
            """
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #28a745; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9fa; padding: 20px; border-radius: 0 0 10px 10px; }}
        .success {{ color: #28a745; font-weight: bold; }}
        .details {{ background: white; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #28a745; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Device Transfer Success</h1>
        </div>
        <div class="content">
            <p>Hello!</p>
            <p>Your device transfer operation has been completed successfully.</p>
            
            <div class="details">
                {custom_message.replace(chr(10), '<br>')}
            </div>
            
            <p>If you have any questions, please contact our technical support team.</p>
            <p>Best regards!<br>Sunmi Technical Support Team</p>
        </div>
    </div>
</body>
</html>
            """
            
        elif message_type == 'transfer_notification':
            # Transfer notification
            body = f"""
Hello!

This is a device transfer notification email.

{custom_message}

Please Note: This email is for notification purposes only and does not involve actual device transfer operations.

Best regards!
Sunmi Technical Support Team
            """
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #17a2b8; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9fa; padding: 20px; border-radius: 0 0 10px 10px; }}
        .info {{ color: #17a2b8; font-weight: bold; }}
        .details {{ background: white; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #17a2b8; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📧 Device Transfer Notification</h1>
        </div>
        <div class="content">
            <p>Hello!</p>
            <p>This is a device transfer notification email.</p>
            
            <div class="details">
                {custom_message.replace(chr(10), '<br>')}
            </div>
            
            <p>Please Note: This email is for notification purposes only and does not involve actual device transfer operations.</p>
            <p>Best regards!<br>Sunmi Technical Support Team</p>
        </div>
    </div>
</body>
</html>
            """
            
        else:
            # 通用消息
            body = f"""
Hello!

{custom_message}

Best regards!
Sunmi Technical Support Team
            """
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #667eea; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9fa; padding: 20px; border-radius: 0 0 10px 10px; }}
        .details {{ background: white; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #667eea; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📧 Sunmi System Notification</h1>
        </div>
        <div class="content">
            <p>Hello!</p>
            
            <div class="details">
                {custom_message.replace(chr(10), '<br>')}
            </div>
            
            <p>Best regards!<br>Sunmi Technical Support Team</p>
        </div>
    </div>
</body>
</html>
            """
        
        # 发送邮件
        try:
            # 打印调试信息
            print(f"DEBUG - Attempting to send email:")
            print(f"  Server: {app.config.get('MAIL_SERVER')}")
            print(f"  Port: {app.config.get('MAIL_PORT')}")
            print(f"  Username: {app.config.get('MAIL_USERNAME')}")
            print(f"  Use TLS: {app.config.get('MAIL_USE_TLS')}")
            print(f"  Use SSL: {app.config.get('MAIL_USE_SSL')}")
            print(f"  Recipient: {recipient_email}")
            print(f"  Subject: {subject}")
            
            msg = Message(
                subject=subject,
                recipients=[recipient_email],
                body=body,
                html=html
            )
            
            # 尝试发送邮件
            mail.send(msg)
            print(f"DEBUG - Email sent successfully to {recipient_email}")
            
            return jsonify({
                'success': True,
                'message': 'Email sent successfully',
                'recipient': recipient_email,
                'subject': subject,
                'message_type': message_type
            })
            
        except Exception as e:
            error_msg = str(e)
            print(f"DEBUG - Failed to send email: {error_msg}")
            print(f"DEBUG - Error type: {type(e).__name__}")
            
            # 提供更详细的错误信息
            if "authentication" in error_msg.lower():
                error_detail = "Authentication failed. Please check email username and password."
            elif "connection" in error_msg.lower():
                error_detail = "Connection failed. Please check SMTP server and port settings."
            elif "ssl" in error_msg.lower():
                error_detail = "SSL/TLS error. Please check SSL/TLS configuration."
            elif "timeout" in error_msg.lower():
                error_detail = "Connection timeout. Please check network connection."
            else:
                error_detail = f"Email sending failed: {error_msg}"
            
            return jsonify({
                'success': False,
                'error': error_detail,
                'debug_info': error_msg
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/send_test_email', methods=['POST'])
def send_test_email():
    """Send test email to verify mail configuration"""
    try:
        data = request.get_json()
        recipient_email = data.get('recipient_email', '')
        
        if not recipient_email:
            return jsonify({
                'success': False,
                'error': 'Recipient email is required'
            }), 400
        
        # 发送测试邮件
        try:
            msg = Message(
                subject="Test Email - Sunmi System",
                recipients=[recipient_email],
                body="""
Hello!

This is a test email from Sunmi System to verify that the mail configuration is working correctly.

If you receive this email, it means:
1. The mail server configuration is correct
2. Authentication is successful
3. The system can send emails

Best regards!
Sunmi Technical Support Team
                """,
                html="""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #28a745; color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9fa; padding: 20px; border-radius: 0 0 10px 10px; }
        .success { color: #28a745; font-weight: bold; }
        .details { background: white; padding: 15px; margin: 15px 0; border-radius: 5px; border-left: 4px solid #28a745; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Test Email Success</h1>
        </div>
        <div class="content">
            <p>Hello!</p>
            <p>This is a test email from Sunmi System to verify that the mail configuration is working correctly.</p>
            
            <div class="details">
                <h3>What this means:</h3>
                <ul>
                    <li>The mail server configuration is correct</li>
                    <li>Authentication is successful</li>
                    <li>The system can send emails</li>
                </ul>
            </div>
            
            <p>Best regards!<br>Sunmi Technical Support Team</p>
        </div>
    </div>
</body>
</html>
                """
            )
            mail.send(msg)
            
            return jsonify({
                'success': True,
                'message': 'Test email sent successfully',
                'recipient': recipient_email
            })
            
        except Exception as e:
            print(f"Failed to send test email: {e}")
            return jsonify({
                'success': False,
                'error': f'Failed to send test email: {str(e)}'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/get_current_mail_config', methods=['GET'])
def get_current_mail_config():
    """Get current mail configuration for display"""
    try:
        from current_mail_config import CURRENT_PROVIDER
        from mail_settings import CURRENT_MAIL_CONFIG
        
        return jsonify({
            'success': True,
            'provider': CURRENT_PROVIDER,
            'mail_config': {
                'MAIL_SERVER': CURRENT_MAIL_CONFIG.get('MAIL_SERVER', 'Not configured'),
                'MAIL_PORT': CURRENT_MAIL_CONFIG.get('MAIL_PORT', 'Not configured'),
                'MAIL_USERNAME': CURRENT_MAIL_CONFIG.get('MAIL_USERNAME', 'Not configured'),
                'MAIL_DEFAULT_SENDER': CURRENT_MAIL_CONFIG.get('MAIL_DEFAULT_SENDER', 'Not configured'),
                'MAIL_USE_TLS': CURRENT_MAIL_CONFIG.get('MAIL_USE_TLS', False),
                'MAIL_USE_SSL': CURRENT_MAIL_CONFIG.get('MAIL_USE_SSL', False)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get mail config: {str(e)}'
        }), 500

@app.route('/api/reset_mail_config', methods=['POST'])
def reset_mail_config():
    """Reset mail configuration to default Gmail settings"""
    try:
        # 重置为Gmail配置
        update_current_provider_config('gmail')
        
        # 重新加载配置模块
        import importlib
        import mail_settings
        importlib.reload(mail_settings)
        
        return jsonify({
            'success': True,
            'message': 'Mail configuration reset to Gmail successfully',
            'provider': 'gmail'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to reset mail config: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 
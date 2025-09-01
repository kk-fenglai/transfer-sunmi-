# 📧 邮件配置指南

## 🔍 当前问题分析

邮件发送失败的原因是：**认证失败 (authentication failed)**

## 🛠️ 解决方案

### 1. 配置163邮箱

要使用163邮箱发送邮件，你需要：

1. **开启SMTP服务**：
   - 登录163邮箱网页版
   - 进入"设置" → "POP3/SMTP/IMAP"
   - 开启"SMTP服务"

2. **获取授权码**：
   - 在SMTP设置中获取"授权码"
   - 这不是你的邮箱密码，而是专门的SMTP授权码

3. **更新配置文件**：
   编辑 `mail_settings.py` 文件中的 `MAIL_163_CONFIG`：

```python
MAIL_163_CONFIG = {
    'MAIL_SERVER': 'smtp.163.com',
    'MAIL_PORT': 465,
    'MAIL_USE_TLS': False,
    'MAIL_USE_SSL': True,
    'MAIL_USERNAME': 'your-actual-email@163.com',  # 替换为你的真实163邮箱
    'MAIL_PASSWORD': 'your-actual-authorization-code',  # 替换为你的授权码
    'MAIL_DEFAULT_SENDER': 'your-actual-email@163.com',  # 替换为你的真实163邮箱
}
```

### 2. 或者使用Gmail配置

如果你想使用Gmail（当前配置）：

1. **开启两步验证**
2. **生成应用专用密码**
3. **更新Gmail配置**：

```python
GMAIL_CONFIG = {
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USE_SSL': False,
    'MAIL_USERNAME': 'your-gmail@gmail.com',  # 替换为你的Gmail
    'MAIL_PASSWORD': 'your-app-password',  # 替换为应用专用密码
    'MAIL_DEFAULT_SENDER': 'your-gmail@gmail.com',  # 替换为你的Gmail
}
```

### 3. 测试配置

配置完成后，运行测试脚本：

```bash
python test_mail_config.py
```

### 4. 重启Flask应用

配置更改后，需要重启Flask应用：

```bash
# 停止当前应用
# 然后重新启动
python app.py
```

## 📋 常见问题

### Q: 为什么认证失败？
A: 可能的原因：
- 用户名不正确
- 密码/授权码不正确
- 没有开启SMTP服务
- 使用了邮箱密码而不是授权码

### Q: 163邮箱的端口设置？
A: 
- 端口25：普通连接（可能被防火墙阻止）
- 端口465：SSL连接（推荐）
- 端口587：TLS连接

### Q: 如何获取163邮箱授权码？
A: 
1. 登录163邮箱
2. 设置 → POP3/SMTP/IMAP
3. 开启SMTP服务
4. 获取授权码

## 🎯 推荐配置

对于163邮箱，推荐使用：
- 服务器：`smtp.163.com`
- 端口：`465`
- SSL：`True`
- TLS：`False`

## 📞 技术支持

如果仍有问题，请检查：
1. 网络连接
2. 防火墙设置
3. 邮箱服务商的状态
4. Flask应用的日志输出


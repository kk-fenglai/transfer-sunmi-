# 📧 邮箱发送通知功能说明

## 功能概述

邮件功能和Device Transfer功能现在是两个独立的按钮，用户可以选择：
1. 只执行设备转绑操作
2. 只发送邮件通知（不执行转绑）
3. 或者两者都执行（分别点击两个按钮）

## 🆕 新增功能

### 1. 独立的邮件功能
- 独立的"📧 Send Email Only"按钮
- 只发送邮件，不执行设备转绑
- 使用专门的 `/api/send_email_notification` 端点

### 2. 独立的转绑功能
- 独立的"🎁 Transfer Devices"按钮
- 只执行设备转绑，不发送邮件
- 使用现有的 `/api/transfer` 端点

## 🎯 使用场景

1. **通知客户转绑状态**：向客户发送设备转绑通知
2. **批量邮件发送**：一次性通知多个设备的状态
3. **邮件模板测试**：测试邮件格式和内容
4. **客户沟通**：与客户沟通设备相关信息

## 🔧 技术实现

### 后端API
```python
@app.route('/api/send_email_notification', methods=['POST'])
def send_email_notification():
    """Send email notification without performing device transfer"""
```

### 前端界面
- 独立的表单区域
- 实时验证和错误提示
- 加载状态显示
- 成功/失败结果展示

## 📋 输入字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| App ID | 文本 | ✅ | Sunmi应用ID |
| App Key | 密码 | ✅ | Sunmi应用密钥 |
| Entity ID | 文本 | ✅ | 目标实体ID |
| Device SN List | 文本域 | ✅ | 设备序列号列表 |
| Customer Email | 邮箱 | ❌ | 客户邮箱地址（可选） |

## 📧 邮件内容

### 邮件主题
`设备转绑成功通知 - Sunmi Device Transfer Success`

### 邮件内容包含
- 设备数量
- 目标实体ID
- 转绑时间
- 设备序列号列表
- 转绑成功状态

### 邮件格式
- 纯文本版本
- HTML版本（带样式）

## 🚀 使用方法

### 1. 访问Friend List页面
```
http://localhost:5000/friend_list
```

### 2. 找到Device Transfer区域
在页面中部的绿色背景区域

### 3. 填写表单
- 输入App ID和App Key
- 输入Entity ID
- 输入设备SN列表（换行或逗号分隔）
- **可选：** 输入客户邮箱地址

### 4. 选择操作
- **转绑设备**: 点击"🎁 Transfer Devices"按钮
- **发送邮件**: 点击"📧 Send Email Only"按钮
- **两者都执行**: 分别点击两个按钮

### 5. 查看结果
- 转绑结果：显示设备转绑成功或失败信息
- 邮件结果：显示邮件发送成功或失败状态

## 🧪 测试功能

### 运行测试脚本
```bash
python test_email_notification.py
```

### 测试要点
- API连接性
- 参数验证
- 邮件发送
- 错误处理

## ⚠️ 注意事项

1. **邮件配置**：确保在`config.py`中正确配置邮件服务器
2. **环境变量**：可以设置环境变量来配置邮件参数
3. **邮件限制**：注意邮件服务器的发送限制
4. **集成功能**：邮件功能已完全整合到Device Transfer功能中
5. **可选功能**：客户邮箱字段为可选，不填写则不发送邮件

## 🔍 错误处理

### 常见错误
- `Invalid email format`：邮箱格式错误
- `SN List must be a non-empty array`：设备列表为空
- `Missing required fields`：缺少必填字段

### 解决方案
- 检查邮箱格式（user@example.com）
- 确保输入至少一个设备SN
- 填写所有必填字段

## 📁 相关文件

- `app.py`：主应用文件，包含API端点
- `templates/friend_list.html`：前端界面
- `config.py`：邮件配置
- `test_email_notification.py`：测试脚本

## 🎨 界面特色

- **双按钮设计**：独立的转绑和邮件发送按钮
- **响应式设计**：适配不同屏幕尺寸
- **实时反馈**：加载状态和结果展示
- **错误提示**：详细的错误信息和解决方案
- **灵活操作**：用户可以选择执行转绑、发送邮件或两者都执行

## 🔮 未来扩展

1. **邮件模板管理**：支持自定义邮件模板
2. **批量邮件**：支持多个收件人
3. **邮件历史**：记录发送历史
4. **定时发送**：支持定时发送功能
5. **邮件状态跟踪**：跟踪邮件发送状态

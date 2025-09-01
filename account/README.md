# Sunmi API 管理工具

这是一个基于Web的Sunmi API管理工具，提供了友好的用户界面来执行各种API操作。

## 功能特性

- 🎨 现代化的Web界面
- 🔐 安全的API调用（HMAC-SHA256签名）
- 📱 响应式设计，支持移动设备
- ⚡ 实时请求状态反馈
- 🛡️ 输入验证和错误处理
- 📋 完整的API文档集成
- 🔍 实体验证功能
- ⚠️ 详细的错误代码解析
- 🔐 全面的签名验证工具
- 📊 详细的签名分析报告
- 📧 自动邮件通知功能（设备转绑成功）
- 🔧 **最新修复**: 设备转移API端点已更新为官方标准

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问：http://localhost:5000

## 使用说明

### 获取API凭据

1. 访问 [商米合作伙伴平台](https://partner.sunmi.com/ability/application)
2. 创建云应用
3. 添加所需能力："Sunmi DataCube"
4. 获取App ID和App Key

### 主要功能

#### 1. 好友列表管理
- 获取当前用户的好友列表
- 查看合作伙伴信息
- 支持SUNMI Remote功能

#### 2. 子账户设备绑定
- 将设备绑定到子账户
- 支持批量绑定操作
- 自动子账户权限验证

#### 3. 实体验证
- 验证目标实体是否存在且有效
- 确认目标实体具有相应权限

#### 4. 邮件通知系统
- 设备转绑成功后自动发送邮件通知
- 支持多种邮件服务提供商（Gmail、Outlook、QQ邮箱等）
- 美观的HTML邮件模板
- 完整的邮件发送状态反馈
- **新增：双按钮设计**，邮件功能和Device Transfer功能现在是两个独立按钮，用户可以选择执行转绑、发送邮件或两者都执行

## 文件结构

```
account/
├── app.py                 # Flask后端应用
├── config.py             # 邮件配置文件
├── templates/
│   ├── index.html        # 主页面
│   ├── friend_list.html  # 好友列表页面
│   ├── bind_sub_account.html  # 绑定子账户页面
│   ├── sub_account_list.html  # 子账户列表页面

│   ├── mail_config.html  # 邮件配置页面
│   └── test_simple.html  # 简单测试页面
├── requirements.txt      # Python依赖
├── README.md            # 项目说明
├── README_EMAIL_FEATURE.md  # 邮件功能使用说明
├── README_EMAIL_NOTIFICATION.md  # 邮箱发送通知功能说明
├── CHANGELOG_INTEGRATED_EMAIL.md  # 邮件功能整合变更日志
├── CHANGELOG_DUAL_BUTTONS.md  # 双按钮设计变更日志
├── test_friend_list.py  # 好友列表测试脚本
├── test_friend_list_simple.py  # 简化版测试脚本
├── test_web_api_simple.py  # Web API测试脚本
├── test_simple_email.py    # 简化邮件发送测试脚本
└── test_email_notification.py  # 完整邮件发送测试脚本
```

## 安全说明

- App Key在传输过程中会被隐藏显示
- 所有API调用都使用HMAC-SHA256签名验证
- 请求包含时间戳和随机数防止重放攻击
- 前端不存储任何敏感信息

## API 规范

### 基本信息
- **基础URL**: `https://openapi.sunmi.com/v2/mdm/open/open/`
- **认证方式**: HMAC-SHA256签名
- **请求格式**: JSON

### 主要API端点

#### 好友列表
- **URL**: `deviceCenter/partner/getFriendList`
- **方法**: POST
- **功能**: 获取当前用户的好友列表

#### 子账户绑定
- **URL**: `deviceCenter/subAccount/device/bound`
- **方法**: POST
- **功能**: 将设备绑定到子账户

#### 设备转移到好友
- **URL**: `deviceCenter/bind/transfer`
- **方法**: POST
- **功能**: 将设备转移到好友账户

#### 实体验证
- **URL**: `entity/info`
- **方法**: POST
- **功能**: 验证目标实体是否存在且有效

## 更新日志

### 最新修复 (2024)

#### API端点修复
- ✅ **修复设备转移API端点**: 从 `deviceCenter/device/transfer` 更新为 `deviceCenter/bind/transfer`
- ✅ **UI界面修复**: 更新了所有模板文件中的API端点显示
- ✅ **导航链接修复**: 移除了无效的 `/sign_test` 链接，更新为正确的页面跳转
- ✅ **API文档同步**: 确保所有显示的API端点与官方Sunmi API文档完全一致

#### 修复详情
- **影响文件**: 
  - `app.py` - 后端API调用端点
  - `templates/unified_transfer.html` - 设备转移页面
  - `templates/bind_sub_account.html` - 子账户绑定页面
  - `templates/friend_list.html` - 好友列表页面
  - `templates/sub_account_list.html` - 子账户列表页面

- **修复内容**:
  - 设备转移API端点现在使用正确的官方端点
  - 所有UI页面显示的API信息已更新
  - 导航链接现在指向正确的功能页面
  - 确保与Sunmi官方API文档100%一致
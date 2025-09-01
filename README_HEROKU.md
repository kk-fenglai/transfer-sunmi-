# Heroku部署指南

## 前置要求

1. 安装 [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. 安装 [Git](https://git-scm.com/)
3. 注册 [Heroku账号](https://signup.heroku.com/)

## 部署步骤

### 1. 登录Heroku
```bash
heroku login
```

### 2. 创建Heroku应用
```bash
cd account
heroku create your-app-name
```

### 3. 设置环境变量
```bash
# 设置Flask密钥
heroku config:set SECRET_KEY=your-secret-key-here

# 设置邮件配置
heroku config:set MAIL_SERVER=smtp.gmail.com
heroku config:set MAIL_PORT=587
heroku config:set MAIL_USE_TLS=True
heroku config:set MAIL_USE_SSL=False
heroku config:set MAIL_USERNAME=your-email@gmail.com
heroku config:set MAIL_PASSWORD=your-app-password
heroku config:set MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### 4. 部署应用
```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main
```

### 5. 启动应用
```bash
heroku ps:scale web=1
```

### 6. 打开应用
```bash
heroku open
```

## 重要注意事项

1. **邮件配置**: 确保在Heroku环境变量中正确设置邮件服务器信息
2. **依赖管理**: 所有依赖都在 `requirements.txt` 中
3. **端口配置**: Heroku会自动分配端口，应用会从 `PORT` 环境变量读取
4. **日志查看**: 使用 `heroku logs --tail` 查看应用日志

## 故障排除

### 常见问题

1. **H10错误**: 应用崩溃，检查日志 `heroku logs --tail`
2. **H14错误**: 没有web进程运行，执行 `heroku ps:scale web=1`
3. **构建失败**: 检查 `requirements.txt` 和 `Procfile`

### 查看日志
```bash
heroku logs --tail
```

### 重启应用
```bash
heroku restart
```

## 更新应用

```bash
git add .
git commit -m "Update message"
git push heroku main
```

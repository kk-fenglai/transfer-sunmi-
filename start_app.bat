@echo off
echo ========================================
echo 📧 Sunmi API Tool - 启动脚本
echo ========================================
echo.

echo 🔧 设置邮件环境变量...
set MAIL_SERVER=smtp.gmail.com
set MAIL_PORT=587
set MAIL_USE_TLS=True
set MAIL_USE_SSL=False
set MAIL_USERNAME=davin.lian@sunmi.tech
set MAIL_PASSWORD=yjxo zycj zlot fyau
set MAIL_DEFAULT_SENDER=davin.lian@sunmi.tech

echo ✅ 环境变量设置完成
echo.
echo 📧 邮件配置信息:
echo   服务器: %MAIL_SERVER%
echo   端口: %MAIL_PORT%
echo   用户名: %MAIL_USERNAME%
echo   发件人: %MAIL_DEFAULT_SENDER%
echo.

echo 🚀 启动Flask应用...
echo 应用将在 http://localhost:5000 启动
echo 按 Ctrl+C 停止应用
echo.

python app.py

echo.
echo ⏹️ 应用已停止
pause










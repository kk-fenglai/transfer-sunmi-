@echo off
echo ========================================
echo Heroku部署脚本
echo ========================================

echo.
echo 1. 检查Heroku CLI是否安装...
heroku --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未安装Heroku CLI
    echo 请先安装: https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

echo Heroku CLI已安装

echo.
echo 2. 检查Git是否安装...
git --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未安装Git
    echo 请先安装: https://git-scm.com/
    pause
    exit /b 1
)

echo Git已安装

echo.
echo 3. 初始化Git仓库（如果还没有）...
if not exist .git (
    git init
    echo Git仓库已初始化
) else (
    echo Git仓库已存在
)

echo.
echo 4. 添加所有文件到Git...
git add .

echo.
echo 5. 提交更改...
git commit -m "Prepare for Heroku deployment"

echo.
echo 6. 请选择操作:
echo [1] 创建新的Heroku应用
echo [2] 部署到现有应用
echo [3] 退出

set /p choice="请输入选择 (1-3): "

if "%choice%"=="1" (
    echo.
    echo 创建新的Heroku应用...
    set /p appname="请输入应用名称 (或按回车使用默认名称): "
    if "%appname%"=="" (
        heroku create
    ) else (
        heroku create %appname%
    )
    goto deploy
) else if "%choice%"=="2" (
    echo.
    echo 部署到现有应用...
    set /p appname="请输入Heroku应用名称: "
    heroku git:remote -a %appname%
    goto deploy
) else if "%choice%"=="3" (
    echo 退出部署
    exit /b 0
) else (
    echo 无效选择
    pause
    exit /b 1
)

:deploy
echo.
echo 7. 设置环境变量...
echo 注意: 请根据你的邮件配置修改以下值

set /p mail_server="邮件服务器 (默认: smtp.gmail.com): "
if "%mail_server%"=="" set mail_server=smtp.gmail.com

set /p mail_username="邮箱地址: "
set /p mail_password="邮箱密码/应用专用密码: "
set /p mail_sender="发件人邮箱: "

echo.
echo 设置环境变量...
heroku config:set SECRET_KEY=your-secret-key-change-in-production
heroku config:set MAIL_SERVER=%mail_server%
heroku config:set MAIL_PORT=587
heroku config:set MAIL_USE_TLS=True
heroku config:set MAIL_USE_SSL=False
heroku config:set MAIL_USERNAME=%mail_username%
heroku config:set MAIL_PASSWORD=%mail_password%
heroku config:set MAIL_DEFAULT_SENDER=%mail_sender%

echo.
echo 8. 部署应用到Heroku...
git push heroku main

echo.
echo 9. 启动应用...
heroku ps:scale web=1

echo.
echo 10. 打开应用...
heroku open

echo.
echo ========================================
echo 部署完成！
echo ========================================
echo.
echo 有用的命令:
echo - 查看日志: heroku logs --tail
echo - 重启应用: heroku restart
echo - 查看应用状态: heroku ps
echo.
pause

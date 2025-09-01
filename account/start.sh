#!/bin/bash
# 启动脚本
echo "Starting Flask application..."
echo "Python version: $(python --version)"
echo "Pip version: $(pip --version)"
echo "Installed packages:"
pip list

echo "Starting gunicorn..."
gunicorn --bind 0.0.0.0:$PORT app:app

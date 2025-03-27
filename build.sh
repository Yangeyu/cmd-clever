#!/bin/bash
# 清理构建脚本 - 移除旧的构建文件并重新构建

set -e  # 有错误时停止脚本执行

echo "正在清理旧的构建文件..."
# 清理构建目录
rm -rf dist/
rm -rf build/
rm -rf *.egg-info/
rm -rf ccc*.egg-info/
rm -rf ccc_cli*.egg-info/
rm -rf ccc_cli_helper*.egg-info/
rm -rf __pycache__/
rm -rf ccc/__pycache__/
rm -rf tests/__pycache__/
rm -rf .pytest_cache/
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name "*.pyd" -delete
find . -name "__pycache__" -delete

echo "正在构建新的包..."
python -m build

echo "构建完成！可以使用以下命令上传到PyPI:"
echo "python -m twine upload dist/*"

echo "或者使用以下命令在开发模式下安装:"
echo "pip install -e ." 
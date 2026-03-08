#!/bin/bash
# AI-GUI 配置检查脚本

echo "🦞 AI-GUI 配置检查"
echo "=================="
echo ""

# 检查 Python
echo "1. 检查 Python 环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✓ $PYTHON_VERSION"
else
    echo "   ✗ Python3 未安装"
    exit 1
fi

# 检查依赖
echo ""
echo "2. 检查依赖包..."
python3 -c "import pyautogui" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ pyautogui 已安装"
else
    echo "   ✗ pyautogui 未安装"
    echo "   运行：pip install pyautogui"
    exit 1
fi

python3 -c "import requests" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✓ requests 已安装"
else
    echo "   ✗ requests 未安装"
    echo "   运行：pip install requests"
    exit 1
fi

# 检查视觉 API 配置
echo ""
echo "3. 检查视觉 API 配置..."
if [ -n "$OPENCLAW_API_ENDPOINT" ]; then
    echo "   ✓ API 端点：$OPENCLAW_API_ENDPOINT"
else
    echo "   ⚠️  未配置 OPENCLAW_API_ENDPOINT"
    echo "   使用默认：http://localhost:18789/api/v1/vision/analyze"
fi

if [ -n "$OPENCLAW_API_KEY" ]; then
    echo "   ✓ API 密钥已配置"
else
    echo "   ⚠️  未配置 OPENCLAW_API_KEY"
    echo "   某些 API 可能需要密钥"
fi

# 测试视觉 API 连接
echo ""
echo "4. 测试视觉 API 连接..."
python3 -c "
import requests
import os
endpoint = os.getenv('OPENCLAW_API_ENDPOINT', 'http://localhost:18789/api/v1/vision/analyze')
try:
    response = requests.get(endpoint.replace('/analyze', '/status'), timeout=5)
    if response.status_code == 200:
        print('   ✓ API 连接正常')
    else:
        print(f'   ⚠️  API 响应：{response.status_code}')
except:
    print('   ✗ 无法连接到 API')
    print('   请检查 OpenClaw 网关是否运行')
    print('   运行：openclaw gateway status')
" 2>/dev/null

# 检查权限
echo ""
echo "5. 检查辅助功能权限..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "   macOS 需要辅助功能权限"
    echo "   系统设置 → 隐私与安全性 → 辅助功能"
    echo "   添加：终端 或 Python"
elif [[ "$OSTYPE" == "linux"* ]]; then
    echo "   ✓ Linux 通常不需要特殊权限"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "   ✓ Windows 建议管理员运行"
fi

# 检查文件完整性
echo ""
echo "6. 检查文件完整性..."
FILES=(
    "ai_gui_simple.py"
    "vision_analyzer.py"
    "annotation_simple.py"
    "requirements.txt"
    "README.md"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✓ $file"
    else
        echo "   ✗ $file 缺失"
    fi
done

# 总结
echo ""
echo "=================="
echo "配置检查完成！"
echo ""
echo "下一步："
echo "1. 如果 API 未配置，设置环境变量："
echo "   export OPENCLAW_API_ENDPOINT=http://localhost:18789/api/v1/vision/analyze"
echo ""
echo "2. 测试基本功能："
echo "   python3 ai_gui_simple.py test"
echo ""
echo "3. 如果权限不足，按提示配置"
echo ""

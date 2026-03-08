#!/bin/bash
# AI-GUI GitHub 一键发布脚本

set -e

echo "🦞 AI-GUI GitHub 发布脚本"
echo "=========================="
echo ""

# 配置
REPO_NAME="ai-gui"
VERSION="2.0.0"
DESCRIPTION="AI-driven desktop GUI control"

# 检查 Git
if ! command -v git &> /dev/null; then
    echo "❌ Git 未安装，请先安装 Git"
    exit 1
fi

echo "✅ Git 已安装"

# 进入目录
cd "$(dirname "$0")"
echo "✅ 进入目录：$(pwd)"

# 初始化 Git
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
    git branch -M main
fi

# 添加文件
echo "📝 添加文件..."
git add .

# 检查是否有更改
if git diff --cached --quiet; then
    echo "⚠️  没有更改"
else
    echo "✅ 文件已添加"
    
    # 提交
    echo "💾 提交更改..."
    git commit -m "Release AI-GUI v${VERSION}

Features:
- AI vision recognition
- Human-in-the-loop collaboration  
- Independent annotation system
- Simple design (100 lines, 1 dependency)

License: MIT
"
    echo "✅ 提交完成"
fi

# 检查远程仓库
if ! git remote | grep -q origin; then
    echo ""
    echo "⚠️  未配置远程仓库"
    echo ""
    read -p "请输入 GitHub 用户名：" GITHUB_USER
    REPO_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"
    
    echo "📍 添加远程仓库：${REPO_URL}"
    git remote add origin "${REPO_URL}"
fi

echo ""
echo "✅ 准备发布"
echo ""
echo "📦 仓库信息:"
git remote -v
echo ""

# 询问是否继续
read -p "是否继续推送？(y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ 已取消"
    exit 1
fi

# 推送
echo "🚀 推送到 GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 推送成功！"
    echo ""
    
    # 获取仓库 URL
    REPO_URL=$(git remote get-url origin | sed 's/\.git$//')
    
    echo "📬 下一步操作:"
    echo ""
    echo "1. 创建 GitHub Release:"
    echo "   ${REPO_URL}/releases/new"
    echo ""
    echo "2. 添加 Topics:"
    echo "   ai, gui, automation, python, vision"
    echo ""
    echo "3. 设置 Website:"
    echo "   https://clawhub.com/skills/ai-gui"
    echo ""
    echo "4. 分享到社交媒体:"
    echo "   ${REPO_URL}"
    echo ""
    echo "🎉 发布完成！"
else
    echo ""
    echo "❌ 推送失败"
    echo ""
    echo "可能的原因:"
    echo "- 未配置 GitHub 凭证"
    echo "- 仓库不存在"
    echo "- 权限不足"
    echo ""
    echo "解决方法:"
    echo "1. 创建 GitHub Personal Access Token"
    echo "2. git remote set-url origin https://TOKEN@github.com/USER/ai-gui.git"
    echo "3. 重新运行此脚本"
fi

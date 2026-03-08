# 🐙 GitHub 发布指南

## 快速发布（推荐）

### 方式 1：使用脚本

```bash
# 进入目录
cd /root/C:\Users\35258\.openclaw\workspace/skills/ai-gui

# 初始化 Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Release AI-GUI v2.0.0

Features:
- AI vision recognition
- Human-in-the-loop collaboration
- Independent annotation system
- Simple design (100 lines, 1 dependency)"

# 添加远程仓库（替换为你的仓库）
git remote add origin https://github.com/your-username/ai-gui.git

# 推送
git push -u origin main
```

---

### 方式 2：手动操作

#### 1. 创建 GitHub 仓库

```
访问：https://github.com/new

填写：
- Repository name: ai-gui
- Description: AI-driven desktop GUI control
- Visibility: Public
- Initialize with README: No (我们已有)
```

#### 2. 推送代码

```bash
cd /root/C:\Users\35258\.openclaw\workspace/skills/ai-gui

git init
git add .
git commit -m "Initial release: AI-GUI v2.0.0"
git branch -M main
git remote add origin https://github.com/your-username/ai-gui.git
git push -u origin main
```

---

## 创建 Release

### 方式 1：GitHub CLI

```bash
# 安装 gh (如果未安装)
# https://cli.github.com/

# 创建 Release
gh release create v2.0.0 \
  --title "AI-GUI v2.0.0" \
  --notes "See RELEASE.md for details" \
  --generate-notes

# 上传压缩包
gh release upload v2.0.0 ../ai-gui-v2.0.0-github.tar.gz
```

### 方式 2：GitHub 网页

```
1. 访问：https://github.com/your-username/ai-gui/releases/new
2. Tag version: v2.0.0
3. Release title: AI-GUI v2.0.0
4. Description: (复制 RELEASE.md 内容)
5. Upload: ai-gui-v2.0.0-github.tar.gz
6. Publish Release
```

---

## GitHub Actions（可选）

### 自动发布

创建 `.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: ai-gui-v*.tar.gz
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 项目结构

```
ai-gui/
├── .gitignore           # Git 忽略文件
├── LICENSE              # MIT 许可证
├── README.md            # GitHub README
├── RELEASE.md           # 发布说明
├── ANNOTATION_DESIGN.md # 标注设计文档
├── ai_gui_simple.py     # 主程序
├── annotation_simple.py # 标注收集
├── requirements.txt     # Python 依赖
└── clawhub.yaml         # ClawHub 配置
```

---

## 最佳实践

### 1. 语义化版本

```
v2.0.0
│ │ │
│ │ └─ 补丁版本（Bug 修复）
│ └─── 次版本（新功能，向后兼容）
└───── 主版本（重大变更）
```

### 2. 提交信息规范

```
feat: 添加新功能
fix: 修复 Bug
docs: 更新文档
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

### 3. Branch 策略

```
main        - 稳定版本
develop     - 开发分支
feature/xxx - 新功能
bugfix/xxx  - Bug 修复
```

---

## 推广建议

### 1. GitHub 特性

```
✅ 添加 Topics: ai, gui, automation, python
✅ 设置 Website: https://clawhub.com/skills/ai-gui
✅ 添加 Issue 模板
✅ 启用 Discussions
✅ 添加 Sponsor 按钮
```

### 2. 社交媒体

```
🦞 发布了 AI-GUI v2.0.0！

GitHub: https://github.com/your-username/ai-gui

特点:
✅ AI 视觉识别
✅ 人机协同
✅ 数据驱动
✅ 简洁设计

#AI #GUI #Python #OpenSource
```

### 3. 技术社区

```
- Reddit: r/Python, r/MachineLearning
- Hacker News
- V2EX
- 知乎
- 掘金
```

---

## 统计与监控

### GitHub Insights

```
访问：https://github.com/your-username/ai-gui/pulse

查看：
- Clone 数量
- Visitor 数量
- Star/Fork 趋势
- 贡献者活动
```

### 添加 Badge

```markdown
[![Stars](https://img.shields.io/github/stars/your-username/ai-gui)](https://github.com/your-username/ai-gui/stargazers)
[![Forks](https://img.shields.io/github/forks/your-username/ai-gui)](https://github.com/your-username/ai-gui/network/members)
[![Issues](https://img.shields.io/github/issues/your-username/ai-gui)](https://github.com/your-username/ai-gui/issues)
```

---

## 下一步

### 发布后立即执行

```bash
# 1. 验证发布
curl https://github.com/your-username/ai-gui

# 2. 分享
# - 社交媒体
# - 技术社区
# - 朋友圈

# 3. 监控
# - GitHub Insights
# - Issues
# - Stars
```

### 一周内

```
□ 回复 Issues
□ 合并 PRs
□ 更新文档
□ 统计数据
```

### 持续维护

```
□ 每月更新版本
□ 收集用户反馈
□ 优化性能
□ 添加新功能
```

---

## 常见问题

### Q: 如何更新版本？

```bash
# 1. 修改版本号（clawhub.yaml, README.md）
# 2. 提交
git commit -m "Release v2.0.1"
# 3. 打标签
git tag v2.0.1
# 4. 推送
git push origin v2.0.1
```

### Q: 如何处理 Issue？

```
1. 及时回复（24 小时内）
2. 添加标签（bug, enhancement, question）
3. 分配负责人
4. 跟踪进度
```

### Q: 如何接受贡献？

```
1. 添加 CONTRIBUTING.md
2. 创建 Pull Request 模板
3. 设置 Code Review 流程
4. 合并前测试
```

---

_发布到 GitHub，让更多人使用！_ 🦞🐙

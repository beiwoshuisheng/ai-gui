# 🦞 AI-GUI 双平台发布指南

> GitHub + ClawHub 同步发布

---

## ✅ 当前状态

### GitHub
- ✅ 本地仓库已创建
- ✅ 代码已提交（v2.0.0）
- ✅ 13 个文件，2228 行代码
- ⏳ 待推送远程仓库

### ClawHub
- ✅ clawhub.yaml 已配置
- ✅ 技能文件已准备
- ⏳ 待上传发布

---

## 📍 下一步操作

### 1. 推送到 GitHub

**方式 A：手动创建仓库（推荐）**

```
1. 访问：https://github.com/new
2. 填写：
   - Repository name: ai-gui
   - Description: AI-driven desktop GUI control
   - Visibility: Public
3. 创建仓库
4. 复制仓库 URL（如：https://github.com/your-username/ai-gui.git）
5. 执行：
   cd /root/C:\Users\35258\.openclaw\workspace/skills/ai-gui
   git remote add origin <仓库 URL>
   git push -u origin main
```

**方式 B：使用发布脚本**

```bash
cd /root/C:\Users\35258\.openclaw\workspace/skills/ai-gui
./publish-to-github.sh
# 按提示输入 GitHub 用户名
```

---

### 2. 发布到 ClawHub

**网页发布：**

```
1. 访问：https://clawhub.com/skills/publish
2. 登录 OpenClaw 账号
3. 上传文件：
   - 打包：tar -czvf ai-gui-v2.0.0.tar.gz ai-gui/
   - 上传：ai-gui-v2.0.0.tar.gz
4. 填写信息：
   - 名称：ai-gui
   - 版本：2.0.0
   - 描述：AI 驱动的桌面 GUI 控制
   - 分类：自动化工具
   - 标签：AI, GUI, 视觉识别，人机协同
5. 提交审核
```

**CLI 发布（如果支持）：**

```bash
# 查看可用命令
openclaw --help | grep -i publish

# 或使用 skills 命令
openclaw skills list
```

---

### 3. 双平台关联

**GitHub README 添加 ClawHub 链接：**

```markdown
## 安装

### ClawHub（推荐）
```bash
openclaw skills install ai-gui
```

### GitHub
```bash
git clone https://github.com/your-username/ai-gui.git
```
```

**ClawHub 页面添加 GitHub 链接：**

```
在 ClawHub 发布页面的"项目主页"字段填写：
https://github.com/your-username/ai-gui
```

---

## 📋 发布检查清单

### GitHub
```
□ 创建仓库
□ 推送代码
□ 创建 Release（v2.0.0）
□ 配置仓库信息
□ 添加 Topics
□ 设置 Website 链接
```

### ClawHub
```
□ 打包技能
□ 上传文件
□ 填写信息
□ 提交审核
□ 等待通过
```

### 关联
```
□ GitHub README 添加 ClawHub 链接
□ ClawHub 页面添加 GitHub 链接
□ 社交媒体分享
```

---

## 🚀 快速执行命令

### 查看当前状态

```bash
# GitHub 状态
cd /root/C:\Users\35258\.openclaw\workspace/skills/ai-gui
git status
git log --oneline

# 打包文件
cd ..
tar -czvf ai-gui-v2.0.0.tar.gz ai-gui/
ls -lh ai-gui-v2.0.0.tar.gz
```

### 推送 GitHub

```bash
cd /root/C:\Users\35258\.openclaw\workspace/skills/ai-gui

# 添加远程仓库（替换为你的用户名）
git remote add origin https://github.com/YOUR_USERNAME/ai-gui.git

# 推送
git push -u origin main
```

### 打包 ClawHub

```bash
cd /root/C:\Users\35258\.openclaw\workspace/skills
tar -czvf ai-gui-v2.0.0.tar.gz ai-gui/
ls -lh ai-gui-v2.0.0.tar.gz
```

---

## 📊 发布后验证

### GitHub

```
访问：https://github.com/YOUR_USERNAME/ai-gui

检查：
□ 代码已显示
□ README 正确渲染
□ 文件完整（13 个文件）
□ License 显示
```

### ClawHub

```
访问：https://clawhub.com/skills/ai-gui

检查：
□ 技能已上架
□ 描述正确
□ 安装命令可用
□ 下载链接有效
```

---

## 🎯 发布后任务

### 立即执行

```bash
# 1. 验证 GitHub
curl https://github.com/YOUR_USERNAME/ai-gui

# 2. 验证 ClawHub
openclaw skills search ai-gui

# 3. 分享
# - 社交媒体
# - 技术社区
# - 朋友圈
```

### 一周内

```
□ 收集用户反馈
□ 回复 Issues
□ 统计数据（下载量、Star 数）
□ 规划 v2.1.0
```

---

## 📈 推广模板

### 社交媒体

```
🦞 发布了 AI-GUI v2.0.0！

GitHub: https://github.com/YOUR_USERNAME/ai-gui
ClawHub: https://clawhub.com/skills/ai-gui

特点:
✅ AI 视觉识别
✅ 人机协同
✅ 数据驱动
✅ 简洁设计（100 行代码）

#AI #GUI #Python #OpenSource
```

### 技术社区

```
标题：我开源了 AI-GUI - 让 AI 看懂屏幕，用自然语言控制电脑

内容：
- 设计理念（简洁 + 独立标注）
- 技术实现（AI 视觉 + 人机协同）
- 使用示例
- 数据驱动优化
- GitHub + ClawHub 双平台

链接：
- GitHub: https://github.com/YOUR_USERNAME/ai-gui
- ClawHub: https://clawhub.com/skills/ai-gui
```

---

## 🆘 常见问题

### Q: GitHub 推送失败？

```
原因：未配置认证
解决：
1. 创建 Personal Access Token
   https://github.com/settings/tokens
2. 使用 Token 推送：
   git remote set-url origin https://TOKEN@github.com/USER/ai-gui.git
   git push -u origin main
```

### Q: ClawHub 审核不通过？

```
原因：信息不完整
解决：
1. 补充描述
2. 添加使用示例
3. 确认 LICENSE
4. 重新提交
```

### Q: 双平台如何同步更新？

```
1. 先在 GitHub 更新
2. 打新版本标签（如 v2.1.0）
3. 同步更新 ClawHub
4. 在两个平台都更新版本号
```

---

**准备就绪！请告诉我你的 GitHub 用户名，或者手动执行上述命令！** 🦞🚀

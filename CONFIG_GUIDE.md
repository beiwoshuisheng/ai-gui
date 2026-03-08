# AI-GUI 配置指南

> 🦞 完整配置说明和检查清单

---

## 📋 配置检查清单

### 1. Python 环境

**要求：** Python 3.8+

```bash
# 检查 Python 版本
python3 --version

# 如果未安装，请安装：
# Ubuntu/Debian: sudo apt install python3
# macOS: brew install python@3.11
# Windows: winget install Python.Python.3.11
```

---

### 2. 安装依赖

**方式 1：虚拟环境（推荐）**

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt
```

**方式 2：系统范围安装**

```bash
# Ubuntu/Debian（需要 --break-system-packages）
pip install --break-system-packages -r requirements.txt

# macOS（推荐用虚拟环境）
pip install -r requirements.txt

# Windows
pip install -r requirements.txt
```

**依赖列表：**
```
pyautogui>=0.9.54      # GUI 控制
requests>=2.28.0       # HTTP 请求
pillow>=10.0.0         # 图像处理
```

---

### 3. 视觉 API 配置

**环境变量：**

```bash
# 配置 API 端点（可选，默认使用 localhost:18789）
export OPENCLAW_API_ENDPOINT=http://localhost:18789/api/v1/vision/analyze

# 配置 API 密钥（如果网关需要认证）
export OPENCLAW_API_KEY=your_api_key_here

# 配置超时（可选，默认 10 秒）
export AI_GUI_TIMEOUT=15
```

**永久配置（添加到 ~/.bashrc 或 ~/.zshrc）：**

```bash
echo 'export OPENCLAW_API_ENDPOINT=http://localhost:18789/api/v1/vision/analyze' >> ~/.bashrc
echo 'export OPENCLAW_API_KEY=your_api_key' >> ~/.bashrc
source ~/.bashrc
```

---

### 4. OpenClaw 网关配置

**检查网关是否运行：**

```bash
openclaw gateway status
```

**如果未运行，启动网关：**

```bash
openclaw gateway start
```

**配置视觉 API（在 openclaw.json 中）：**

```json
{
  "vision": {
    "enabled": true,
    "model": "qwen-vl-max",
    "endpoint": "/api/v1/vision/analyze",
    "timeout": 10000
  }
}
```

---

### 5. 系统权限

**macOS：**

```
系统设置 → 隐私与安全性 → 辅助功能
添加：
- 终端
- Python（如果在虚拟环境中）
```

**Windows：**

```
建议以管理员身份运行
或右键 → 以管理员身份运行
```

**Linux：**

```bash
# 安装必要的包
sudo apt install python3-tk scrot

# 如果使用 Wayland，可能需要额外配置
```

---

## 🔍 配置检查工具

**运行配置检查：**

```bash
cd /root/C:\Users\35258\.openclaw\workspace/skills/ai-gui
chmod +x check-config.sh
./check-config.sh
```

**检查内容：**
- ✅ Python 环境
- ✅ 依赖包
- ✅ API 配置
- ✅ API 连接
- ✅ 系统权限
- ✅ 文件完整性

---

## 🧪 测试

### 测试 1：基本功能

```bash
# 测试点击（模拟）
python3 ai_gui_simple.py test
```

### 测试 2：视觉 API

```bash
cd ai-gui
python3 vision_analyzer.py
```

**预期输出：**
```
视觉分析模块测试
==================================================
测试 API 连接...
✓ API 连接正常
```

### 测试 3：实际点击

```bash
# 先打开一个窗口（如记事本）
# 然后运行：
python3 ai_gui_simple.py click "关闭按钮" --auto
```

---

## ⚠️ 常见问题

### Q1: pyautogui 安装失败

**错误：**
```
error: externally-managed-environment
```

**解决：**
```bash
# 方式 1：使用虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install pyautogui

# 方式 2：强制安装（不推荐）
pip install --break-system-packages pyautogui
```

---

### Q2: 无法连接视觉 API

**错误：**
```
✗ 无法连接到 API
```

**解决：**
```bash
# 1. 检查网关是否运行
openclaw gateway status

# 2. 检查端点配置
echo $OPENCLAW_API_ENDPOINT

# 3. 测试连接
curl http://localhost:18789/api/v1/vision/analyze
```

---

### Q3: 鼠标键盘无响应

**macOS：**
```
检查辅助功能权限
系统设置 → 隐私 → 辅助功能
```

**Windows：**
```
以管理员身份运行
```

**Linux：**
```bash
sudo apt install python3-tk scrot
```

---

### Q4: 点击位置不准确

**可能原因：**
1. 屏幕缩放比例不是 100%
2. 多显示器配置
3. AI 识别误差

**解决：**
```bash
# 检查屏幕分辨率
xdpyinfo | grep resolution  # Linux
system_profiler DisplaysDataType  # macOS

# 调整置信度阈值
# 编辑 ai_gui_simple.py，修改：
CONFIDENCE_HIGH = 0.95  # 提高阈值
CONFIDENCE_MEDIUM = 0.75
```

---

## 📊 配置验证

**完整验证流程：**

```bash
# 1. 运行配置检查
./check-config.sh

# 2. 测试视觉 API
python3 vision_analyzer.py

# 3. 测试基本功能
python3 ai_gui_simple.py test

# 4. 实际测试（手动确认目标位置）
python3 ai_gui_simple.py click "测试按钮" --auto
```

---

## 🎯 推荐配置

### 开发环境

```bash
# 虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export OPENCLAW_API_ENDPOINT=http://localhost:18789/api/v1/vision/analyze
export AI_GUI_TIMEOUT=15
```

### 生产环境

```bash
# 系统范围安装
sudo pip install pyautogui requests pillow

# 配置 systemd 服务（可选）
# 配置环境变量在 /etc/environment
```

---

## 📝 环境变量总结

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OPENCLAW_API_ENDPOINT` | localhost:18789 | 视觉 API 端点 |
| `OPENCLAW_API_KEY` | 空 | API 认证密钥 |
| `AI_GUI_TIMEOUT` | 10 | API 超时（秒） |
| `AI_GUI_ANNOTATION` | false | 是否启用标注 |

---

**配置完成！可以开始使用 AI-GUI 了！** 🦞✨

---
name: ai-gui
description: "AI 驱动的桌面 GUI 自动化 - 大模型视觉识别 + 人机协同 + 数据驱动。核心：语义识别、用户习惯学习、标注数据积累。越用越懂你。"
allowed-tools: Bash(python3 *)
triggers:
  - 点击
  - 拖拽
  - 输入
  - 识别
  - 找到
  - 打开
  - 关闭
  - 截图
  - 视觉
  - 图像识别
  - 记住
  - 学习
---

# ai-gui - AI 驱动的桌面 GUI 控制

## 核心理念

**传统 GUI 自动化：**
- ❌ 固定坐标（界面变了就失效）
- ❌ 模板匹配（需要精确截图）
- ❌ 死板规则（无法理解语义）

**ai-gui：**
- ✅ AI 语义识别（说"登录按钮"就能找到）
- ✅ 动态定位（界面自适应）
- ✅ 自然语言交互（零学习成本）

---

## 使用方式

### 通过 OpenClaw exec 调用

```bash
# AI 点击
openclaw exec --command "python ai_gui.py click '登录按钮'"

# AI 拖拽
openclaw exec --command "python ai_gui.py drag '文件.txt' '回收站'"

# AI 输入
openclaw exec --command "python ai_gui.py type 'Hello' '输入框'"

# 列出元素
openclaw exec --command "python ai_gui.py list"
```

### 通过消息触发

```
用户：帮我点一下登录按钮
AI: 好的！
    → exec: python ai_gui.py click "登录按钮"
    → AI 识别并点击
    → ✓ 完成！

用户：把这个文件拖到回收站
AI: 好的！
    → exec: python ai_gui.py drag "文件" "回收站"
    → AI 识别并拖拽
    → ✓ 完成！
```

---

## API 配置

需要 OpenClaw 网关支持视觉分析：

```json
{
  "vision": {
    "enabled": true,
    "model": "qwen-vl-max",
    "endpoint": "/api/v1/vision/analyze"
  }
}
```

---

## 核心函数

### ai_click(target_description)

AI 识别并点击目标。

```python
ai_click("登录按钮")
ai_click("提交按钮")
ai_click("右上角关闭按钮")
```

### ai_drag(from_target, to_target)

AI 识别并拖拽。

```python
ai_drag("文件.txt", "回收站")
ai_drag("这张图片", "桌面")
```

### ai_type(text, target_description)

AI 识别输入框并输入。

```python
ai_type("Hello", "搜索框")
ai_type("用户名", "用户名输入框")
```

### show_ui_elements()

列出屏幕所有可交互元素。

```python
elements = show_ui_elements()
```

---

## 技术架构

```
用户指令 → AI 视觉分析 → 坐标定位 → 执行操作
   ↓           ↓            ↓          ↓
"点登录"   截图 + 大模型   (x,y)    pyautogui.click
```

---

## 优势对比

| 场景 | 传统方式 | ai-gui |
|------|---------|--------|
| 按钮定位 | 需要坐标/模板 | 说"登录按钮" |
| 界面变化 | 需要重新配置 | AI 自适应 |
| 学习成本 | 几天 | 5 分钟 |
| 维护成本 | 高 | 低 |

---

## 注意事项

⚠️ **需要网络** - AI 识别需要调用 API
⚠️ **隐私考虑** - 截图会发送到 AI 服务
⚠️ **性能** - 比传统方式慢 1-2 秒

---

## 示例工作流

### 自动登录

```bash
python ai_gui.py type "myusername" "用户名"
python ai_gui.py type "mypassword" "密码"
python ai_gui.py click "登录"
```

### 文件整理

```bash
python ai_gui.py drag "截图.png" "图片文件夹"
python ai_gui.py drag "文档.pdf" "文档文件夹"
```

### 表单填写

```bash
python ai_gui.py type "张三" "姓名"
python ai_gui.py type "zhangsan@example.com" "邮箱"
python ai_gui.py click "提交"
```

---

## 依赖安装

```bash
pip install pyautogui requests pillow
```

---

_让 AI 看懂屏幕，用自然语言控制电脑！_ 🦞

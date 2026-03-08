# 🦞 AI-GUI 视觉 API 快速配置

> ✅ **不修改 OpenClaw 主配置** - 独立配置文件

---

## 🚀 快速配置（3 步）

### 步骤 1：运行配置工具

```bash
cd /root/C:\Users\35258\.openclaw\workspace/skills/ai-gui
python3 vision_config.py setup
```

### 步骤 2：输入 API Key

```
请输入新配置（直接回车使用默认值）：

模型名称 [qwen-vl-max]: 
提供商 [bailian]: 
API 基础 URL [https://coding.dashscope.aliyuncs.com/v1]: 
API Key: sk-your-api-key-here
超时时间 (毫秒) [10000]: 
API 端点 [/api/v1/vision/analyze]: 
```

### 步骤 3：测试连接

```bash
python3 vision_config.py test
```

**完成！** ✅

---

## 📋 配置说明

### 配置文件位置

```
~/.openclaw/ai-gui/vision_config.json
```

**特点：**
- ✅ 独立配置，不影响 OpenClaw 主配置
- ✅ 只供 AI-GUI 使用
- ✅ 可以随时修改或删除

---

### 配置项说明

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `model` | qwen-vl-max | 视觉模型名称 |
| `provider` | bailian | 提供商（bailian/openai 等） |
| `base_url` | 阿里百炼 API | API 基础 URL |
| `api_key` | 空 | 你的 API Key |
| `timeout` | 10000 | 超时时间（毫秒） |
| `endpoint` | /api/v1/vision/analyze | API 端点 |

---

## 🔧 配置方式对比

### 方式 1：交互式配置（推荐）

```bash
python3 vision_config.py setup
```

**优点：**
- ✅ 简单直观
- ✅ 自动验证
- ✅ 保存配置

---

### 方式 2：手动编辑配置文件

```bash
# 创建配置目录
mkdir -p ~/.openclaw/ai-gui

# 编辑配置文件
nano ~/.openclaw/ai-gui/vision_config.json
```

**配置内容：**

```json
{
  "enabled": true,
  "model": "qwen-vl-max",
  "provider": "bailian",
  "base_url": "https://coding.dashscope.aliyuncs.com/v1",
  "api_key": "sk-your-api-key",
  "timeout": 10000,
  "endpoint": "/api/v1/vision/analyze"
}
```

---

### 方式 3：环境变量（临时）

```bash
export AI_GUI_VISION_API_KEY=sk-your-api-key
export AI_GUI_VISION_MODEL=qwen-vl-max
export AI_GUI_VISION_TIMEOUT=10000
```

**优点：**
- ✅ 临时测试
- ✅ 不创建文件

**缺点：**
- ❌ 每次终端都要设置
- ❌ 不安全（会暴露在历史命令中）

---

## 📊 获取 API Key

### 阿里百炼（推荐）

**步骤：**

```
1. 访问：https://dashscope.console.aliyun.com/
2. 登录/注册阿里云账号
3. 开通 DashScope 服务
4. 创建 API Key
5. 复制 Key（以 sk- 开头）
```

**免费额度：**
- ✅ 新用户赠送额度
- ✅ qwen-vl-max 有一定免费调用次数

---

### 其他提供商

| 提供商 | 获取地址 | 免费额度 |
|--------|---------|---------|
| **阿里百炼** | https://dashscope.console.aliyun.com/ | ✅ 有 |
| **OpenAI** | https://platform.openai.com/ | ❌ 无 |
| **Anthropic** | https://console.anthropic.com/ | ❌ 无 |
| **Google** | https://makersuite.google.com/ | ✅ 有 |

---

## 🧪 测试配置

### 测试 1：检查配置

```bash
python3 vision_config.py show
```

**输出示例：**
```
当前视觉 API 配置：

  enabled: True
  model: qwen-vl-max
  provider: bailian
  base_url: https://coding.dashscope.aliyuncs.com/v1
  api_key: ***xxxx1234
  timeout: 10000
  endpoint: /api/v1/vision/analyze
```

---

### 测试 2：测试 API 连接

```bash
python3 vision_config.py test
```

**预期输出：**
```
🔍 测试视觉 API 连接...

模型：qwen-vl-max
提供商：bailian
API URL: https://coding.dashscope.aliyuncs.com/v1

✓ API 连接正常
```

---

### 测试 3：实际使用

```bash
# 测试视觉识别
python3 ai_gui_simple.py test
```

---

## ⚠️ 常见问题

### Q1: 没有 API Key

**解决：**
```
1. 访问阿里云 DashScope 控制台
2. 注册/登录
3. 创建 API Key
4. 复制到配置文件
```

---

### Q2: API Key 无效

**错误：**
```
✗ API Key 无效
```

**解决：**
```bash
# 1. 检查 Key 是否正确复制
python3 vision_config.py show

# 2. 重新配置
python3 vision_config.py setup

# 3. 确保 Key 以 sk- 开头
```

---

### Q3: 连接超时

**错误：**
```
✗ 无法连接到 API 服务器
```

**解决：**
```bash
# 1. 检查网络连接
ping dashscope.aliyuncs.com

# 2. 增加超时时间
python3 vision_config.py setup
# 超时时间设置为 30000

# 3. 检查防火墙
```

---

### Q4: 配置文件找不到

**错误：**
```
配置文件不存在
```

**解决：**
```bash
# 运行配置工具创建配置文件
python3 vision_config.py setup

# 或手动创建
mkdir -p ~/.openclaw/ai-gui
nano ~/.openclaw/ai-gui/vision_config.json
```

---

## 🎯 最佳实践

### 1. 使用独立配置

```
✅ 优点：
- 不影响 OpenClaw 主配置
- 可以随时修改
- 可以删除不影响其他功能
```

### 2. 保护 API Key

```bash
# 设置文件权限
chmod 600 ~/.openclaw/ai-gui/vision_config.json

# 或使用环境变量
export AI_GUI_VISION_API_KEY=sk-xxx
```

### 3. 监控使用情况

```bash
# 查看阿里百炼使用量
# 访问：https://dashscope.console.aliyun.com/usage
```

---

## 📝 完整示例

### 配置阿里百炼

```bash
# 1. 运行配置工具
cd /root/C:\Users\35258\.openclaw\workspace/skills/ai-gui
python3 vision_config.py setup

# 2. 输入配置
模型名称 [qwen-vl-max]: qwen-vl-max
提供商 [bailian]: bailian
API 基础 URL [https://coding.dashscope.aliyuncs.com/v1]: https://coding.dashscope.aliyuncs.com/v1
API Key: sk-xxxxxxxxxxxxxxxx
超时时间 (毫秒) [10000]: 10000
API 端点 [/api/v1/vision/analyze]: /api/v1/vision/analyze

# 3. 测试
python3 vision_config.py test

# 4. 使用
python3 ai_gui_simple.py click "测试按钮"
```

---

**配置完成！现在可以安全使用视觉 API，不影响 OpenClaw 主配置！** 🦞✨

# OpenClaw Skill 视觉 API 配置指南

> 🦞 如何为 AI-GUI 等 skill 配置视觉分析能力

---

## 📋 配置方法

### 方法 1：使用现有模型配置（推荐）

AI-GUI 会自动使用 OpenClaw 默认的多模态模型。

**检查当前模型配置：**

```bash
openclaw config get models.providers
```

**如果已有支持图像的模型（如 qwen-vl），AI-GUI 会自动使用。**

---

### 方法 2：添加视觉专用模型

**编辑 `~/.openclaw/openclaw.json`：**

```json
{
  "models": {
    "providers": {
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "sk-your-api-key",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen-vl-max",
            "name": "Qwen-VL-Max",
            "api": "openai-completions",
            "reasoning": false,
            "input": ["text", "image"],
            "output": ["text"],
            "context": 8000,
            "cost": {
              "input": 0.02,
              "output": 0.06
            }
          }
        ]
      }
    ],
    "defaults": {
      "vision": "bailian/qwen-vl-max"
    }
  }
}
```

---

### 方法 3：为 Skill 单独配置

**在 openclaw.json 中添加 skill 特定配置：**

```json
{
  "skills": {
    "ai-gui": {
      "vision": {
        "enabled": true,
        "model": "bailian/qwen-vl-max",
        "timeout": 10000
      }
    }
  }
}
```

---

## 🔧 AI-GUI Skill 配置

### 环境变量方式

**在 `~/.bashrc` 或 `~/.zshrc` 中添加：**

```bash
# AI-GUI 视觉 API 配置
export AI_GUI_VISION_MODEL=bailian/qwen-vl-max
export AI_GUI_VISION_TIMEOUT=10000
export AI_GUI_VISION_ENDPOINT=http://localhost:18789/api/v1/vision/analyze
```

### Skill 内部配置

**编辑 `ai_gui_simple.py`：**

```python
# 在文件开头添加配置
VISION_CONFIG = {
    'model': 'bailian/qwen-vl-max',
    'timeout': 10000,
    'endpoint': 'http://localhost:18789/api/v1/vision/analyze'
}
```

---

## 🧪 测试配置

### 测试 1：检查模型是否支持视觉

```bash
openclaw config get models.providers.bailian.models
```

**查找有 `"input": ["text", "image"]` 的模型。**

---

### 测试 2：测试视觉 API

```bash
cd /root/C:\Users\35258\.openclaw\workspace/skills/ai-gui
python3 vision_analyzer.py
```

**预期输出：**
```
视觉分析模块测试
==================================================
测试 API 连接...
✓ API 连接正常
```

---

### 测试 3：实际使用

```bash
# 截图并识别
python3 -c "
from vision_analyzer import VisionAnalyzer
from PIL import Image

analyzer = VisionAnalyzer()
screenshot = Image.new('RGB', (1920, 1080), color='white')
result = analyzer.analyze('测试按钮', screenshot)
print(result)
"
```

---

## 📊 视觉模型推荐

### 推荐模型

| 模型 | 提供商 | 准确率 | 速度 | 成本 |
|------|--------|--------|------|------|
| **qwen-vl-max** | 阿里 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中 |
| **gpt-4-vision** | OpenAI | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 高 |
| **claude-3-vision** | Anthropic | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 高 |
| **gemini-pro-vision** | Google | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中 |

---

### 配置示例（阿里百炼）

```json
{
  "models": {
    "providers": {
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "sk-your-api-key",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen-vl-max",
            "name": "Qwen-VL-Max",
            "input": ["text", "image"],
            "context": 8000
          }
        ]
      }
    }
  }
}
```

---

### 配置示例（OpenAI）

```json
{
  "models": {
    "providers": {
      "openai": {
        "baseUrl": "https://api.openai.com/v1",
        "apiKey": "sk-your-openai-key",
        "api": "openai-completions",
        "models": [
          {
            "id": "gpt-4-vision-preview",
            "name": "GPT-4 Vision",
            "input": ["text", "image"],
            "context": 128000
          }
        ]
      }
    }
  }
}
```

---

## ⚠️ 常见问题

### Q1: 找不到视觉模型

**错误：**
```
Model not found: qwen-vl-max
```

**解决：**
```bash
# 1. 检查模型配置
openclaw config get models.providers

# 2. 添加视觉模型（见上方配置示例）

# 3. 重启网关
openclaw gateway restart
```

---

### Q2: API 调用失败

**错误：**
```
API 调用失败：401
```

**解决：**
```bash
# 检查 API 密钥
openclaw config get models.providers.bailian.apiKey

# 如果为空，设置密钥
openclaw config set models.providers.bailian.apiKey sk-your-key
```

---

### Q3: 超时或响应慢

**解决：**
```bash
# 增加超时时间
export AI_GUI_VISION_TIMEOUT=30000

# 或修改配置文件
{
  "skills": {
    "ai-gui": {
      "vision": {
        "timeout": 30000
      }
    }
  }
}
```

---

## 🎯 最佳实践

### 1. 使用本地网关

```json
{
  "vision": {
    "endpoint": "http://localhost:18789/api/v1/vision/analyze"
  }
}
```

**优点：**
- ✅ 低延迟
- ✅ 数据隐私
- ✅ 离线可用（如果本地有模型）

---

### 2. 配置备用模型

```json
{
  "models": {
    "defaults": {
      "vision": "bailian/qwen-vl-max",
      "vision_backup": "openai/gpt-4-vision-preview"
    }
  }
}
```

---

### 3. 监控使用情况

```bash
# 查看视觉 API 调用统计
openclaw status --vision

# 或查看日志
openclaw logs --follow | grep vision
```

---

## 📝 完整配置示例

**`~/.openclaw/openclaw.json`：**

```json
{
  "models": {
    "providers": {
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "sk-your-api-key",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen-vl-max",
            "name": "Qwen-VL-Max",
            "input": ["text", "image"],
            "output": ["text"],
            "context": 8000,
            "cost": {
              "input": 0.02,
              "output": 0.06
            }
          }
        ]
      }
    },
    "defaults": {
      "chat": "bailian/qwen3.5-plus",
      "vision": "bailian/qwen-vl-max",
      "code": "bailian/qwen3.5-plus"
    }
  },
  "skills": {
    "ai-gui": {
      "vision": {
        "enabled": true,
        "model": "bailian/qwen-vl-max",
        "timeout": 10000,
        "confidence_threshold": 0.7
      }
    }
  }
}
```

---

**配置完成！现在 AI-GUI 可以使用视觉 API 识别屏幕元素了！** 🦞✨

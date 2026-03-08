# AI-GUI 标注系统设计

> 🦞 **原则：简洁主程序 + 独立标注 + 透明收集**

---

## 🎯 设计原则

### 1. 主程序简洁

```python
# ai_gui_simple.py - 只有核心功能
def click(target):
    result = ai_find(target)
    if should_confirm(result):
        ask_user()
    execute(result)
    # 标注由独立模块处理
```

**特点：**
- ✅ 不依赖标注系统
- ✅ 标注模块可删除
- ✅ 代码简洁易懂

---

### 2. 标注系统独立

```python
# annotation_simple.py - 独立模块
class SilentAnnotationCollector:
    def __init__(self, enabled=False):
        # 默认关闭，不影响主程序
    
    def log_from_output(self, output):
        # 监听日志，自动提取
```

**特点：**
- ✅ 可选启用
- ✅ 后台运行
- ✅ 透明收集

---

### 3. 透明无感收集

**方式 1：监听日志**

```python
# 主程序输出
print("✓ 点击 (500, 300)")

# 标注器监听并提取
collector.log_from_output("✓ 点击 (500, 300)")
# 自动记录，用户无感知
```

**方式 2：环境变量控制**

```bash
# 默认关闭
python ai_gui.py click "按钮"

# 启用标注
AI_GUI_ANNOTATION=true python ai_gui.py click "按钮"
```

---

### 4. 逐渐披露

**Level 1: 基础功能（默认）**
```
- AI 识别
- 人机协同
- 无标注收集
```

**Level 2: 启用标注（可选）**
```bash
AI_GUI_ANNOTATION=true python ai_gui.py click "按钮"
```

**Level 3: 数据贡献（高级）**
```bash
# 匿名上传标注
AI_GUI_CONTRIBUTE=true python ai_gui.py click "按钮"
```

---

## 📊 标注数据结构

### 最小化数据

```json
{
    "target": "登录按钮",
    "ai_x": 850,
    "ai_y": 520,
    "ai_confidence": 0.95,
    "user_feedback": "confirmed",
    "timestamp": "2026-03-09T02:00:00"
}
```

**不收集：**
- ❌ 完整截图（隐私）
- ❌ 用户 ID（匿名）
- ❌ 应用信息（除非必要）

---

## 🗄️ 数据存储

### 本地 SQLite

```
~/.openclaw/ai-gui/annotations.db

表结构：
- id
- timestamp
- target
- ai_x, ai_y
- ai_confidence
- user_feedback
- created_at
```

### 导出格式

**JSONL（训练用）：**
```jsonl
{"target": "登录按钮", "x": 850, "y": 520, "feedback": "confirmed"}
{"target": "提交按钮", "x": 900, "y": 600, "feedback": "confirmed"}
```

---

## 🔧 使用方式

### 方式 1：完全自动（推荐）

```bash
# 主程序运行
python ai_gui_simple.py click "登录按钮"

# 标注器后台监听（如果启用）
python annotation_simple.py enable
```

### 方式 2：手动标注

```python
from annotation_simple import get_collector

collector = get_collector()
collector.log_from_result(
    target="登录按钮",
    result={'x': 850, 'y': 520, 'confidence': 0.95},
    feedback="confirmed"
)
```

### 方式 3：日志解析

```bash
# 运行主程序，输出到日志
python ai_gui_simple.py click "按钮" > output.log

# 标注器解析日志
python annotation_simple.py parse output.log
```

---

## 📈 数据质量

### 自动标记高质量

```python
def is_high_quality(annotation):
    # 高置信度 + 用户确认
    if annotation['confidence'] >= 0.9 and annotation['feedback'] == 'confirmed':
        return True
    
    # 用户修正
    if annotation['feedback'] == 'corrected':
        return True
    
    return False
```

### 导出高质量数据

```bash
# 只导出高质量标注
python annotation_simple.py export --min-confidence 0.9 training.jsonl
```

---

## 🔐 隐私保护

### 默认设置

```python
# 默认关闭标注
enabled = False

# 用户主动启用
AI_GUI_ANNOTATION=true
```

### 数据脱敏

```python
def anonymize(data):
    # 不存储截图
    del data['screenshot']
    
    # 模糊位置（可选）
    data['x'] = round(data['x'] / 10) * 10
    
    return data
```

### 用户控制

```bash
# 查看状态
python annotation_simple.py status

# 导出数据
python annotation_simple.py export my_data.jsonl

# 删除数据
rm ~/.openclaw/ai-gui/annotations.db
```

---

## 🎯 最佳实践

### 开发阶段

```bash
# 启用标注，收集数据
AI_GUI_ANNOTATION=true python ai_gui_simple.py click "按钮"

# 定期导出
python annotation_simple.py export weekly_data.jsonl
```

### 生产阶段

```bash
# 关闭标注，保护隐私
python ai_gui_simple.py click "按钮"
```

### 贡献数据

```bash
# 匿名贡献
AI_GUI_ANNOTATION=true AI_GUI_CONTRIBUTE=true python ai_gui_simple.py
```

---

## 💡 总结

**设计哲学：**

1. ✅ **主程序简洁** - 核心功能不依赖标注
2. ✅ **标注独立** - 可选模块，随时禁用
3. ✅ **透明收集** - 用户无感知但可控制
4. ✅ **逐渐披露** - 从基础到高级

**数据价值：**

```
每次交互 → 标注数据 → 模型优化 → 更好体验
```

**隐私优先：**

```
默认关闭 → 用户选择 → 本地存储 → 可删除
```

---

_简洁而不简单，透明而有价值_ 🦞✨

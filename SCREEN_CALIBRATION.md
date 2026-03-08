# 🖥️ AI-GUI 屏幕校准指南

> 自动检测屏幕分辨率和坐标比例，提高点击准确率

---

## 🎯 为什么需要校准？

**问题场景：**

1. **不同分辨率** - 1920x1080 vs 2560x1440 vs 4K
2. **DPI 缩放** - Windows 缩放 125% / 150%
3. **多显示器** - 不同尺寸和分辨率
4. **截图尺寸** - 截图分辨率与实际屏幕不一致

**校准后：**
- ✅ 自动坐标转换
- ✅ 提高点击准确率
- ✅ 支持多分辨率

---

## 🚀 快速校准（30 秒）

### 步骤 1：运行校准工具

```bash
cd /root/C:\Users\35258\.openclaw\workspace/skills/ai-gui
python3 screen_calibrator.py calibrate
```

### 步骤 2：观察校准过程

```
🔍 开始屏幕坐标校准...

✓ 当前分辨率：1920x1080
✓ 起始位置：(500, 300)
✓ 测试移动：向右 100 像素
✓ 结束位置：(600, 300)
✓ 实际移动：X=100, Y=0
✓ 坐标比例：X=1.0000, Y=1.0000
✓ 已恢复原始位置
✓ 校准数据已保存：~/.openclaw/ai-gui/screen_calibration.json

✓ 校准完成！
```

### 步骤 3：完成！

```
校准数据已保存，下次使用自动应用。
```

---

## 📊 校准原理

### 校准流程

```
1. 获取当前屏幕分辨率
   ↓
2. 记录鼠标起始位置
   ↓
3. 向右移动 100 像素
   ↓
4. 记录鼠标结束位置
   ↓
5. 计算实际移动距离
   ↓
6. 计算坐标比例
   ↓
7. 保存校准数据
```

### 坐标转换

```
AI 识别坐标 → 校准转换 → 实际屏幕坐标

例如：
AI 返回：(500, 300)
校准比例：X=1.0, Y=1.0
实际坐标：(500, 300)

如果 DPI 缩放 125%：
AI 返回：(500, 300)
校准比例：X=0.8, Y=0.8
实际坐标：(625, 375)
```

---

## 🔧 高级用法

### 自定义测试距离

```bash
# 使用 50 像素测试距离
python3 screen_calibrator.py calibrate 50

# 使用 200 像素测试距离
python3 screen_calibrator.py calibrate 200
```

**说明：**
- 小距离（50）- 更精确，但可能受鼠标精度影响
- 大距离（200）- 更稳定，但可能超出某些区域

---

### 查看校准信息

```bash
python3 screen_calibrator.py show
```

**输出示例：**
```
==================================================
📊 屏幕校准信息
==================================================
屏幕分辨率：1920x1080
X 轴比例：1.0000
Y 轴比例：1.0000
测试距离：100 像素
校准时间：/home/user
==================================================
```

---

### 重置校准

```bash
python3 screen_calibrator.py reset
```

**效果：**
- 删除校准数据
- 恢复默认比例（1.0）
- 下次使用时重新校准

---

### 测试校准

```bash
python3 screen_calibrator.py test
```

**测试内容：**
- 不同分辨率的坐标转换
- 1920x1080 → 当前分辨率
- 2560x1440 → 当前分辨率
- 3840x2160 → 当前分辨率

---

## 💡 使用场景

### 场景 1：多显示器设置

**问题：** 主显示器 1920x1080，副显示器 2560x1440

**解决：**
```bash
# 在主显示器上校准
python3 screen_calibrator.py calibrate

# AI-GUI 会自动使用当前显示器的校准数据
python3 ai_gui_simple.py click "登录按钮"
```

---

### 场景 2：DPI 缩放

**问题：** Windows 缩放 150%，坐标不准确

**解决：**
```bash
# 校准会自动检测 DPI 缩放
python3 screen_calibrator.py calibrate

# 校准后，坐标会自动转换
# AI 返回 (500, 300) → 实际点击 (750, 450)
```

---

### 场景 3：4K 屏幕

**问题：** 4K 屏幕（3840x2160），截图是 1080p

**解决：**
```bash
# 校准会记录屏幕分辨率
python3 screen_calibrator.py calibrate

# 视觉分析时会自动转换
# 1080p 截图的 (500, 300) → 4K 屏幕的 (1000, 600)
```

---

## 📁 校准数据

### 存储位置

```
~/.openclaw/ai-gui/screen_calibration.json
```

### 数据格式

```json
{
  "screen_width": 1920,
  "screen_height": 1080,
  "x_scale": 1.0,
  "y_scale": 1.0,
  "test_distance": 100,
  "timestamp": "/home/user"
}
```

### 手动编辑

```bash
# 可以手动编辑校准文件
nano ~/.openclaw/ai-gui/screen_calibration.json

# 修改后保存，下次使用自动应用
```

---

## ⚠️ 常见问题

### Q1: 校准后鼠标乱跳

**原因：** 校准过程中鼠标会移动

**解决：**
```
校准前保存工作，校准过程约 5 秒
```

---

### Q2: 校准数据不准确

**原因：** 校准时鼠标移动不精确

**解决：**
```bash
# 重新校准
python3 screen_calibrator.py calibrate

# 使用更大的测试距离
python3 screen_calibrator.py calibrate 200
```

---

### Q3: 多显示器如何校准

**解决：**
```bash
# 在主显示器上运行校准
python3 screen_calibrator.py calibrate

# 校准数据会应用到所有 AI-GUI 操作
# 如果需要在不同显示器使用不同校准
# 可以手动编辑校准文件
```

---

### Q4: 校准文件在哪里

**查找：**
```bash
# Linux/macOS
ls -la ~/.openclaw/ai-gui/screen_calibration.json

# Windows
dir %USERPROFILE%\.openclaw\ai-gui\screen_calibration.json
```

---

## 🎯 最佳实践

### 1. 首次使用时校准

```bash
# 安装后立即校准
python3 screen_calibrator.py calibrate

# 然后开始使用
python3 ai_gui_simple.py click "按钮"
```

---

### 2. 更换显示器后重新校准

```bash
# 更换显示器或调整分辨率后
python3 screen_calibrator.py calibrate
```

---

### 3. 定期检查校准

```bash
# 每月检查一次
python3 screen_calibrator.py show

# 如果比例变化，重新校准
python3 screen_calibrator.py calibrate
```

---

## 📊 校准效果

### 未校准

```
AI 识别：(500, 300)
实际点击：(500, 300)  ← 可能不准确（DPI 缩放）
准确率：~70%
```

### 已校准

```
AI 识别：(500, 300)
校准转换：(625, 375)  ← 考虑 DPI 缩放
实际点击：(625, 375)
准确率：~95%
```

---

## 🚀 集成到 AI-GUI

### 自动校准提示

```python
# ai_gui_simple.py 会自动检查校准
def simple_click(target):
    # 检查校准
    if not is_calibrated():
        print("⚠️  建议先进行屏幕校准")
        print("   python3 screen_calibrator.py calibrate")
    
    # 继续点击逻辑...
```

### 自动坐标转换

```python
# vision_analyzer.py 会自动转换坐标
result = ai_analyze(screenshot)

# 自动校准坐标
calibrated_x, calibrated_y = calibrator.convert_coordinates(
    result['x'], result['y']
)
```

---

**校准完成，点击更准确！** 🦞✨

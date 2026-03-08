#!/usr/bin/env python3
"""
ai-gui - 简洁版主程序
核心：AI 识别 + 人机协同
标注：独立模块，透明收集
"""

import pyautogui
import sys
import json

# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

# 置信度阈值
CONFIDENCE_HIGH = 0.9
CONFIDENCE_MEDIUM = 0.7


def simple_click(target_description: str, auto_confirm: bool = False) -> bool:
    """
    简单点击 - 主功能
    
    Args:
        target_description: 目标描述（如"登录按钮"）
        auto_confirm: 自动确认（测试用）
    
    Returns:
        是否成功
    """
    print(f"🔍 识别：{target_description}")
    
    # 0. 检查屏幕校准
    try:
        from screen_calibrator import get_calibrator
        calibrator = get_calibrator()
        calibration = calibrator.load_calibration()
        
        # 如果是首次使用，提示校准
        if calibration.get('x_scale') == 1.0 and calibration.get('y_scale') == 1.0:
            print(f"⚠️  建议先进行屏幕校准以获得更准确的结果")
            print(f"   运行：python3 screen_calibrator.py calibrate")
            print(f"")
    except:
        pass  # 校准可选，不影响使用
    
    # 1. 截图
    screenshot = pyautogui.screenshot()
    
    # 2. AI 识别（调用大模型）
    result = ai_find(target_description, screenshot)
    
    if not result or not result.get('found'):
        print(f"✗ 未找到")
        return False
    
    confidence = result.get('confidence', 0)
    x, y = result['x'], result['y']
    
    # 3. 人机协同决策
    if confidence >= CONFIDENCE_HIGH:
        # 高置信度：直接执行
        print(f"✓ 点击 ({x}, {y})")
        pyautogui.click(x, y)
        return True
    
    elif confidence >= CONFIDENCE_MEDIUM:
        # 中置信度：执行 + 通知
        print(f"⚠️  点击 ({x}, {y}) [置信度 {confidence*100:.0f}%]")
        pyautogui.click(x, y)
        return True
    
    else:
        # 低置信度：需要确认
        if auto_confirm:
            print(f"❓ 点击 ({x}, {y}) [置信度 {confidence*100:.0f}%]")
            pyautogui.click(x, y)
            return True
        
        print(f"❓ 确认：{target_description} 在 ({x}, {y}) [置信度 {confidence*100:.0f}%]")
        choice = input("是否执行？(y/n): ").strip().lower()
        
        if choice == 'y':
            pyautogui.click(x, y)
            return True
        else:
            print("✗ 已取消")
            return False


def ai_find(target: str, screenshot) -> dict:
    """
    AI 识别目标
    
    调用视觉分析模块
    """
    from vision_analyzer import ai_find as vision_ai_find
    return vision_ai_find(target, screenshot)


# ========== 命令行接口 ==========

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("AI-GUI - AI 驱动的桌面控制")
        print("")
        print("用法：python ai_gui.py <命令> [目标]")
        print("")
        print("命令:")
        print("  click <目标>     点击目标")
        print("  test             测试")
        print("")
        print("示例:")
        print('  python ai_gui.py click "登录按钮"')
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    try:
        if cmd == 'click':
            target = ' '.join(sys.argv[2:])
            auto = '--auto' in sys.argv
            success = simple_click(target, auto)
            sys.exit(0 if success else 1)
        
        elif cmd == 'test':
            print("测试模式")
            simple_click("测试按钮", auto_confirm=True)
        
        else:
            print(f"未知命令：{cmd}")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n已中止")
        sys.exit(0)
    except Exception as e:
        print(f"错误：{e}")
        sys.exit(1)

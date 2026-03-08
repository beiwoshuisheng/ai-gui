#!/usr/bin/env python3
"""
ai-gui - 屏幕坐标校准模块
自动检测屏幕分辨率和坐标比例
"""

import pyautogui
import json
from pathlib import Path
from typing import Tuple, Dict


class ScreenCalibrator:
    """屏幕坐标校准器"""
    
    def __init__(self):
        """初始化校准器"""
        self.calibration_file = Path.home() / ".openclaw" / "ai-gui" / "screen_calibration.json"
        self.calibration_data = None
        
    def get_screen_size(self) -> Tuple[int, int]:
        """获取当前屏幕分辨率"""
        width, height = pyautogui.size()
        return (width, height)
    
    def calibrate(self, test_distance: int = 100) -> Dict:
        """
        自动校准屏幕坐标
        
        Args:
            test_distance: 测试移动距离（像素），默认 100
        
        Returns:
            校准数据
        """
        print("🔍 开始屏幕坐标校准...")
        print("")
        
        # 1. 获取当前屏幕分辨率
        current_width, current_height = self.get_screen_size()
        print(f"✓ 当前分辨率：{current_width}x{current_height}")
        
        # 2. 获取当前鼠标位置
        start_x, start_y = pyautogui.position()
        print(f"✓ 起始位置：({start_x}, {start_y})")
        
        # 3. 向右移动 test_distance 像素
        print(f"✓ 测试移动：向右 {test_distance} 像素")
        pyautogui.move(test_distance, 0, duration=0.5)
        
        # 4. 获取新位置
        end_x, end_y = pyautogui.position()
        print(f"✓ 结束位置：({end_x}, {end_y})")
        
        # 5. 计算实际移动距离
        actual_move_x = end_x - start_x
        actual_move_y = end_y - start_y
        
        print(f"✓ 实际移动：X={actual_move_x}, Y={actual_move_y}")
        
        # 6. 计算比例
        x_scale = actual_move_x / test_distance if test_distance > 0 else 1.0
        y_scale = 1.0  # Y 轴通常准确
        
        print(f"✓ 坐标比例：X={x_scale:.4f}, Y={y_scale:.4f}")
        
        # 7. 恢复原始位置
        pyautogui.moveTo(start_x, start_y, duration=0.3)
        print(f"✓ 已恢复原始位置")
        
        # 8. 构建校准数据
        calibration_data = {
            "screen_width": current_width,
            "screen_height": current_height,
            "x_scale": x_scale,
            "y_scale": y_scale,
            "test_distance": test_distance,
            "timestamp": str(Path.home())
        }
        
        # 9. 保存校准数据
        self.save_calibration(calibration_data)
        
        print("")
        print("✓ 校准完成！")
        print("")
        
        return calibration_data
    
    def save_calibration(self, data: Dict):
        """保存校准数据到文件"""
        # 确保目录存在
        self.calibration_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存
        with open(self.calibration_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ 校准数据已保存：{self.calibration_file}")
    
    def load_calibration(self) -> Dict:
        """加载校准数据"""
        if self.calibration_data:
            return self.calibration_data
        
        if self.calibration_file.exists():
            try:
                with open(self.calibration_file, 'r', encoding='utf-8') as f:
                    self.calibration_data = json.load(f)
                    print(f"✓ 已加载校准数据")
                    return self.calibration_data
            except Exception as e:
                print(f"⚠️  加载校准数据失败：{e}")
        
        # 返回默认值
        width, height = self.get_screen_size()
        default_data = {
            "screen_width": width,
            "screen_height": height,
            "x_scale": 1.0,
            "y_scale": 1.0,
            "test_distance": 100
        }
        print(f"⚠️  使用默认校准数据")
        return default_data
    
    def convert_coordinates(self, x: int, y: int, from_resolution: str = None) -> Tuple[int, int]:
        """
        转换坐标到当前屏幕
        
        Args:
            x: X 坐标
            y: Y 坐标
            from_resolution: 源分辨率（如 "1920x1080"）
        
        Returns:
            (new_x, new_y)
        """
        # 加载校准数据
        calibration = self.load_calibration()
        
        current_width = calibration["screen_width"]
        current_height = calibration["screen_height"]
        x_scale = calibration["x_scale"]
        y_scale = calibration["y_scale"]
        
        # 如果指定了源分辨率，进行分辨率转换
        if from_resolution:
            try:
                src_width, src_height = map(int, from_resolution.split('x'))
                
                # 计算相对位置
                rel_x = x / src_width
                rel_y = y / src_height
                
                # 转换到目标分辨率
                new_x = int(rel_x * current_width)
                new_y = int(rel_y * current_height)
                
                print(f"✓ 分辨率转换：{from_resolution} → {current_width}x{current_height}")
                print(f"  原始坐标：({x}, {y})")
                print(f"  转换坐标：({new_x}, {new_y})")
                
                return (new_x, new_y)
            except Exception as e:
                print(f"⚠️  分辨率转换失败：{e}")
        
        # 应用坐标比例校正
        new_x = int(x / x_scale)
        new_y = int(y / y_scale)
        
        if from_resolution:
            print(f"✓ 坐标校正：({x}, {y}) → ({new_x}, {new_y})")
        
        return (new_x, new_y)
    
    def reset_calibration(self):
        """重置校准数据"""
        if self.calibration_file.exists():
            self.calibration_file.unlink()
            print("✓ 校准数据已重置")
        else:
            print("✓ 已经是默认校准")
        
        self.calibration_data = None
    
    def show_calibration_info(self):
        """显示校准信息"""
        calibration = self.load_calibration()
        
        print("")
        print("=" * 50)
        print("📊 屏幕校准信息")
        print("=" * 50)
        print(f"屏幕分辨率：{calibration['screen_width']}x{calibration['screen_height']}")
        print(f"X 轴比例：{calibration['x_scale']:.4f}")
        print(f"Y 轴比例：{calibration['y_scale']:.4f}")
        print(f"测试距离：{calibration['test_distance']} 像素")
        
        if 'timestamp' in calibration:
            print(f"校准时间：{calibration['timestamp']}")
        
        print("=" * 50)
        print("")


# ========== 全局校准器实例 ==========

_calibrator = None

def get_calibrator() -> ScreenCalibrator:
    """获取全局校准器实例"""
    global _calibrator
    if _calibrator is None:
        _calibrator = ScreenCalibrator()
    return _calibrator


def calibrate_screen(test_distance: int = 100) -> Dict:
    """校准屏幕坐标"""
    return get_calibrator().calibrate(test_distance)


def convert_coords(x: int, y: int, from_resolution: str = None) -> Tuple[int, int]:
    """转换坐标"""
    return get_calibrator().convert_coordinates(x, y, from_resolution)


def show_calibration():
    """显示校准信息"""
    return get_calibrator().show_calibration_info()


# ========== 命令行接口 ==========

if __name__ == '__main__':
    import sys
    
    print("🦞 AI-GUI 屏幕坐标校准工具")
    print("=" * 50)
    print("")
    
    if len(sys.argv) < 2:
        print("用法：python3 screen_calibrator.py <命令>")
        print("")
        print("命令:")
        print("  calibrate [距离]  校准屏幕（可选：测试距离）")
        print("  show             显示校准信息")
        print("  reset            重置校准")
        print("  test             测试校准")
        print("")
        print("示例:")
        print("  python3 screen_calibrator.py calibrate 100")
        print("  python3 screen_calibrator.py show")
        sys.exit(0)
    
    cmd = sys.argv[1]
    calibrator = ScreenCalibrator()
    
    try:
        if cmd == 'calibrate':
            distance = int(sys.argv[2]) if len(sys.argv) > 2 else 100
            calibrator.calibrate(distance)
        
        elif cmd == 'show':
            calibrator.show_calibration_info()
        
        elif cmd == 'reset':
            calibrator.reset_calibration()
        
        elif cmd == 'test':
            print("测试坐标转换...")
            print("")
            
            # 测试不同分辨率的坐标转换
            test_cases = [
                (500, 300, "1920x1080"),
                (800, 600, "2560x1440"),
                (1000, 500, "3840x2160"),
            ]
            
            for x, y, from_res in test_cases:
                new_x, new_y = calibrator.convert_coordinates(x, y, from_res)
                print(f"  {from_res} ({x}, {y}) → ({new_x}, {new_y})")
            
            print("")
            print("✓ 测试完成")
        
        else:
            print(f"未知命令：{cmd}")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  已中止")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

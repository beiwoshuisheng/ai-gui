#!/usr/bin/env python3
"""
ai-gui - 视觉分析模块
调用 OpenClaw 大模型 API 进行屏幕识别
"""

import requests
import base64
from io import BytesIO
from typing import Dict, Optional


class VisionAnalyzer:
    """视觉分析器"""
    
    def __init__(self, api_endpoint: str = None):
        """
        Args:
            api_endpoint: OpenClaw 视觉 API 端点
        """
        # 从独立配置文件读取（不影响 OpenClaw 主配置）
        from vision_config import get_vision_config
        config = get_vision_config()
        
        # 使用配置
        self.model = config.get('model', 'qwen-vl-max')
        self.api_key = config.get('api_key', '')
        self.timeout = config.get('timeout', 10000) / 1000  # 转换为秒
        
        # API 端点
        if api_endpoint:
            self.api_endpoint = api_endpoint
        else:
            base_url = config.get('base_url', 'https://coding.dashscope.aliyuncs.com/v1')
            endpoint = config.get('endpoint', '/api/v1/vision/analyze')
            self.api_endpoint = base_url.rstrip('/') + endpoint
    
    def screenshot_to_base64(self, screenshot) -> str:
        """将截图转换为 Base64"""
        buffered = BytesIO()
        screenshot.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode()
    
    def analyze(self, target: str, screenshot) -> Optional[Dict]:
        """
        分析截图，找到目标元素
        
        Args:
            target: 目标描述（如"登录按钮"）
            screenshot: PIL Image 对象
        
        Returns:
            识别结果：{'found': bool, 'x': int, 'y': int, 'confidence': float}
        """
        # 获取截图尺寸
        screenshot_width, screenshot_height = screenshot.size
        
        # 转换为 Base64
        image_b64 = self.screenshot_to_base64(screenshot)
        
        # 构建提示词
        system_prompt = """你是一个专业的桌面 UI 分析助手。请分析这张屏幕截图，找到指定的 UI 元素。

**输出格式要求（必须严格遵守）：**

```json
{
    "found": true 或 false,
    "x": 整数（0-屏幕宽度）,
    "y": 整数（0-屏幕高度）,
    "width": 整数（元素宽度，可选）,
    "height": 整数（元素高度，可选）,
    "confidence": 0.0-1.0 的数字,
    "element_type": "button/input/text/link/icon/other",
    "description": "简短描述看到的元素"
}
```

**重要规则：**
1. 只输出 JSON，不要任何其他文字
2. 坐标必须是整数
3. confidence 必须基于你的判断（0.0-1.0）
4. 如果没找到，found=false，x/y 设为 -1
"""
        
        user_prompt = f'请在截图中找到："{target}"'
        
        # 调用 API
        try:
            response = requests.post(
                self.api_endpoint,
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt, "image": image_b64}
                    ]
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', '{}')
                
                # 解析 JSON 输出
                import json
                parsed_result = json.loads(answer)
                
                # 坐标校准（如果识别成功）
                if parsed_result.get('found') and 'x' in parsed_result and 'y' in parsed_result:
                    from screen_calibrator import get_calibrator
                    calibrator = get_calibrator()
                    
                    # 转换坐标到实际屏幕
                    calibrated_x, calibrated_y = calibrator.convert_coordinates(
                        parsed_result['x'],
                        parsed_result['y']
                    )
                    
                    parsed_result['x'] = calibrated_x
                    parsed_result['y'] = calibrated_y
                    parsed_result['calibrated'] = True
                
                return parsed_result
            else:
                print(f"API 调用失败：{response.status_code}")
                return None
        
        except requests.exceptions.ConnectionError:
            print("⚠️  无法连接到视觉 API，请检查网关是否运行")
            print(f"端点：{self.api_endpoint}")
            return None
        
        except Exception as e:
            print(f"视觉分析失败：{e}")
            return None
    
    def test_connection(self) -> bool:
        """测试 API 连接"""
        try:
            response = requests.get(
                self.api_endpoint.replace('/analyze', '/status'),
                timeout=5
            )
            return response.status_code == 200
        except:
            return False


# ========== 简化的 API 调用函数 ==========

_analyzer = None

def ai_find(target: str, screenshot) -> Dict:
    """
    AI 识别目标（简化接口）
    
    Args:
        target: 目标描述
        screenshot: PIL Image 对象
    
    Returns:
        识别结果
    """
    global _analyzer
    if _analyzer is None:
        _analyzer = VisionAnalyzer()
    
    result = _analyzer.analyze(target, screenshot)
    
    if result is None:
        # API 调用失败，返回默认值
        return {
            'found': False,
            'x': -1,
            'y': -1,
            'confidence': 0,
            'error': 'API 调用失败，请检查网关配置'
        }
    
    return result


def set_vision_api(endpoint: str, api_key: str = ''):
    """
    配置视觉 API
    
    Args:
        endpoint: API 端点
        api_key: API 密钥（可选）
    """
    global _analyzer
    _analyzer = VisionAnalyzer(endpoint)
    if api_key:
        _analyzer.api_key = api_key


def test_vision_api() -> bool:
    """测试视觉 API 连接"""
    global _analyzer
    if _analyzer is None:
        _analyzer = VisionAnalyzer()
    return _analyzer.test_connection()


# ========== 命令行测试 ==========

if __name__ == '__main__':
    import sys
    
    print("视觉分析模块测试")
    print("=" * 50)
    
    # 测试连接
    print("测试 API 连接...")
    if test_vision_api():
        print("✓ API 连接正常")
    else:
        print("✗ API 连接失败")
        print("")
        print("请检查:")
        print("1. OpenClaw 网关是否运行")
        print("2. API 端点是否正确")
        print("3. 网络连接是否正常")
        print("")
        print("配置方法:")
        print("  export OPENCLAW_API_ENDPOINT=http://localhost:18789/api/v1/vision/analyze")
        print("  export OPENCLAW_API_KEY=your_api_key")
    
    sys.exit(0)

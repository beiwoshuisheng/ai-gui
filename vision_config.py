#!/usr/bin/env python3
"""
ai-gui - 视觉 API 配置（独立版）
不修改 OpenClaw 主配置，独立管理视觉 API
"""

import os
from pathlib import Path

# 配置文件路径
CONFIG_DIR = Path.home() / ".openclaw" / "ai-gui"
CONFIG_FILE = CONFIG_DIR / "vision_config.json"


def get_vision_config():
    """
    获取视觉 API 配置
    
    优先级：
    1. 环境变量
    2. 独立配置文件
    3. 默认值
    """
    import json
    
    # 默认配置
    default_config = {
        "enabled": True,
        "model": "qwen-vl-max",
        "provider": "bailian",
        "base_url": "https://coding.dashscope.aliyuncs.com/v1",
        "api_key": "",
        "timeout": 10000,
        "endpoint": "/api/v1/vision/analyze"
    }
    
    # 1. 从环境变量读取（最高优先级）
    env_config = {
        "enabled": os.getenv('AI_GUI_VISION_ENABLED', 'true').lower() == 'true',
        "model": os.getenv('AI_GUI_VISION_MODEL', default_config['model']),
        "provider": os.getenv('AI_GUI_VISION_PROVIDER', default_config['provider']),
        "base_url": os.getenv('AI_GUI_VISION_BASE_URL', default_config['base_url']),
        "api_key": os.getenv('AI_GUI_VISION_API_KEY', default_config['api_key']),
        "timeout": int(os.getenv('AI_GUI_VISION_TIMEOUT', default_config['timeout'])),
        "endpoint": os.getenv('AI_GUI_VISION_ENDPOINT', default_config['endpoint'])
    }
    
    # 如果环境变量设置了 API Key，直接返回
    if env_config['api_key']:
        return env_config
    
    # 2. 从独立配置文件读取
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                # 合并配置（环境变量优先）
                return {**default_config, **file_config, **env_config}
        except Exception as e:
            print(f"⚠️  读取配置文件失败：{e}")
    
    # 3. 返回默认配置
    return default_config


def save_vision_config(config):
    """保存配置到独立文件"""
    import json
    
    # 确保目录存在
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    # 保存配置
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 配置已保存：{CONFIG_FILE}")


def setup_vision_api():
    """交互式配置视觉 API"""
    import json
    
    print("🦞 AI-GUI 视觉 API 配置")
    print("=" * 50)
    print("")
    print("说明：")
    print("- 配置保存在独立文件中，不影响 OpenClaw 主配置")
    print("- 配置文件位置：~/.openclaw/ai-gui/vision_config.json")
    print("")
    
    # 获取当前配置
    current_config = get_vision_config()
    
    print("当前配置：")
    for key, value in current_config.items():
        if key == 'api_key' and value:
            value = "***" + value[-8:] if len(value) > 8 else "***"
        print(f"  {key}: {value}")
    print("")
    
    # 询问是否修改
    choice = input("是否修改配置？(y/n): ").strip().lower()
    if choice != 'y':
        print("✓ 使用当前配置")
        return current_config
    
    print("")
    print("请输入新配置（直接回车使用默认值）：")
    print("")
    
    # 交互式配置
    new_config = {}
    new_config['model'] = input(f"模型名称 [{current_config['model']}]: ").strip() or current_config['model']
    new_config['provider'] = input(f"提供商 [{current_config['provider']}]: ").strip() or current_config['provider']
    new_config['base_url'] = input(f"API 基础 URL [{current_config['base_url']}]: ").strip() or current_config['base_url']
    
    api_key = input("API Key: ").strip()
    if api_key:
        new_config['api_key'] = api_key
    else:
        new_config['api_key'] = current_config['api_key']
    
    new_config['timeout'] = int(input(f"超时时间 (毫秒) [{current_config['timeout']}]: ").strip() or current_config['timeout'])
    new_config['endpoint'] = input(f"API 端点 [{current_config['endpoint']}]: ").strip() or current_config['endpoint']
    new_config['enabled'] = True
    
    # 保存配置
    save_vision_config(new_config)
    
    print("")
    print("✓ 配置完成！")
    print("")
    print("使用方式：")
    print("  1. 环境变量（临时）:")
    print("     export AI_GUI_VISION_API_KEY=your_key")
    print("")
    print("  2. 配置文件（永久）:")
    print(f"     编辑：{CONFIG_FILE}")
    print("")
    
    return new_config


def test_vision_connection():
    """测试视觉 API 连接"""
    import requests
    
    config = get_vision_config()
    
    print("🔍 测试视觉 API 连接...")
    print("")
    print(f"模型：{config['model']}")
    print(f"提供商：{config['provider']}")
    print(f"API URL: {config['base_url']}")
    print("")
    
    if not config['api_key']:
        print("⚠️  未配置 API Key")
        print("")
        print("请运行以下命令配置：")
        print("  python3 vision_config.py setup")
        print("")
        print("或设置环境变量：")
        print("  export AI_GUI_VISION_API_KEY=your_api_key")
        return False
    
    # 测试连接
    try:
        # 尝试调用 API（简单测试）
        test_url = config['base_url'].rstrip('/') + '/models'
        headers = {
            'Authorization': f"Bearer {config['api_key']}"
        }
        
        response = requests.get(test_url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            print("✓ API 连接正常")
            return True
        elif response.status_code == 401:
            print("✗ API Key 无效")
            return False
        else:
            print(f"⚠️  API 响应：{response.status_code}")
            return True  # 连接成功，但可能有其他问题
    
    except requests.exceptions.ConnectionError:
        print("✗ 无法连接到 API 服务器")
        print("请检查网络连接和 API URL")
        return False
    
    except Exception as e:
        print(f"⚠️  测试失败：{e}")
        return True  # 可能是网络问题，不一定是配置问题


# ========== 命令行接口 ==========

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("AI-GUI 视觉 API 配置工具")
        print("")
        print("用法：python3 vision_config.py <命令>")
        print("")
        print("命令:")
        print("  setup    交互式配置")
        print("  show     显示当前配置")
        print("  test     测试 API 连接")
        print("  reset    重置为默认配置")
        print("")
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == 'setup':
        setup_vision_api()
    
    elif cmd == 'show':
        config = get_vision_config()
        print("当前视觉 API 配置：")
        print("")
        for key, value in config.items():
            if key == 'api_key' and value:
                value = "***" + value[-8:] if len(value) > 8 else "***"
            print(f"  {key}: {value}")
    
    elif cmd == 'test':
        success = test_vision_connection()
        sys.exit(0 if success else 1)
    
    elif cmd == 'reset':
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
            print("✓ 配置已重置为默认值")
        else:
            print("✓ 已经是默认配置")
    
    else:
        print(f"未知命令：{cmd}")
        sys.exit(1)

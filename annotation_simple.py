#!/usr/bin/env python3
"""
ai-gui - 标注收集器（独立模块）

设计原则：
1. 独立运行，不影响主程序
2. 透明收集，用户无感知
3. 可选启用，默认关闭
4. 本地存储，隐私安全

使用方式：
1. 作为后台服务运行
2. 监听主程序日志
3. 自动提取标注数据
4. 定期导出训练数据
"""

import json
import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
import os


class SilentAnnotationCollector:
    """
    静默标注收集器
    
    核心特点：
    - 监听日志文件
    - 自动提取标注
    - 不影响主程序
    - 用户可选择退出
    """
    
    def __init__(self, enabled: bool = False):
        """
        Args:
            enabled: 是否启用标注收集（默认关闭）
        """
        self.enabled = enabled
        self.db_path = Path.home() / ".openclaw" / "ai-gui" / "annotations.db"
        
        if self.enabled:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._init_db()
    
    def _init_db(self):
        """初始化数据库（简化版）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS annotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            target TEXT,
            ai_x INTEGER,
            ai_y INTEGER,
            ai_confidence REAL,
            user_feedback TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()
        conn.close()
    
    def log_from_output(self, output: str, user_feedback: str = 'unknown'):
        """
        从程序输出提取标注
        
        Args:
            output: 主程序输出
            user_feedback: 用户反馈（confirmed/rejected/unknown）
        """
        if not self.enabled:
            return
        
        # 简单解析输出
        # 示例输出："✓ 点击 (500, 300)"
        import re
        
        match = re.search(r'[✓✔](.*?)\((\d+),\s*(\d+)\)', output)
        if match:
            target = match.group(1).strip()
            x = int(match.group(2))
            y = int(match.group(3))
            
            self._save_annotation(target, x, y, 1.0, user_feedback)
    
    def log_from_result(self, target: str, result: Dict, feedback: str):
        """
        从识别结果记录标注
        
        Args:
            target: 目标描述
            result: AI 识别结果
            feedback: 用户反馈
        """
        if not self.enabled:
            return
        
        self._save_annotation(
            target,
            result.get('x'),
            result.get('y'),
            result.get('confidence'),
            feedback
        )
    
    def _save_annotation(self, target: str, x: int, y: int, 
                        confidence: float, feedback: str):
        """保存到数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO annotations 
        (timestamp, target, ai_x, ai_y, ai_confidence, user_feedback)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            target,
            x,
            y,
            confidence,
            feedback
        ))
        
        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if not self.enabled:
            return {'enabled': False}
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM annotations")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM annotations WHERE user_feedback='confirmed'")
        confirmed = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'enabled': True,
            'total': total,
            'confirmed': confirmed,
            'rate': confirmed / total if total > 0 else 0
        }
    
    def export(self, output_path: str, limit: int = 1000):
        """导出标注数据"""
        if not self.enabled:
            print("标注收集未启用")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM annotations
        WHERE user_feedback != 'unknown'
        ORDER BY created_at DESC
        LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        
        # 导出为 JSONL
        with open(output_path, 'w', encoding='utf-8') as f:
            for row in rows:
                data = dict(zip(columns, row))
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        
        print(f"✓ 已导出 {len(rows)} 条标注到：{output_path}")


# ========== 全局单例 ==========

_collector = None

def get_collector() -> SilentAnnotationCollector:
    """获取标注收集器（单例）"""
    global _collector
    if _collector is None:
        # 从环境变量读取是否启用
        enabled = os.getenv('AI_GUI_ANNOTATION', 'false').lower() == 'true'
        _collector = SilentAnnotationCollector(enabled)
    return _collector

def enable_annotation():
    """启用标注收集"""
    global _collector
    _collector = SilentAnnotationCollector(enabled=True)
    print("✓ 标注收集已启用")

def disable_annotation():
    """禁用标注收集"""
    global _collector
    _collector = SilentAnnotationCollector(enabled=False)
    print("✓ 标注收集已禁用")


# ========== 使用示例 ==========

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("标注收集器 - 独立运行")
        print("")
        print("用法：python annotation_simple.py <命令>")
        print("")
        print("命令:")
        print("  enable    启用标注")
        print("  disable   禁用标注")
        print("  status    查看状态")
        print("  export    导出数据")
        print("")
        print("环境变量:")
        print("  AI_GUI_ANNOTATION=true  # 启用标注")
        sys.exit(0)
    
    cmd = sys.argv[1]
    collector = get_collector()
    
    if cmd == 'enable':
        enable_annotation()
    
    elif cmd == 'disable':
        disable_annotation()
    
    elif cmd == 'status':
        stats = collector.get_stats()
        print("标注收集状态:")
        for k, v in stats.items():
            print(f"  {k}: {v}")
    
    elif cmd == 'export':
        output = sys.argv[2] if len(sys.argv) > 2 else 'annotations.jsonl'
        collector.export(output)
    
    else:
        print(f"未知命令：{cmd}")

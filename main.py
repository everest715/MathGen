#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数学题目生成器 - 主入口文件

这是一个基于PyQt6的数学题目生成器应用程序的主入口文件。
该程序可以生成各种类型的数学练习题并保存为PDF格式。

功能特点：
- 支持多种运算类型：加法、减法、乘法、除法、混合运算
- 可自定义数字范围和结果范围
- 支持自定义页数、列数和每列题目数
- 可调节字号大小
- 智能调整行间距
- 自动生成PDF文件

使用方法：
    python main.py

作者: AI Assistant
版本: 2.0
日期: 2024
"""

import sys
import os

# 添加当前目录到Python路径，确保能够导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from math_ui import main as ui_main
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保 math_ui.py 和 math_engine.py 文件存在于同一目录中")
    sys.exit(1)

def main():
    """主函数 - 应用程序入口点"""
    print("启动数学题目生成器...")
    print("功能：生成各种类型的数学练习题并保存为PDF")
    print("支持的运算类型：加法、减法、乘法、除法、混合运算")
    print("-" * 50)
    
    try:
        # 启动UI界面
        ui_main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"程序运行时出错: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数学题目生成器 - 向后兼容入口文件

为了保持向后兼容性，这个文件现在导入并启动新的模块化版本。
建议使用 main.py 作为新的入口点。
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from math_ui import MathProblemGeneratorUI
    from PyQt6.QtWidgets import QApplication
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保安装了所需的依赖包：pip install -r requirements.txt")
    sys.exit(1)

# 为了向后兼容，保留原来的类名
MathProblemGenerator = MathProblemGeneratorUI

def main():
    """主函数 - 向后兼容的入口点"""
    app = QApplication(sys.argv)
    window = MathProblemGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
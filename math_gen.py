#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数学题目生成器 - 命令行版本

功能：
- 生成加减法填空题
- 支持多列布局
- 导出为PDF格式

使用方法：
python math_gen.py
"""

import random
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Preformatted, BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.units import inch

def generate_expression():
    """生成单个数学表达式
    
    返回格式：
    - 加法：(     ) + b = a 或 b + (     ) = a
    - 减法：(     ) - b = a-b 或 a - (     ) = b
    
    确保减法结果为正数
    """
    operator = random.choice(['+', '-'])
    a = random.randint(1, 99)
    b = random.randint(1, 99)
    a, b = max(a, b), min(a, b)  # 确保a >= b，减法结果为正

    # 随机选择要加括号的位置（0-左边 1-右边）
    bracket_pos = random.choice([0, 1])

    if bracket_pos == 0:
        if operator == "+":
            return f'(     ) + {b} = {a}'  # 使用中文全角空格
        else:
            return f'(     ) - {b} = {a - b}'
    else:
        if operator == "+":
            return f'{b} + (     ) = {a}'
        else:
            return f'{a} - (     ) = {b}'

def create_pdf(filename, problems, cols=3):
    """创建PDF文档
    
    参数：
        filename: 输出文件名
        problems: 题目列表
        cols: 每页列数（默认3列）
    """
    # 自定义多列文档模板
    class MultiColumnDocTemplate(BaseDocTemplate):
        def __init__(self, filename, cols=3, **kwargs):
            super().__init__(filename, **kwargs)
            self.cols = cols
            
        def build(self, flowables, **kwargs):
            """构建多列布局"""
            frame_width = (self.width) / self.cols
            frames = []
            for i in range(self.cols):
                left = self.leftMargin + i * frame_width
                width = frame_width - 12  # 留出间距
                frame = Frame(left, self.bottomMargin, 
                            width, self.height, 
                            leftPadding=6, rightPadding=6)
                frames.append(frame)
            
            template = PageTemplate(frames=frames)
            self.addPageTemplates([template])
            super().build(flowables, **kwargs)

    # 创建PDF文档
    doc = MultiColumnDocTemplate(filename, cols=cols,
                               pagesize=letter,
                               rightMargin=48, leftMargin=48,
                               topMargin=36, bottomMargin=18)

    # 设置样式
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontSize = 16  # 默认字号
    style.leading = style.fontSize + 6  # 行间距 = 字号 + 6

    # 添加内容
    content = []
    for i, prob in enumerate(problems):
        p = Preformatted(f"{prob}", style)
        content.append(p)

    doc.build(content)

if __name__ == '__main__':
    pages = 10
    cols = 4
    perCol = 25
    count = pages * perCol * cols
    problems = [generate_expression() for _ in range(count)]

    # 保存txt
    # with open('math_problems.txt', 'w', encoding='utf-8') as f:
    #     f.write('\n'.join([f'{p}' for i, p in enumerate(problems)]))

    # 生成PDF
    create_pdf('math_problems.pdf', problems, cols)
    print(f'\n已生成{count}道题目到 math_problems.pdf')
#!/usr/bin/env python3
"""精确简化注释的工具"""

import re

def simplify_math_engine():
    """简化 math_engine.py 中的函数注释"""
    with open('f:\\Downloads\\六一\\MathGen\\math_engine.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 定义要替换的冗长 docstring 映射
    replacements = {
        # __init__
        '''    def __init__(self, 
                 min_number: Optional[int] = None, 
                 max_number: Optional[int] = None, 
                 min_result: Optional[int] = None, 
                 max_result: Optional[int] = None, 
                 allow_right_bracket: bool = False) -> None:
        """初始化数学引擎
        
        负责生成各种数学运算表达式，包括加法、减法、乘法、除法和混合运算。
        支持自定义数字范围和结果范围，以及括号位置控制。
        
        Args:
            min_number: 最小数字值（默认值：Constants.DEFAULT_MIN_NUMBER）
            max_number: 最大数字值（默认值：Constants.DEFAULT_MAX_NUMBER）
            min_result: 最小结果值（默认值：Constants.DEFAULT_MIN_RESULT）
            max_result: 最大结果值（默认值：Constants.DEFAULT_MAX_RESULT）
            allow_right_bracket: 是否允许括号出现在等号右边（默认值：False）
        """''':
        '''    def __init__(self, 
                 min_number: Optional[int] = None, 
                 max_number: Optional[int] = None, 
                 min_result: Optional[int] = None, 
                 max_result: Optional[int] = None, 
                 allow_right_bracket: bool = False) -> None:
        """初始化数学引擎。"""''',
        
        # _normalize_ranges
        '''    def _normalize_ranges(self) -> None:
        """规范化范围，确保最小值不大于最大值"""''':
        '''    def _normalize_ranges(self) -> None:
        """规范化范围。"""''',
        
        # update_ranges
        '''    def update_ranges(self, 
                     min_number: int, 
                     max_number: int, 
                     min_result: int, 
                     max_result: int, 
                     allow_right_bracket: Optional[bool] = None) -> None:
        """更新数字和结果范围
        
        Args:
            min_number: 新的最小数字值
            max_number: 新的最大数字值
            min_result: 新的最小结果值
            max_result: 新的最大结果值
            allow_right_bracket: 是否允许等号右边括号（可选）
        """''':
        '''    def update_ranges(self, 
                     min_number: int, 
                     max_number: int, 
                     min_result: int, 
                     max_result: int, 
                     allow_right_bracket: Optional[bool] = None) -> None:
        """更新数字和结果范围。"""''',
    }
    
    # 应用替换
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    with open('f:\\Downloads\\六一\\MathGen\\math_engine_simplified_comments.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return len(content.split('\n'))

def main():
    # 简化 math_engine.py
    line_count = simplify_math_engine()
    print(f"简化完成，共 {line_count} 行")
    
    # 测试
    try:
        exec(open('f:\\Downloads\\六一\\MathGen\\math_engine_simplified_comments.py', 'r', encoding='utf-8').read())
        from math_engine import MathEngine
        m = MathEngine()
        result = m.generate_expression()
        print(f"✓ 测试通过: {result}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")

if __name__ == "__main__":
    main()
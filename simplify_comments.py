#!/usr/bin/env python3
"""简化函数注释的工具"""

import re

def simplify_math_engine():
    """简化 math_engine.py 中的函数注释"""
    with open('f:\Downloads\六一\MathGen\math_engine.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简化 __init__
    content = re.sub(
        r'    def __init__\(self[^)]*\) -> None:\n    """[^"]*?初始化[^"]*?"""',
        r'    def __init__(self, min_number=None, max_number=None, min_result=None, max_result=None, allow_right_bracket=False) -> None:\n    """初始化数学引擎。"""',
        content,
        flags=re.MULTILINE
    )
    
    # 简化 _normalize_ranges
    content = re.sub(
        r'    def _normalize_ranges\(self\) -> None:\n    """[^"]*?规范化[^"]*?"""',
        r'    def _normalize_ranges(self) -> None:\n    """规范化范围，确保最小值不大于最大值。"""',
        content
    )
    
    # 简化 update_ranges
    content = re.sub(
        r'    def update_ranges\(self[^)]*\) -> None:\n    """[^"]*?更新[^"]*?"""',
        r'    def update_ranges(self, min_number: int, max_number: int, min_result: int, max_result: int, allow_right_bracket: Optional[bool] = None) -> None:\n    """更新数字和结果范围。"""',
        content
    )
    
    # 简化 _generate_safe_random
    content = re.sub(
        r'    def _generate_safe_random\(self[^)]*\) -> int:\n    """安全地生成随机数[^"]*?"""',
        r'    def _generate_safe_random(self, min_val: int, max_val: int, fallback_min: int = 1, fallback_max: int = 10) -> int:\n    """安全生成随机数，范围无效时使用备用值。"""',
        content
    )
    
    # 简化验证方法
    content = re.sub(
        r'    def _is_valid_expression_result\(self[^)]*\) -> bool:\n    """[^"]*?验证[^"]\x7f结果[^"]*?"""',
        r'    def _is_valid_expression_result(self, result: int) -> bool:\n    """验证表达式结果在有效范围内。"""',
        content
    )
    
    # 简化生成表达式的方法
    content = re.sub(
        r'    def generate_expression\(self[^)]*\) -> str:\n    """生成单个数学表达式[^"]*?"""',
        r'    def generate_expression(self, num_count: int = 2, has_multiply: bool = False, has_divide: bool = False) -> str:\n    """生成数学表达式，支持2-3个数字和四则运算。"""',
        content
    )
    
    with open('f:\Downloads\六一\MathGen\math_engine_simplified_comments.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return content

def simplify_main():
    """简化 main.py 中的函数注释"""
    with open('f:\Downloads\六一\MathGen\main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简化 MathProblemGenerator 类注释
    content = re.sub(
        r'class MathProblemGenerator:\n    """[^"]*?数学题生成器[^"]*?"""',
        r'class MathProblemGenerator:\n    """数学题生成器主类。"""',
        content
    )
    
    # 简化 __init__
    content = re.sub(
        r'    def __init__\(self\) -> None:\n    """初始化[^"]*?"""',
        r'    def __init__(self) -> None:\n    """初始化数学题生成器。"""',
        content
    )
    
    # 简化 run
    content = re.sub(
        r'    def run\(self\) -> None:\n    """运行[^"]*?"""',
        r'    def run(self) -> None:\n    """运行应用程序。"""',
        content
    )
    
    # 简化 generate_problems
    content = re.sub(
        r'    def generate_problems\(self\) -> None:\n    """[^"]*?生成数学题目[^"]*?"""',
        r'    def generate_problems(self) -> None:\n    """生成数学题目主流程。"""',
        content
    )
    
    # 简化 validate_settings
    content = re.sub(
        r'    def _validate_settings\(self[^)]*\) -> tuple:\n    """[^"]*?验证[^"]*?"""',
        r'    def _validate_settings(self, settings: Dict) -> tuple:\n    """验证用户设置有效性。"""',
        content
    )
    
    with open('f:\Downloads\六一\MathGen\main_simplified_comments.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return content

if __name__ == "__main__":
    print("简化 math_engine.py...")
    simplify_math_engine()
    print("简化 main.py...")
    simplify_main()
    print("完成！")
    
    # 比较行数
    import os
    orig_math = len(open('f:\Downloads\六一\MathGen\math_engine.py', 'r', encoding='utf-8').readlines())
    simp_math = len(open('f:\Downloads\六一\MathGen\math_engine_simplified_comments.py', 'r', encoding='utf-8').readlines())
    
    orig_main = len(open('f:\Downloads\六一\MathGen\main.py', 'r', encoding='utf-8').readlines())
    simp_main = len(open('f:\Downloads\六一\MathGen\main_simplified_comments.py', 'r', encoding='utf-8').readlines())
    
    print(f"\nmath_engine.py: {orig_math} -> {simp_math} 行 (减少 {orig_math - simp_math})")
    print(f"main.py: {orig_main} -> {simp_main} 行 (减少 {orig_main - simp_main})")

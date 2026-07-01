#!/usr/bin/env python3
"""Simplified math_engine.py with unified 3-number expression generation"""

import random
from typing import Optional, Tuple, Dict, Any, Callable
from constants import Constants


class MathEngine:
    """数学表达式生成引擎
    
    负责生成各种数学运算表达式，包括加法、减法、乘法、除法和混合运算。
    支持自定义数字范围和结果范围，以及括号位置控制。
    """
    
    def __init__(self, 
                 min_number: Optional[int] = None, 
                 max_number: Optional[int] = None, 
                 min_result: Optional[int] = None, 
                 max_result: Optional[int] = None, 
                 allow_left_bracket: bool = False,
                 allow_right_bracket: bool = False,
                 reduce_round_tens: bool = False) -> None:
        """初始化数学引擎
        
        Args:
            min_number: 最小数字值（默认值：Constants.DEFAULT_MIN_NUMBER）
            max_number: 最大数字值（默认值：Constants.DEFAULT_MAX_NUMBER）
            min_result: 最小结果值（默认值：Constants.DEFAULT_MIN_RESULT）
            max_result: 最大结果值（默认值：Constants.DEFAULT_MAX_RESULT）
            allow_left_bracket: 是否允许括号出现在等号左边（默认值：False）
            allow_right_bracket: 是否允许括号出现在等号右边（默认值：False）
            reduce_round_tens: 是否减少整十数字在加减法中的出现（默认值：False）
        """
        self.min_number: int = min_number or Constants.DEFAULT_MIN_NUMBER
        self.max_number: int = max_number or Constants.DEFAULT_MAX_NUMBER
        self.min_result: int = min_result or Constants.DEFAULT_MIN_RESULT
        self.max_result: int = max_result or Constants.DEFAULT_MAX_RESULT
        self.allow_left_bracket: bool = allow_left_bracket
        self.allow_right_bracket: bool = allow_right_bracket
        self.reduce_round_tens: bool = reduce_round_tens
        
        # 确保范围合理
        self._normalize_ranges()
    
    def _normalize_ranges(self) -> None:
        """规范化范围。"""
        if self.min_number > self.max_number:
            self.min_number, self.max_number = self.max_number, self.min_number
        if self.min_result > self.max_result:
            self.min_result, self.max_result = self.max_result, self.min_result
    
    def update_ranges(self, 
                     min_number: int, 
                     max_number: int, 
                     min_result: int, 
                     max_result: int, 
                     allow_left_bracket: Optional[bool] = None,
                     allow_right_bracket: Optional[bool] = None,
                     reduce_round_tens: Optional[bool] = None) -> None:
        """更新数字和结果范围。"""
        self.min_number = min_number
        self.max_number = max_number
        self.min_result = min_result
        self.max_result = max_result
        if allow_left_bracket is not None:
            self.allow_left_bracket = allow_left_bracket
        if allow_right_bracket is not None:
            self.allow_right_bracket = allow_right_bracket
        if reduce_round_tens is not None:
            self.reduce_round_tens = reduce_round_tens
        
        self._normalize_ranges()
    
    def _generate_safe_random(self, min_val: int, max_val: int, 
                             fallback_min: int = 1, fallback_max: int = 10) -> int:
        """安全地生成随机数，如果范围无效则使用备用范围"""
        try:
            if min_val <= max_val:
                return random.randint(min_val, max_val)
            else:
                return random.randint(fallback_min, fallback_max)
        except ValueError:
            return random.randint(fallback_min, fallback_max)
    
    def _generate_random_with_round_tens_control(self, min_val: int, max_val: int, 
                                                reduce_round_tens: bool = False,
                                                max_attempts: int = 10) -> int:
        """生成随机数，可选择性地减少整十数字的出现概率
        
        Args:
            min_val: 最小值
            max_val: 最大值
            reduce_round_tens: 是否减少整十数字（10、20、30等）的出现
            max_attempts: 最大尝试次数
            
        Returns:
            生成的随机数
        """
        for attempt in range(max_attempts):
            value = self._generate_safe_random(min_val, max_val)
            
            # 如果不需要减少整十数字，直接返回
            if not reduce_round_tens:
                return value
            
            # 检查是否为整十数字（10、20、30等）
            if value % 10 == 0 and value != 0:
                # 以50%的概率重新生成（可以根据需要调整这个概率）
                if random.random() < 0.5 and attempt < max_attempts - 1:
                    continue
            
            return value
        
        # 如果多次尝试后仍然得到整十数字，就接受它
        return value
    
    def _is_valid_expression_result(self, result: int) -> bool:
        """验证表达式结果是否在有效范围内"""
        return self.min_result <= result <= self.max_result
    
    def _is_valid_number(self, number: int) -> bool:
        """验证数字是否在有效范围内"""
        return self.min_number <= number <= self.max_number
    
    def _generate_multiplication_pair(self) -> Tuple[int, int]:
        """生成乘法因子对，确保结果不超过99"""
        a = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, 
                          Constants.MAX_MULTIPLICATION_FACTOR)
        b = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, 
                          Constants.MAX_MULTIPLICATION_FACTOR)
        return a, b
    
    def _generate_division_pair(self) -> Tuple[int, int, int]:
        """生成除法数对，确保能整除"""
        divisor = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, 
                                Constants.MAX_MULTIPLICATION_FACTOR)
        quotient = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, 
                                 Constants.MAX_MULTIPLICATION_FACTOR)
        dividend = divisor * quotient
        return dividend, divisor, quotient
    
    def _find_factors(self, number: int) -> list[Tuple[int, int]]:
        """找到数字在指定范围内的因子对"""
        factors = []
        min_factor = Constants.MIN_MULTIPLICATION_FACTOR
        max_factor = Constants.MAX_MULTIPLICATION_FACTOR
        
        for i in range(min_factor, max_factor + 1):
            if number % i == 0:
                j = number // i
                if min_factor <= j <= max_factor:
                    factors.append((i, j))
        
        return factors
    
    def _generate_bracket_expression(self, a: int, op: str, b: int, 
                                    result: str, bracket_pos: Optional[int] = None) -> str:
        """生成带括号的表达式"""
        if bracket_pos is None:
            # 根据括号设置决定可选的括号位置
            available_positions = []
            if self.allow_left_bracket:
                available_positions.extend([0, 1])
            available_positions.append(2)  # 无括号（填空结果）始终可用
            if self.allow_right_bracket:
                available_positions.append(3)
            
            bracket_pos = random.choice(available_positions)
        
        expressions = {
            0: f'(     ) {op} {b} = {result}',      # 左操作数括号
            1: f'{a} {op} (     ) = {result}',      # 右操作数括号
            2: f'{a} {op} {b} =',                   # 等号左边无括号（填空结果）
            3: f'{a} {op} {b} = (     )'            # 等号右边括号（在allow_right_bracket=True时）
        }
        
        return expressions[bracket_pos]
    
    def _safe_generate_expression(self, generator_func: Callable[[], str], 
                                 max_attempts: int = Constants.MAX_GENERATION_ATTEMPTS) -> str:
        """安全地生成表达式，带重试机制"""
        for attempt in range(max_attempts):
            try:
                result = generator_func()
                if result:
                    return result
            except Exception:
                continue
        
        # 如果所有尝试都失败，返回默认表达式
        return Constants.DEFAULT_PROBLEM
    
    def generate_expression(self, num_count: int = 2, 
                           has_multiply: bool = False, 
                           has_divide: bool = False) -> str:
        """生成单个数学表达式"""
        if num_count not in [2, 3]:
            raise ValueError("num_count必须是2或3")
        
        if num_count == 2:
            return self._generate_two_number_expression(has_multiply, has_divide)
        else:
            return self._generate_three_number_expression(has_multiply, has_divide)
    
    def _generate_two_number_expression(self, has_multiply: bool, has_divide: bool) -> str:
        """生成两个数的表达式"""
        # 随机选择运算类型
        operation_choices = []
        if has_divide:
            operation_choices.append('÷')
        if has_multiply:
            operation_choices.append('x')
        operation_choices.extend(['+', '-'])  # 总是包含加减法
        
        operation = random.choice(operation_choices)
        
        # 使用统一的生成方法
        operation_methods: Dict[str, Callable[[], str]] = {
            '÷': self._generate_division_expression,
            'x': self._generate_multiplication_expression,
            '+': self._generate_addition_expression,
            '-': self._generate_subtraction_expression
        }
        
        method = operation_methods.get(operation)
        return method() if method else Constants.DEFAULT_PROBLEM
    
    def _generate_division_expression(self) -> str:
        """生成除法表达式(带余数)"""
        # 除数在数字范围内，且不超过9
        divisor = self._generate_safe_random(
            max(2, self.min_number), 
            min(self.max_number, 9)
        )
        
        # 计算商的有效范围
        max_quotient = min(
            self.max_result, 
            9, 
            self.max_number // divisor if divisor > 0 else 9
        )
        min_quotient = max(1, self.min_result)
        
        # 确保范围有效
        if min_quotient > max_quotient:
            quotient = self._generate_safe_random(1, min(9, self.max_result))
        else:
            quotient = self._generate_safe_random(min_quotient, max_quotient)
        
        # 余数小于除数
        remainder = self._generate_safe_random(0, divisor - 1)
        dividend = quotient * divisor + remainder
        
        # 确保被除数在数字范围内
        if dividend > self.max_number:
            max_quotient = min(9, self.max_number // divisor)
            quotient = self._generate_safe_random(1, max_quotient)
            remainder = self._generate_safe_random(0, min(divisor - 1, self.max_number - quotient * divisor))
            dividend = quotient * divisor + remainder

        expression = self._generate_bracket_expression(
            dividend, '÷', divisor, f'{quotient}...{remainder}'
        )
        return expression
    
    def _generate_multiplication_expression(self) -> str:
        """生成乘法表达式"""
        # 生成两个乘数，确保结果在范围内
        a = self._generate_safe_random(
            max(2, self.min_number), 
            min(self.max_number, 9)
        )
        
        max_b = min(
            self.max_number, 
            self.max_result // a if a > 0 else self.max_number,
            9  # 限制乘数范围
        )
        b = self._generate_safe_random(max(2, self.min_number), max_b)
        result = a * b
        
        # 确保结果在范围内
        if not self._is_valid_expression_result(result):
            # 重新生成较小的数
            a = self._generate_safe_random(2, min(5, self.max_number, 9))
            max_b_for_result = min(
                self.max_result // a if a > 0 else self.max_number,
                self.max_number,
                9
            )
            b = self._generate_safe_random(2, max_b_for_result)
            result = a * b
            
        expression = self._generate_bracket_expression(a, 'x', b, result)
        return expression
    
    def _generate_addition_expression(self) -> str:
        """生成加法表达式（优化分布）"""
        # 先随机选择结果，确保结果在范围内均匀分布
        min_result_possible = max(self.min_result, self.min_number * 2)
        max_result_possible = min(self.max_result, self.max_number * 2)
        
        # 确保范围有效
        if min_result_possible > max_result_possible:
            min_result_possible = self.min_result
            max_result_possible = self.max_result
        
        result = self._generate_random_with_round_tens_control(
            min_result_possible, max_result_possible, self.reduce_round_tens
        )
        
        # 根据结果生成a，确保a在有效范围内
        min_a = max(self.min_number, result - self.max_number)
        max_a = min(self.max_number, result - self.min_number)
        
        # 确保范围有效
        if min_a > max_a:
            # 如果无法满足条件，调整结果
            result = self._generate_random_with_round_tens_control(
                max(self.min_result, self.min_number * 2),
                min(self.max_result, self.max_number * 2),
                self.reduce_round_tens
            )
            min_a = max(self.min_number, result - self.max_number)
            max_a = min(self.max_number, result - self.min_number)
        
        # 如果仍然无效，使用备用方案
        if min_a > max_a:
            a = self._generate_random_with_round_tens_control(
                self.min_number, self.max_number, self.reduce_round_tens
            )
            b = self._generate_random_with_round_tens_control(
                self.min_number, self.max_number, self.reduce_round_tens
            )
            result = a + b
        else:
            a = self._generate_random_with_round_tens_control(
                min_a, max_a, self.reduce_round_tens
            )
            b = result - a
        
        expression = self._generate_bracket_expression(a, '+', b, result)
        return expression
    
    def _generate_subtraction_expression(self) -> str:
        """生成减法表达式（优化分布）"""
        # 先随机选择结果，确保结果在范围内均匀分布
        result = self._generate_random_with_round_tens_control(
            self.min_result, self.max_result, self.reduce_round_tens
        )
        
        # 生成减数b，确保被减数a在数字范围内
        max_b_possible = self.max_number - result
        
        if max_b_possible < self.min_number:
            # 如果当前结果太大，重新生成较小的结果
            result = self._generate_random_with_round_tens_control(
                self.min_result, 
                min(self.max_result, self.max_number - self.min_number),
                self.reduce_round_tens
            )
            max_b_possible = self.max_number - result
        
        # 生成减数b
        if max_b_possible >= self.min_number:
            b = self._generate_random_with_round_tens_control(
                self.min_number, max_b_possible, self.reduce_round_tens
            )
        else:
            # 如果无法满足条件，使用最小值
            b = self.min_number
        
        # 计算被减数a
        a = result + b
        
        # 验证结果
        if not (self.min_number <= a <= self.max_number and self.min_result <= result <= self.max_result):
            # 如果验证失败，使用备用方案
            a = self._generate_random_with_round_tens_control(
                self.min_number, self.max_number, self.reduce_round_tens
            )
            b = self._generate_random_with_round_tens_control(
                self.min_number, a, self.reduce_round_tens
            )
            result = a - b
                
        expression = self._generate_bracket_expression(a, '-', b, result)
        return expression
    
    def _generate_three_number_expression(self, has_multiply: bool, has_divide: bool) -> str:
        """生成三个数的表达式（统一处理所有运算符组合）"""
        max_attempts = Constants.MAX_GENERATION_ATTEMPTS
        
        for _ in range(max_attempts):
            # 选择运算符
            op1, op2 = self._select_operators(has_multiply, has_divide)
            
            # 生成数值
            a, b, c = self._generate_three_numbers(op1, op2)
            
            # 计算结果
            try:
                result = self._calculate_expression((a, b, c), (op1, op2))
                
                # 验证结果
                if self._is_valid_expression_result(result):
                    # 根据括号设置决定可选的括号位置
                    available_positions = []
                    if self.allow_left_bracket:
                        available_positions.extend([0, 1, 2])
                    available_positions.append(3)  # 无括号（填空结果）始终可用
                    if self.allow_right_bracket:
                        available_positions.append(4)
                    
                    bracket_pos = random.choice(available_positions)
                    
                    expressions = {
                        0: f'(     ) {op1} {b} {op2} {c} = {result}',
                        1: f'{a} {op1} (     ) {op2} {c} = {result}',
                        2: f'{a} {op1} {b} {op2} (     ) = {result}',
                        3: f'{a} {op1} {b} {op2} {c} =',
                        4: f'{a} {op1} {b} {op2} {c} = (     )'
                    }
                    return expressions[bracket_pos]
            except (ZeroDivisionError, ValueError):
                continue
        
        return Constants.DEFAULT_PROBLEM
    
    def _select_operators(self, has_multiply: bool, has_divide: bool) -> tuple[str, str]:
        """选择两个运算符"""
        # 构建可用运算符池
        available_ops = ['+', '-']
        if has_multiply:
            available_ops.append('x')
        if has_divide:
            available_ops.append('÷')
        
        # 随机选择两个运算符
        op1 = random.choice(available_ops)
        op2 = random.choice(available_ops)
        
        return op1, op2
    
    def _generate_three_numbers(self, op1: str, op2: str) -> tuple[int, int, int]:
        """为给定的运算符生成三个合适的数"""
        # 优先处理乘除法（需要确保整除、结果范围等）
        if op1 in ['x', '÷']:
            return self._generate_for_mixed_first(op1, op2)
        elif op2 in ['x', '÷']:
            return self._generate_for_mixed_second(op1, op2)
        else:
            # 纯加减法
            return self._generate_for_add_sub_only(op1, op2)
    
    def _generate_for_mixed_first(self, op1: str, op2: str) -> tuple[int, int, int]:
        """处理第一个运算符是乘除法的情况"""
        # 生成第一个运算
        if op1 == 'x':
            a = self._generate_safe_random(2, min(self.max_number, 9))
            b = self._generate_safe_random(2, min(self.max_number, 9))
            temp_result = a * b
        else:  # ÷
            b = self._generate_safe_random(2, min(self.max_number, 9))
            quotient = self._generate_safe_random(1, min(self.max_result, self.max_number // b if b > 0 else 1))
            a = b * quotient
            temp_result = quotient
        
        # 生成第二个运算
        if op2 == '+':
            max_c = min(self.max_number, self.max_result - temp_result)
            c = self._generate_safe_random(self.min_number, max_c)
        else:  # '-'
            max_c = min(self.max_number, temp_result - self.min_result)
            c = self._generate_safe_random(self.min_number, max_c)
        
        return a, b, c
    
    def _generate_for_mixed_second(self, op1: str, op2: str) -> tuple[int, int, int]:
        """处理第二个运算符是乘除法的情况"""
        # 生成第二个运算（乘除法）
        if op2 == 'x':
            b = self._generate_safe_random(2, min(self.max_number, 9))
            c = self._generate_safe_random(2, min(self.max_number, 9))
            temp_result = b * c
        else:  # ÷
            c = self._generate_safe_random(2, min(self.max_number, 9))
            quotient = self._generate_safe_random(1, min(self.max_result, self.max_number // c if c > 0 else 1))
            b = c * quotient
            temp_result = quotient
        
        # 生成第一个运算（加减法）
        if op1 == '+':
            max_a = min(self.max_number, self.max_result - temp_result)
            a = self._generate_safe_random(self.min_number, max_a)
        else:  # '-'
            min_a = max(self.min_number, temp_result + self.min_result)
            a = self._generate_safe_random(min_a, self.max_number)
        
        return a, b, c
    
    def _generate_for_add_sub_only(self, op1: str, op2: str) -> tuple[int, int, int]:
        """处理纯加减法的情况"""
        # 根据运算符生成三个数，确保中间结果和最终结果都为正
        if op1 == '+' and op2 == '+':
            # a + b + c
            a = self._generate_safe_random(self.min_number, min(self.max_number, self.max_result // 3))
            b = self._generate_safe_random(self.min_number, min(self.max_number, (self.max_result - a) // 2))
            c = self._generate_safe_random(self.min_number, min(self.max_number, self.max_result - a - b))
            
        elif op1 == '+' and op2 == '-':
            # a + b - c (确保 a + b > c)
            c = self._generate_safe_random(self.min_number, min(self.max_number, self.max_result - self.min_result))
            temp_sum = self._generate_safe_random(c + self.min_result, min(self.max_result + c, self.max_number * 2))
            a = self._generate_safe_random(self.min_number, min(self.max_number, temp_sum - self.min_number))
            b = temp_sum - a
            if b > self.max_number:
                b = self.max_number
                a = temp_sum - b
                
        elif op1 == '-' and op2 == '+':
            # a - b + c (确保 a > b)
            b = self._generate_safe_random(self.min_number, self.max_number)
            c = self._generate_safe_random(self.min_number, self.max_number)
            min_a = max(self.min_number, b + self.min_result - c if c < self.min_result else b + 1)
            a = self._generate_safe_random(min_a, self.max_number)
            
        else:  # '-' and '-'
            # a - b - c (确保 a > b + c)
            max_bc = self.max_number - self.min_result
            if max_bc < self.min_number * 2:
                total_sub = self._generate_safe_random(self.min_number * 2, min(self.max_number * 2, self.max_result))
            else:
                total_sub = self._generate_safe_random(self.min_number * 2, max_bc)
            
            b = self._generate_safe_random(self.min_number, min(self.max_number, total_sub - self.min_number))
            c = total_sub - b
            if c < self.min_number or c > self.max_number:
                c = self.max_number
                b = total_sub - c
            
            min_a = total_sub + self.min_result
            a = self._generate_safe_random(min_a, self.max_number)
        
        return a, b, c
    
    def _calculate_expression(self, numbers: tuple[int, int, int], 
                            ops: tuple[str, str]) -> int:
        """计算三个数的表达式结果（遵循运算优先级）"""
        a, b, c = numbers
        op1, op2 = ops
        
        # 先计算乘除法
        if op1 in ['x', '÷']:
            if op1 == 'x':
                temp = a * b
            else:
                temp = a // b if b != 0 else 0
            
            if op2 == '+':
                return temp + c
            else:
                return temp - c
        elif op2 in ['x', '÷']:
            if op2 == 'x':
                temp = b * c
            else:
                temp = b // c if c != 0 else 0
            
            if op1 == '+':
                return a + temp
            else:
                return a - temp
        else:
            # 纯加减法
            if op1 == '+':
                result = a + b
            else:
                result = a - b
            
            if op2 == '+':
                return result + c
            else:
                return result - c
#!/usr/bin/env python3
"""数学表达式生成引擎"""

import random
from typing import Optional
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
                 allow_right_bracket: bool = False) -> None:
        """初始化数学引擎"""
        self.min_number: int = min_number or Constants.DEFAULT_MIN_NUMBER
        self.max_number: int = max_number or Constants.DEFAULT_MAX_NUMBER
        self.min_result: int = min_result or Constants.DEFAULT_MIN_RESULT
        self.max_result: int = max_result or Constants.DEFAULT_MAX_RESULT
        self.allow_left_bracket: bool = allow_left_bracket
        self.allow_right_bracket: bool = allow_right_bracket
        self.reduce_round_tens: bool = True
        
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
                     allow_right_bracket: Optional[bool] = None) -> None:
        """更新数字和结果范围。"""
        self.min_number = min_number
        self.max_number = max_number
        self.min_result = min_result
        self.max_result = max_result
        if allow_left_bracket is not None:
            self.allow_left_bracket = allow_left_bracket
        if allow_right_bracket is not None:
            self.allow_right_bracket = allow_right_bracket
        
        self._normalize_ranges()
    
    def _generate_safe_random(self, min_val: int, max_val: int, 
                             fallback_min: int = 2, fallback_max: int = 10) -> int:
        """安全地生成随机数，如果范围无效则使用备用范围"""
        try:
            if min_val <= max_val:
                return random.randint(min_val, max_val)
            return random.randint(fallback_min, fallback_max)
        except ValueError:
            return random.randint(fallback_min, fallback_max)
    
    def _generate_random_with_round_tens_control(self, min_val: int, max_val: int, 
                                                reduce_round_tens: bool = False) -> int:
        """生成随机数，可选择性地减少整十数字的出现概率"""
        value = self._generate_safe_random(min_val, max_val)
        
        if not reduce_round_tens or value == 0 or value % 10 != 0:
            return value
        
        # 整十数字：50% 概率保留，50% 概率替换为附近的非整十数字
        if random.random() < 0.5:
            return value
        
        offset = random.randint(1, 9)
        if random.random() < 0.5:
            offset = -offset
        return max(min_val, min(max_val, value + offset))
    
    def _is_valid_expression_result(self, result: int) -> bool:
        """验证表达式结果是否在有效范围内"""
        return self.min_result <= result <= self.max_result
    
    def _generate_bracket_expression(self, a: int, op: str, b: int, 
                                    result, bracket_pos: Optional[int] = None) -> str:
        """生成带括号的表达式"""
        result = str(result)
        
        if bracket_pos is None:
            available_positions = []
            if self.allow_left_bracket:
                available_positions.extend([0, 1])
            available_positions.append(2)  # 无括号（填空结果）始终可用
            # 右边括号仅用于除法带余数的情况
            if self.allow_right_bracket and op == '÷' and '...' in result:
                available_positions.append(3)
            
            bracket_pos = random.choice(available_positions)
        
        # 位置3：右边括号，仅除法带余数时可用，括号只包商或余数
        if bracket_pos == 3:
            quotient, remainder = result.split('...')
            if random.random() < 0.5:
                return f'{a} {op} {b} = (     )...{remainder}'
            else:
                return f'{a} {op} {b} = {quotient}...(     )'
        
        expressions = {
            0: f'(     ) {op} {b} = {result}',
            1: f'{a} {op} (     ) = {result}',
            2: f'{a} {op} {b} =',
        }
        
        return expressions[bracket_pos]
    
    def generate_expression(self, num_count: int = 3, 
                           has_multiply: bool = False, 
                           has_divide: bool = False) -> str:
        """生成三数运算表达式"""
        max_attempts = Constants.MAX_GENERATION_ATTEMPTS
        
        for _ in range(max_attempts):
            op1, op2 = self._select_operators(has_multiply, has_divide)
            a, b, c = self._generate_three_numbers(op1, op2)
            
            try:
                result = self._calculate_expression((a, b, c), (op1, op2))
                
                if self._is_valid_expression_result(result):
                    available_positions = []
                    if self.allow_left_bracket:
                        available_positions.extend([0, 1, 2])
                    available_positions.append(3)  # 无括号（填空结果）始终可用
                    
                    bracket_pos = random.choice(available_positions)
                    
                    expressions = {
                        0: f'(     ) {op1} {b} {op2} {c} = {result}',
                        1: f'{a} {op1} (     ) {op2} {c} = {result}',
                        2: f'{a} {op1} {b} {op2} (     ) = {result}',
                        3: f'{a} {op1} {b} {op2} {c} =',
                    }
                    return expressions[bracket_pos]
            except (ZeroDivisionError, ValueError):
                continue
        
        return Constants.DEFAULT_PROBLEM
    
    def _generate_division_expression(self) -> str:
        """生成除法表达式(带余数)"""
        divisor = self._generate_safe_random(max(2, self.min_number), self.max_number)
        
        max_quotient = min(
            self.max_result, 
            self.max_number // divisor if divisor > 0 else self.max_result
        )
        min_quotient = max(2, self.min_result)
        
        if min_quotient > max_quotient:
            quotient = self._generate_safe_random(2, self.max_result)
        else:
            quotient = self._generate_safe_random(min_quotient, max_quotient)
        
        remainder = self._generate_safe_random(0, divisor - 1)
        dividend = quotient * divisor + remainder
        
        if dividend > self.max_number:
            max_quotient = self.max_number // divisor
            quotient = self._generate_safe_random(2, max_quotient)
            remainder = self._generate_safe_random(0, min(divisor - 1, self.max_number - quotient * divisor))
            dividend = quotient * divisor + remainder

        result_str = f'{quotient}...{remainder}' if remainder != 0 else str(quotient)
        return self._generate_bracket_expression(dividend, '÷', divisor, result_str)
    
    def _generate_division_no_remainder_expression(self) -> str:
        """生成除法表达式(无余数)"""
        divisor = self._generate_safe_random(max(2, self.min_number), self.max_number)
        
        max_quotient = min(
            self.max_result, 
            self.max_number // divisor if divisor > 0 else self.max_result
        )
        min_quotient = max(2, self.min_result)
        
        if min_quotient > max_quotient:
            quotient = self._generate_safe_random(2, self.max_result)
        else:
            quotient = self._generate_safe_random(min_quotient, max_quotient)
        
        dividend = quotient * divisor
        
        if dividend > self.max_number:
            max_quotient = self.max_number // divisor
            quotient = self._generate_safe_random(2, max_quotient)
            dividend = quotient * divisor

        return self._generate_bracket_expression(dividend, '÷', divisor, str(quotient))
    
    def _generate_multiplication_expression(self) -> str:
        """生成乘法表达式"""
        rt = self.reduce_round_tens
        a = self._generate_random_with_round_tens_control(max(2, self.min_number), self.max_number, rt)
        
        max_b = min(self.max_number, self.max_result // a if a > 0 else self.max_number)
        b = self._generate_random_with_round_tens_control(max(2, self.min_number), max_b, rt)
        result = a * b
        
        if not self._is_valid_expression_result(result):
            a = self._generate_random_with_round_tens_control(2, min(5, self.max_number), rt)
            max_b_for_result = min(
                self.max_result // a if a > 0 else self.max_number,
                self.max_number
            )
            b = self._generate_random_with_round_tens_control(2, max_b_for_result, rt)
            result = a * b
            
        return self._generate_bracket_expression(a, 'x', b, result)
    
    def _generate_addition_expression(self) -> str:
        """生成加法表达式（优化分布）"""
        min_result_possible = max(self.min_result, self.min_number * 2)
        max_result_possible = min(self.max_result, self.max_number * 2)
        
        if min_result_possible > max_result_possible:
            min_result_possible = self.min_result
            max_result_possible = self.max_result
        
        result = self._generate_random_with_round_tens_control(
            min_result_possible, max_result_possible, self.reduce_round_tens
        )
        
        min_a = max(self.min_number, result - self.max_number)
        max_a = min(self.max_number, result - self.min_number)
        
        if min_a > max_a:
            result = self._generate_random_with_round_tens_control(
                max(self.min_result, self.min_number * 2),
                min(self.max_result, self.max_number * 2),
                self.reduce_round_tens
            )
            min_a = max(self.min_number, result - self.max_number)
            max_a = min(self.max_number, result - self.min_number)
        
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
        
        return self._generate_bracket_expression(a, '+', b, result)
    
    def _generate_subtraction_expression(self) -> str:
        """生成减法表达式（优化分布）"""
        result = self._generate_random_with_round_tens_control(
            self.min_result, self.max_result, self.reduce_round_tens
        )
        
        max_b_possible = self.max_number - result
        
        if max_b_possible < self.min_number:
            result = self._generate_random_with_round_tens_control(
                self.min_result, 
                min(self.max_result, self.max_number - self.min_number),
                self.reduce_round_tens
            )
            max_b_possible = self.max_number - result
        
        if max_b_possible >= self.min_number:
            b = self._generate_random_with_round_tens_control(
                self.min_number, max_b_possible, self.reduce_round_tens
            )
        else:
            b = self.min_number
        
        a = result + b
        
        if not (self.min_number <= a <= self.max_number and self.min_result <= result <= self.max_result):
            a = self._generate_random_with_round_tens_control(
                self.min_number, self.max_number, self.reduce_round_tens
            )
            b = self._generate_random_with_round_tens_control(
                self.min_number, a, self.reduce_round_tens
            )
            result = a - b
                
        return self._generate_bracket_expression(a, '-', b, result)
    
    def _select_operators(self, has_multiply: bool, has_divide: bool) -> tuple[str, str]:
        """选择两个运算符"""
        available_ops = ['+', '-']
        if has_multiply:
            available_ops.append('x')
        if has_divide:
            available_ops.append('÷')
        
        return random.choice(available_ops), random.choice(available_ops)
    
    def _generate_three_numbers(self, op1: str, op2: str) -> tuple[int, int, int]:
        """为给定的运算符生成三个合适的数"""
        if op1 in ['x', '÷']:
            return self._generate_for_mixed_first(op1, op2)
        elif op2 in ['x', '÷']:
            return self._generate_for_mixed_second(op1, op2)
        else:
            return self._generate_for_add_sub_only(op1, op2)
    
    def _generate_for_mixed_first(self, op1: str, op2: str) -> tuple[int, int, int]:
        """处理第一个运算符是乘除法的情况"""
        if op1 == 'x':
            a = self._generate_safe_random(2, self.max_number)
            b = self._generate_safe_random(2, min(self.max_number, self.max_result // a if a > 0 else self.max_number))
            temp_result = a * b
        else:  # ÷
            b = self._generate_safe_random(2, self.max_number)
            quotient = self._generate_safe_random(2, min(self.max_result, self.max_number // b if b > 0 else self.max_result))
            a = b * quotient
            temp_result = quotient
        
        if op2 == '+':
            max_c = min(self.max_number, self.max_result - temp_result)
            c = self._generate_random_with_round_tens_control(self.min_number, max_c, self.reduce_round_tens)
        else:
            max_c = min(self.max_number, temp_result - self.min_result)
            c = self._generate_random_with_round_tens_control(self.min_number, max_c, self.reduce_round_tens)
        
        return a, b, c
    
    def _generate_for_mixed_second(self, op1: str, op2: str) -> tuple[int, int, int]:
        """处理第二个运算符是乘除法的情况"""
        if op2 == 'x':
            b = self._generate_safe_random(2, self.max_number)
            c = self._generate_safe_random(2, min(self.max_number, self.max_result // b if b > 0 else self.max_number))
            temp_result = b * c
        else:  # ÷
            c = self._generate_safe_random(2, self.max_number)
            quotient = self._generate_safe_random(2, min(self.max_result, self.max_number // c if c > 0 else self.max_result))
            b = c * quotient
            temp_result = quotient
        
        if op1 == '+':
            max_a = min(self.max_number, self.max_result - temp_result)
            a = self._generate_random_with_round_tens_control(self.min_number, max_a, self.reduce_round_tens)
        else:
            min_a = max(self.min_number, temp_result + self.min_result)
            a = self._generate_random_with_round_tens_control(min_a, self.max_number, self.reduce_round_tens)
        
        return a, b, c
    
    def _generate_for_add_sub_only(self, op1: str, op2: str) -> tuple[int, int, int]:
        """处理纯加减法的情况"""
        rt = self.reduce_round_tens
        if op1 == '+' and op2 == '+':
            a = self._generate_random_with_round_tens_control(self.min_number, min(self.max_number, self.max_result // 3), rt)
            b = self._generate_random_with_round_tens_control(self.min_number, min(self.max_number, (self.max_result - a) // 2), rt)
            c = self._generate_random_with_round_tens_control(self.min_number, min(self.max_number, self.max_result - a - b), rt)
            
        elif op1 == '+' and op2 == '-':
            # a + b - c (确保 a + b > c，且 b != c 避免抵消)
            c = self._generate_random_with_round_tens_control(self.min_number, min(self.max_number, self.max_result - self.min_result), rt)
            temp_sum = self._generate_random_with_round_tens_control(c + self.min_result, min(self.max_result + c, self.max_number * 2), rt)
            a = self._generate_random_with_round_tens_control(self.min_number, min(self.max_number, temp_sum - self.min_number), rt)
            b = temp_sum - a
            if b > self.max_number:
                b = self.max_number
                a = temp_sum - b
            if b == c:
                b = b + 1 if b < self.max_number else b - 1
                a = temp_sum - b
                
        elif op1 == '-' and op2 == '+':
            # a - b + c (确保 a > b，且 b != c 避免抵消)
            b = self._generate_random_with_round_tens_control(self.min_number, self.max_number, rt)
            c = self._generate_random_with_round_tens_control(self.min_number, self.max_number, rt)
            if b == c:
                c = c + 1 if c < self.max_number else c - 1
            min_a = max(self.min_number, b - c + self.min_result if c < b else b + 1)
            a = self._generate_random_with_round_tens_control(min_a, self.max_number, rt)
            
        else:  # '-' and '-'
            # a - b - c (确保 a > b + c)
            max_bc = self.max_number - self.min_result
            if max_bc < self.min_number * 2:
                total_sub = self._generate_random_with_round_tens_control(self.min_number * 2, min(self.max_number * 2, self.max_result), rt)
            else:
                total_sub = self._generate_random_with_round_tens_control(self.min_number * 2, max_bc, rt)
            
            b = self._generate_random_with_round_tens_control(self.min_number, min(self.max_number, total_sub - self.min_number), rt)
            c = total_sub - b
            if c < self.min_number or c > self.max_number:
                c = self.max_number
                b = total_sub - c
            
            min_a = total_sub + self.min_result
            a = self._generate_random_with_round_tens_control(min_a, self.max_number, rt)
        
        return a, b, c
    
    def _calculate_expression(self, numbers: tuple[int, int, int], 
                            ops: tuple[str, str]) -> int:
        """计算三个数的表达式结果（遵循运算优先级）"""
        a, b, c = numbers
        op1, op2 = ops
        
        if op1 in ['x', '÷']:
            temp = a * b if op1 == 'x' else (a // b if b != 0 else 0)
            return temp + c if op2 == '+' else temp - c
        elif op2 in ['x', '÷']:
            temp = b * c if op2 == 'x' else (b // c if c != 0 else 0)
            return a + temp if op1 == '+' else a - temp
        else:
            result = a + b if op1 == '+' else a - b
            return result + c if op2 == '+' else result - c

    # ==================== 巧算方法 ====================

    def generate_clever_expression(self, clever_type: str) -> str:
        """生成巧算表达式"""
        if clever_type == '凑整加减法':
            return random.choice([self._generate_clever_addition, self._generate_clever_subtraction])()
        elif clever_type == '乘法交换律':
            return self._generate_clever_multiplication()
        return Constants.DEFAULT_PROBLEM

    def _generate_clever_addition(self) -> str:
        """生成凑整加法：a + b + c，其中 a + c 凑整十/百"""
        # 随机选择凑整目标：整十或整百
        if random.random() < 0.5:
            # 凑整十
            target = random.randint(self.min_number // 10 + 1, self.max_number // 10) * 10
        else:
            # 凑整百
            target = random.randint(self.min_number // 100 + 1, self.max_number // 100) * 100

        # a 的个位不能为 0
        a = self._generate_safe_random(max(self.min_number, target - self.max_number), min(self.max_number, target - self.min_number))
        if a % 10 == 0:
            a = a + 1 if a < self.max_number else a - 1
        c = target - a

        if not (self.min_number <= c <= self.max_number):
            # 范围不合法，重试
            return self._generate_clever_addition()

        # b 为中间数，确保总和在结果范围内
        min_b = max(self.min_number, self.min_result - target)
        max_b = min(self.max_number, self.max_result - target)

        if min_b > max_b:
            return self._generate_clever_addition()

        b = self._generate_safe_random(min_b, max_b)
        result = target + b

        # 确保前两数相加不为整十数且必须进位
        valid_arrangements = [
            (x, b, y) for x, y in [(a, c), (c, a)]
            if (x + b) % 10 != 0 and (x % 10) + (b % 10) >= 10
        ]
        if not valid_arrangements:
            return self._generate_clever_addition()
        a, b, c = random.choice(valid_arrangements)

        # 选择括号位置
        available_positions = [2]  # 默认无括号
        if self.allow_left_bracket:
            available_positions.extend([0, 1])
        pos = random.choice(available_positions)

        if pos == 0:
            return f'(     ) + {b} + {c} = {result}'
        elif pos == 1:
            return f'{a} + {b} + (     ) = {result}'
        else:
            return f'{a} + {b} + {c} ='

    def _generate_clever_subtraction(self) -> str:
        """生成凑整减法：a - b - c，其中 b+c 凑整 或 a-c 凑整"""
        mode = random.choice(['b_plus_c', 'a_minus_c'])

        if mode == 'b_plus_c':
            # b + c 凑整十/百
            if random.random() < 0.5:
                target = random.randint(self.min_number // 10 + 1, self.max_number // 10) * 10
            else:
                target = random.randint(self.min_number // 100 + 1, self.max_number // 100) * 100

            b = self._generate_safe_random(self.min_number, min(self.max_number, target - self.min_number))
            if b % 10 == 0:
                b = b + 1 if b < self.max_number else b - 1
            c = target - b

            if not (self.min_number <= c <= self.max_number):
                return self._generate_clever_subtraction()

            # a 确保结果为正且在结果范围内
            min_a = max(self.min_number, target + self.min_result)
            max_a = min(self.max_number, target + self.max_result)

            if min_a > max_a:
                return self._generate_clever_subtraction()

            a = self._generate_safe_random(min_a, max_a)
            result = a - target

            # 确保前两数相减不为整十数且必须退位
            valid_arrangements = [
                (a, x, y) for x, y in [(b, c), (c, b)]
                if (a - x) % 10 != 0 and (a % 10) < (x % 10)
            ]
            if not valid_arrangements:
                return self._generate_clever_subtraction()
            a, b, c = random.choice(valid_arrangements)

        else:
            # a - c 凑整十/百
            if random.random() < 0.5:
                target = random.randint(self.min_number // 10 + 1, self.max_number // 10) * 10
            else:
                target = random.randint(self.min_number // 100 + 1, self.max_number // 100) * 100

            c = self._generate_safe_random(self.min_number, min(self.max_number, target - self.min_number))
            if c % 10 == 0:
                c = c + 1 if c < self.max_number else c - 1
            a = target + c

            if not (self.min_number <= a <= self.max_number):
                return self._generate_clever_subtraction()

            # b 确保结果为正且在结果范围内
            min_b = self.min_number
            max_b = min(self.max_number, target - self.min_result)

            if min_b > max_b:
                return self._generate_clever_subtraction()

            b = self._generate_safe_random(min_b, max_b)
            result = target - b

            # 确保前两数相减不为整十数且必须退位
            if (a - b) % 10 == 0 or (a % 10) >= (b % 10):
                return self._generate_clever_subtraction()

        # 选择括号位置
        available_positions = [2]
        if self.allow_left_bracket:
            available_positions.extend([0, 1])
        pos = random.choice(available_positions)

        if pos == 0:
            return f'(     ) - {b} - {c} = {result}'
        elif pos == 1:
            return f'{a} - (     ) - {c} = {result}'
        else:
            return f'{a} - {b} - {c} ='

    def _generate_clever_multiplication(self) -> str:
        """生成乘法交换律：a x b x c，其中一对乘数凑整"""
        # 随机生成 a（2-9，排除整十数）
        a = self._generate_safe_random(2, 9)

        # 找到 b 使得 a * b = 整十或整百，且 a 和 b 都不是整十数
        targets = []
        for t in range(10, self.max_result + 1, 10):
            if t % a == 0:
                b = t // a
                if 2 <= b <= self.max_number and b % 10 != 0:
                    targets.append((b, t))

        if not targets:
            return self._generate_clever_multiplication()

        b, pair_product = random.choice(targets)

        # c 为随意数，确保总结果在结果范围内
        max_c = min(self.max_number, self.max_result // pair_product) if pair_product > 0 else self.max_number
        min_c = max(self.min_number, self.min_result // pair_product) if pair_product > 0 else self.min_number

        if min_c > max_c:
            return self._generate_clever_multiplication()

        c = self._generate_safe_random(min_c, max_c)
        result = pair_product * c

        # 确保前两个数相乘结果不为整十数，避免凑整对出现在前两位
        valid_arrangements = [
            arr for arr in [
                [a, b, c], [a, c, b], [b, a, c], [b, c, a], [c, a, b], [c, b, a]
            ] if arr[0] * arr[1] % 10 != 0
        ]
        if not valid_arrangements:
            return self._generate_clever_multiplication()
        nums = random.choice(valid_arrangements)

        # 选择括号位置
        available_positions = [2]
        if self.allow_left_bracket:
            available_positions.extend([0, 1])
        pos = random.choice(available_positions)

        if pos == 0:
            return f'(     ) x {nums[1]} x {nums[2]} = {result}'
        elif pos == 1:
            return f'{nums[0]} x (     ) x {nums[2]} = {result}'
        else:
            return f'{nums[0]} x {nums[1]} x {nums[2]} ='

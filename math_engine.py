"""数学表达式生成引擎

包含所有数学表达式生成的核心逻辑
"""

import random
from constants import Constants

class MathEngine:
    """数学表达式生成引擎"""
    
    def __init__(self, min_number=None, max_number=None, min_result=None, max_result=None):
        """初始化数学引擎
        
        参数:
            min_number: 最小数字值
            max_number: 最大数字值
            min_result: 最小结果值
            max_result: 最大结果值
        """
        self.min_number = min_number or Constants.DEFAULT_MIN_NUMBER
        self.max_number = max_number or Constants.DEFAULT_MAX_NUMBER
        self.min_result = min_result or Constants.DEFAULT_MIN_RESULT
        self.max_result = max_result or Constants.DEFAULT_MAX_RESULT
        
        # 确保范围合理
        if self.min_number > self.max_number:
            self.min_number, self.max_number = self.max_number, self.min_number
        if self.min_result > self.max_result:
            self.min_result, self.max_result = self.max_result, self.min_result
    
    def update_ranges(self, min_number, max_number, min_result, max_result):
        """更新数字和结果范围"""
        self.min_number = min_number
        self.max_number = max_number
        self.min_result = min_result
        self.max_result = max_result
        
        # 确保范围合理
        if self.min_number > self.max_number:
            self.min_number, self.max_number = self.max_number, self.min_number
        if self.min_result > self.max_result:
            self.min_result, self.max_result = self.max_result, self.min_result
    
    def _generate_safe_random(self, min_val, max_val, fallback_min=1, fallback_max=10):
        """安全地生成随机数，如果范围无效则使用备用范围"""
        try:
            if min_val <= max_val:
                return random.randint(min_val, max_val)
            else:
                return random.randint(fallback_min, fallback_max)
        except ValueError:
            return random.randint(fallback_min, fallback_max)
    
    def _is_valid_expression_result(self, result):
        """验证表达式结果是否在有效范围内"""
        return self.min_result <= result <= self.max_result
    
    def _is_valid_number(self, number):
        """验证数字是否在有效范围内"""
        return self.min_number <= number <= self.max_number
    
    def _generate_multiplication_pair(self):
        """生成乘法因子对，确保结果不超过99"""
        a = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, Constants.MAX_MULTIPLICATION_FACTOR)
        b = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, Constants.MAX_MULTIPLICATION_FACTOR)
        return a, b
    
    def _generate_division_pair(self):
        """生成除法数对，确保能整除"""
        divisor = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, Constants.MAX_MULTIPLICATION_FACTOR)
        quotient = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, Constants.MAX_MULTIPLICATION_FACTOR)
        dividend = divisor * quotient
        return dividend, divisor, quotient
    
    def _find_factors(self, number):
        """找到数字在指定范围内的因子对"""
        factors = []
        for i in range(Constants.MIN_MULTIPLICATION_FACTOR, Constants.MAX_MULTIPLICATION_FACTOR + 1):
            if number % i == 0:
                j = number // i
                if Constants.MIN_MULTIPLICATION_FACTOR <= j <= Constants.MAX_MULTIPLICATION_FACTOR:
                    factors.append((i, j))
        return factors
    
    def _generate_bracket_expression(self, a, op, b, result, bracket_pos=None):
        """生成带括号的表达式"""
        if bracket_pos is None:
            bracket_pos = random.choice([0, 1, 2])
        
        if bracket_pos == 0:
            return f'(     ) {op} {b} = {result}'
        elif bracket_pos == 1:
            return f'{a} {op} (     ) = {result}'
        else:
            return f'{a} {op} {b} ='
    
    def _safe_generate_expression(self, generator_func, max_attempts=Constants.MAX_GENERATION_ATTEMPTS):
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
    
    def generate_expression(self, num_count=2, has_multiply=False, has_divide=False):
        """生成单个数学表达式

        参数：
            num_count: 等号左边数值数量(2或3)
            has_multiply: 是否包含乘法
            has_divide: 是否包含除法
        """
        if num_count == 2:
            return self._generate_two_number_expression(has_multiply, has_divide)
        else:
            return self._generate_three_number_expression(has_multiply, has_divide)

    def _generate_two_number_expression(self, has_multiply, has_divide):
        """生成两个数的表达式"""
        # 随机选择运算类型
        operation_choices = []
        if has_divide:
            operation_choices.append('÷')
        if has_multiply:
            operation_choices.append('x')
        operation_choices.extend(['+', '-'])  # 总是包含加减法
        
        operation = random.choice(operation_choices)
        
        if operation == '÷':
            return self._generate_division_expression()
        elif operation == 'x':
            return self._generate_multiplication_expression()
        elif operation == '+':
            return self._generate_addition_expression()
        else:  # subtract
            return self._generate_subtraction_expression()

    def _generate_division_expression(self):
        """生成除法表达式(带余数)"""
        # 除数在数字范围内
        divisor = random.randint(max(2, self.min_number), min(self.max_number, 9))  # 限制除数不要太大
        # 商在结果范围内
        quotient = random.randint(self.min_result, min(self.max_result, self.max_number // divisor))
        # 余数小于除数
        remainder = random.randint(0, divisor - 1)
        dividend = quotient * divisor + remainder
        
        # 确保被除数在数字范围内
        if dividend > self.max_number:
            dividend = self.max_number
            quotient = dividend // divisor
            remainder = dividend % divisor

        return self._generate_bracket_expression(dividend, '÷', divisor, f'{quotient}...{remainder}')

    def _generate_multiplication_expression(self):
        """生成乘法表达式"""
        # 生成两个乘数，确保结果在范围内
        a = random.randint(max(2, self.min_number), min(self.max_number, 9))  # 限制乘数范围
        max_b = min(self.max_number, self.max_result // a) if a > 0 else self.max_number
        b = random.randint(max(2, self.min_number), min(max_b, 9))
        result = a * b
        
        # 确保结果在范围内
        if result < self.min_result or result > self.max_result:
            # 重新生成较小的数
            a = random.randint(2, min(5, self.max_number))
            b = random.randint(2, min(self.max_result // a, self.max_number))
            result = a * b
            
        return self._generate_bracket_expression(a, 'x', b, result)

    def _generate_addition_expression(self):
        """生成加法表达式"""
        # 生成两个加数，确保和在结果范围内
        a = self._generate_safe_random(self.min_number, self.max_number)
        max_b = min(self.max_number, self.max_result - a)
        if max_b < self.min_number:
            # 如果无法满足条件，调整a
            a = self._generate_safe_random(self.min_number, self.max_result - self.min_number)
            max_b = min(self.max_number, self.max_result - a)
        b = self._generate_safe_random(self.min_number, max_b)
        result = a + b
        
        return self._generate_bracket_expression(a, '+', b, result)

    def _generate_subtraction_expression(self):
        """生成减法表达式(确保结果为正)"""
        # 生成被减数和减数，确保差在结果范围内且为正
        result = self._generate_safe_random(self.min_result, self.max_result)
        b = self._generate_safe_random(self.min_number, self.max_number)
        a = result + b
        
        # 确保被减数在数字范围内
        if a > self.max_number:
            # 调整减数
            max_b = min(self.max_number, self.max_number - result)
            if max_b >= self.min_number:
                b = self._generate_safe_random(self.min_number, max_b)
                a = result + b
            else:
                # 重新生成较小的结果
                result = self._generate_safe_random(self.min_result, min(self.max_result, self.max_number - self.min_number))
                b = self._generate_safe_random(self.min_number, self.max_number - result)
                a = result + b
                
        return self._generate_bracket_expression(a, '-', b, result)

    def _generate_three_number_expression(self, has_multiply, has_divide):
        """生成三个数的表达式"""
        # 确定运算符组合
        operations = []
        
        # 如果选择了乘法或除法，必须包含至少一个乘除法运算符和一个加减法运算符
        if has_multiply or has_divide:
            # 如果包含乘法，添加乘法与加减法的组合
            if has_multiply:
                operations.extend([('x', '+'), ('x', '-'), ('+', 'x'), ('-', 'x')])
            
            # 如果包含除法，添加除法与加减法的组合
            if has_divide:
                operations.extend([('÷', '+'), ('÷', '-'), ('+', '÷'), ('-', '÷')])
        else:
            # 如果没有选择乘法和除法，只生成纯加减法运算
            operations.extend([('+', '+'), ('+', '-'), ('-', '+'), ('-', '-')])
        
        op1, op2 = random.choice(operations)
        
        # 生成数值
        if 'x' in [op1, op2] or '÷' in [op1, op2]:
            return self._generate_mixed_operation_expression(op1, op2)
        else:
            return self._generate_addition_subtraction_expression(op1, op2)

    def _generate_mixed_operation_expression(self, op1, op2):
        """生成包含乘除法的混合运算表达式"""
        # 确定哪个运算符是乘除法，优先处理乘除法
        if op1 in ['x', '÷']:
            # 第一个是乘除法，第二个是加减法
            if op1 == 'x':
                a = random.randint(max(2, self.min_number), min(self.max_number, 9))
                b = random.randint(max(2, self.min_number), min(self.max_number, 9))
                temp_result = a * b
            else:  # op1 == '÷'
                b = random.randint(max(2, self.min_number), min(self.max_number, 9))
                quotient = random.randint(max(1, self.min_result), min(self.max_result, self.max_number // b))
                a = b * quotient
                temp_result = quotient
            
            # 基于乘除法结果生成加减法
            if op2 == '+':
                c = random.randint(self.min_number, min(self.max_number, self.max_result - temp_result))
            else:  # op2 == '-'
                # 确保最终结果为正数
                c = random.randint(self.min_number, min(self.max_number, temp_result - self.min_result))
        
        elif op2 in ['x', '÷']:
            # 第二个是乘除法，第一个是加减法
            if op2 == 'x':
                # 先生成乘法部分
                b = random.randint(max(2, self.min_number), min(self.max_number, 9))
                c = random.randint(max(2, self.min_number), min(self.max_number, 9))
                multiplication_result = b * c
                
                # 基于乘法结果生成加减法
                if op1 == '+':
                    a = random.randint(self.min_number, min(self.max_number, self.max_result - multiplication_result))
                else:  # op1 == '-'
                    # 确保a - (b * c) > 0
                    a = random.randint(max(self.min_number, multiplication_result + self.min_result), self.max_number)
            
            else:  # op2 == '÷'
                # 先生成除法部分
                c = random.randint(max(2, self.min_number), min(self.max_number, 9))
                quotient = random.randint(max(1, self.min_result), min(self.max_result, self.max_number // c))
                b = c * quotient  # 被除数
                
                # 基于除法结果生成加减法
                if op1 == '+':
                    a = random.randint(self.min_number, min(self.max_number, self.max_result - quotient))
                else:  # op1 == '-'
                    # 确保a - (b ÷ c) > 0
                    a = random.randint(max(self.min_number, quotient + self.min_result), self.max_number)
        
        # 计算最终结果
        if op1 == 'x':
            temp = a * b
        elif op1 == '÷':
            temp = a // b
        elif op1 == '+':
            temp = a + (b * c if op2 == 'x' else b // c)
        else:  # op1 == '-'
            temp = a - (b * c if op2 == 'x' else b // c)
        
        if op2 == 'x':
            final_result = temp + b * c if op1 in ['+', '-'] else (a * b) + c if op1 == 'x' else (a // b) + c
        elif op2 == '÷':
            final_result = temp + b // c if op1 in ['+', '-'] else (a * b) + (b // c) if op1 == 'x' else (a // b) + (b // c)
        elif op2 == '+':
            final_result = temp + c
        else:  # op2 == '-'
            final_result = temp - c
        
        return f'{a} {op1} {b} {op2} {c} ='

    def _generate_addition_subtraction_expression(self, op1, op2):
        """生成纯加减法的三个数表达式"""
        # 生成合理的数值组合，确保每一步和最终结果都为正数
        
        # 根据运算符组合生成不同的数值
        if op1 == '+' and op2 == '+':
            # a + b + c
            a = random.randint(self.min_number, self.max_number)
            b = random.randint(self.min_number, min(self.max_number, self.max_result - a - self.min_number))
            c = random.randint(self.min_number, min(self.max_number, self.max_result - a - b))
            result = a + b + c
            
        elif op1 == '+' and op2 == '-':
            # a + b - c，确保a + b > c
            c = random.randint(self.min_number, self.max_number)
            temp_sum = random.randint(c + self.min_result, min(self.max_result + c, self.max_number * 2))
            a = random.randint(self.min_number, min(self.max_number, temp_sum - self.min_number))
            b = temp_sum - a
            if b > self.max_number:
                b = self.max_number
                a = temp_sum - b
            result = a + b - c
            
        elif op1 == '-' and op2 == '+':
            # a - b + c，确保a > b
            b = random.randint(self.min_number, self.max_number)
            c = random.randint(self.min_number, self.max_number)
            min_a = b + self.min_result - c if c < self.min_result else b + 1
            a = random.randint(max(self.min_number, min_a), self.max_number)
            result = a - b + c
            
        else:  # op1 == '-' and op2 == '-'
            # a - b - c，确保a > b + c
            b = random.randint(self.min_number, self.max_number)
            c = random.randint(self.min_number, self.max_number)
            min_a = b + c + self.min_result
            if min_a > self.max_number:
                # 重新生成较小的b和c
                total_subtract = random.randint(self.min_number, self.max_number - self.min_result)
                b = random.randint(self.min_number, total_subtract)
                c = total_subtract - b
                a = total_subtract + random.randint(self.min_result, min(self.max_result, self.max_number - total_subtract))
            else:
                a = random.randint(min_a, self.max_number)
            result = a - b - c
        
        return f'{a} {op1} {b} {op2} {c} ='
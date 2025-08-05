import random

class Constants:
    """常量定义"""
    # 计算相关常量
    MIN_RESULT = 1
    MAX_RESULT = 100
    MIN_MULTIPLICATION_FACTOR = 2
    MAX_MULTIPLICATION_FACTOR = 9
    MAX_TOTAL_PROBLEMS = 10000
    
    # 范围限制常量
    MIN_RANGE_VALUE = 1
    MAX_RANGE_VALUE = 999
    DEFAULT_MIN_NUMBER = 1
    DEFAULT_MAX_NUMBER = 100
    DEFAULT_MIN_RESULT = 1
    DEFAULT_MAX_RESULT = 100
    
    # 重试次数常量
    MAX_GENERATION_ATTEMPTS = 10
    DEFAULT_PROBLEM = '1 + 1 ='

class MathExpressionEngine:
    """数学表达式生成引擎
    
    负责生成各种类型的数学表达式，包括：
    - 加法、减法、乘法、除法
    - 混合运算
    - 带括号的表达式
    """
    
    def __init__(self, min_number=1, max_number=100, min_result=1, max_result=100):
        """初始化表达式生成引擎
        
        Args:
            min_number: 数字最小值
            max_number: 数字最大值
            min_result: 结果最小值
            max_result: 结果最大值
        """
        self.min_number = min_number
        self.max_number = max_number
        self.min_result = min_result
        self.max_result = max_result
    
    def update_ranges(self, min_number, max_number, min_result, max_result):
        """更新数字和结果范围"""
        self.min_number = min_number
        self.max_number = max_number
        self.min_result = min_result
        self.max_result = max_result
    
    def _get_user_ranges(self):
        """获取用户设置的数字和结果范围，并确保合理性"""
        min_num = self.min_number
        max_num = self.max_number
        min_result = self.min_result
        max_result = self.max_result
        
        # 确保范围合理
        if min_num > max_num:
            min_num, max_num = max_num, min_num
        if min_result > max_result:
            min_result, max_result = max_result, min_result
            
        return min_num, max_num, min_result, max_result
    
    def _generate_safe_random(self, min_val, max_val, fallback_min=1, fallback_max=10):
        """安全地生成随机数，如果范围无效则使用备用范围"""
        try:
            if min_val <= max_val:
                return random.randint(min_val, max_val)
            else:
                return random.randint(fallback_min, fallback_max)
        except ValueError:
            return random.randint(fallback_min, fallback_max)
    
    def _is_valid_expression_result(self, result, min_result, max_result):
        """验证表达式结果是否在有效范围内"""
        return min_result <= result <= max_result
    
    def _is_valid_number(self, number, min_num, max_num):
        """验证数字是否在有效范围内"""
        return min_num <= number <= max_num
    
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
            return f'{a} {op} {b} = (     )'
    
    def _safe_generate_expression(self, generator_func, max_attempts=Constants.MAX_GENERATION_ATTEMPTS):
        """安全地生成表达式，带重试机制"""
        for attempt in range(max_attempts):
            try:
                return generator_func()
            except (ValueError, ZeroDivisionError, OverflowError):
                if attempt == max_attempts - 1:
                    return Constants.DEFAULT_PROBLEM
                continue
        return Constants.DEFAULT_PROBLEM
    
    def _generate_addition_expression(self):
        """生成加法表达式"""
        min_num, max_num, min_result, max_result = self._get_user_ranges()
            
        # 生成两个加数，确保和在结果范围内
        a = self._generate_safe_random(min_num, max_num)
        max_b = min(max_num, max_result - a)
        if max_b < min_num:
            # 如果无法满足条件，调整a
            a = self._generate_safe_random(min_num, max_result - min_num)
            max_b = min(max_num, max_result - a)
        b = self._generate_safe_random(min_num, max_b)
        result = a + b
        
        return self._generate_bracket_expression(a, '+', b, result)
    
    def _generate_subtraction_expression(self):
        """生成减法表达式(确保结果为正)"""
        min_num, max_num, min_result, max_result = self._get_user_ranges()
            
        # 生成被减数和减数，确保差在结果范围内且为正
        result = self._generate_safe_random(min_result, max_result)
        b = self._generate_safe_random(min_num, max_num)
        a = result + b
        
        # 确保被减数在数字范围内
        if a > max_num:
            # 调整减数
            max_b = min(max_num, max_num - result)
            if max_b >= min_num:
                b = self._generate_safe_random(min_num, max_b)
                a = result + b
            else:
                # 重新生成较小的结果
                result = self._generate_safe_random(min_result, min(max_result, max_num - min_num))
                b = self._generate_safe_random(min_num, max_num - result)
                a = result + b
                
        return self._generate_bracket_expression(a, '-', b, result)
    
    def _generate_multiplication_expression(self):
        """生成乘法表达式"""
        min_num, max_num, min_result, max_result = self._get_user_ranges()
            
        # 生成两个乘数，确保结果在范围内
        a = self._generate_safe_random(max(2, min_num), min(max_num, 9))  # 限制乘数范围
        max_b = min(max_num, max_result // a) if a > 0 else max_num
        b = self._generate_safe_random(max(2, min_num), min(max_b, 9))
        result = a * b
        
        # 确保结果在范围内
        if result < min_result or result > max_result:
            # 重新生成较小的数
            a = self._generate_safe_random(2, min(5, max_num))
            b = self._generate_safe_random(2, min(max_result // a, max_num))
            result = a * b
            
        return self._generate_bracket_expression(a, 'x', b, result)
    
    def _generate_division_expression(self):
        """生成除法表达式(带余数)"""
        min_num, max_num, min_result, max_result = self._get_user_ranges()
            
        # 除数在数字范围内
        divisor = self._generate_safe_random(max(2, min_num), min(max_num, 9))  # 限制除数不要太大
        # 商在结果范围内
        quotient = self._generate_safe_random(min_result, min(max_result, max_num // divisor))
        # 余数小于除数
        remainder = self._generate_safe_random(0, divisor - 1)
        dividend = quotient * divisor + remainder
        
        # 确保被除数在数字范围内
        if dividend > max_num:
            dividend = max_num
            quotient = dividend // divisor
            remainder = dividend % divisor

        return self._generate_bracket_expression(dividend, '÷', divisor, f'{quotient}...{remainder}')
    
    def generate_expression(self, operation_type):
        """根据运算类型生成表达式
        
        Args:
            operation_type: 运算类型 ('addition', 'subtraction', 'multiplication', 'division', 'mixed')
            
        Returns:
            str: 生成的数学表达式
        """
        if operation_type == 'addition':
            return self._safe_generate_expression(self._generate_addition_expression)
        elif operation_type == 'subtraction':
            return self._safe_generate_expression(self._generate_subtraction_expression)
        elif operation_type == 'multiplication':
            return self._safe_generate_expression(self._generate_multiplication_expression)
        elif operation_type == 'division':
            return self._safe_generate_expression(self._generate_division_expression)
        elif operation_type == 'mixed':
            # 随机选择一种运算类型
            ops = ['addition', 'subtraction', 'multiplication', 'division']
            selected_op = random.choice(ops)
            return self.generate_expression(selected_op)
        else:
            return Constants.DEFAULT_PROBLEM
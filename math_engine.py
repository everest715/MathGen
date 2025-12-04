"""数学表达式生成引擎

包含所有数学表达式生成的核心逻辑
"""

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
                 allow_right_bracket: bool = False) -> None:
        """初始化数学引擎
        
        Args:
            min_number: 最小数字值（默认值：Constants.DEFAULT_MIN_NUMBER）
            max_number: 最大数字值（默认值：Constants.DEFAULT_MAX_NUMBER）
            min_result: 最小结果值（默认值：Constants.DEFAULT_MIN_RESULT）
            max_result: 最大结果值（默认值：Constants.DEFAULT_MAX_RESULT）
            allow_right_bracket: 是否允许括号出现在等号右边（默认值：False）
        """
        self.min_number: int = min_number or Constants.DEFAULT_MIN_NUMBER
        self.max_number: int = max_number or Constants.DEFAULT_MAX_NUMBER
        self.min_result: int = min_result or Constants.DEFAULT_MIN_RESULT
        self.max_result: int = max_result or Constants.DEFAULT_MAX_RESULT
        self.allow_right_bracket: bool = allow_right_bracket
        
        # 确保范围合理
        self._normalize_ranges()
    
    def _normalize_ranges(self) -> None:
        """规范化范围，确保最小值不大于最大值"""
        if self.min_number > self.max_number:
            self.min_number, self.max_number = self.max_number, self.min_number
        if self.min_result > self.max_result:
            self.min_result, self.max_result = self.max_result, self.min_result
    
    def update_ranges(self, 
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
        """
        self.min_number = min_number
        self.max_number = max_number
        self.min_result = min_result
        self.max_result = max_result
        if allow_right_bracket is not None:
            self.allow_right_bracket = allow_right_bracket
        
        self._normalize_ranges()
    
    def _generate_safe_random(self, min_val: int, max_val: int, 
                             fallback_min: int = 1, fallback_max: int = 10) -> int:
        """安全地生成随机数，如果范围无效则使用备用范围
        
        Args:
            min_val: 最小值
            max_val: 最大值
            fallback_min: 备用最小值（默认值：1）
            fallback_max: 备用最大值（默认值：10）
            
        Returns:
            生成的随机整数
        """
        try:
            if min_val <= max_val:
                return random.randint(min_val, max_val)
            else:
                return random.randint(fallback_min, fallback_max)
        except ValueError:
            return random.randint(fallback_min, fallback_max)
    
    def _is_valid_expression_result(self, result: int) -> bool:
        """验证表达式结果是否在有效范围内
        
        Args:
            result: 要验证的结果值
            
        Returns:
            结果是否在有效范围内
        """
        return self.min_result <= result <= self.max_result
    
    def _is_valid_number(self, number: int) -> bool:
        """验证数字是否在有效范围内
        
        Args:
            number: 要验证的数字
            
        Returns:
            数字是否在有效范围内
        """
        return self.min_number <= number <= self.max_number
    
    def _generate_multiplication_pair(self) -> Tuple[int, int]:
        """生成乘法因子对，确保结果不超过99
        
        Returns:
            两个乘法因子的元组 (a, b)
        """
        a = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, 
                          Constants.MAX_MULTIPLICATION_FACTOR)
        b = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, 
                          Constants.MAX_MULTIPLICATION_FACTOR)
        return a, b
    
    def _generate_division_pair(self) -> Tuple[int, int, int]:
        """生成除法数对，确保能整除
        
        Returns:
            被除数、除数、商的元组 (dividend, divisor, quotient)
        """
        divisor = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, 
                                Constants.MAX_MULTIPLICATION_FACTOR)
        quotient = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, 
                                 Constants.MAX_MULTIPLICATION_FACTOR)
        dividend = divisor * quotient
        return dividend, divisor, quotient
    
    def _find_factors(self, number: int) -> list[Tuple[int, int]]:
        """找到数字在指定范围内的因子对
        
        Args:
            number: 要查找因子的数字
            
        Returns:
            因子对的列表，每个元素是 (因子1, 因子2) 的元组
        """
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
        """生成带括号的表达式
        
        Args:
            a: 左操作数
            op: 运算符
            b: 右操作数
            result: 结果（字符串形式，可能包含余数）
            bracket_pos: 括号位置（0=左操作数, 1=右操作数, 2=等号左边无括号, 3=等号右边）
            
        Returns:
            格式化后的表达式字符串
        """
        if bracket_pos is None:
            # 根据allow_right_bracket参数决定可选的括号位置
            if self.allow_right_bracket:
                bracket_pos = random.choice([0, 1, 2, 3])  # 0,1,2为左边括号，3为右边括号
            else:
                bracket_pos = random.choice([0, 1, 2])  # 只允许左边括号
        
        expressions = {
            0: f'(     ) {op} {b} = {result}',      # 左操作数括号
            1: f'{a} {op} (     ) = {result}',      # 右操作数括号
            2: f'{a} {op} {b} =',                   # 等号左边无括号（填空结果）
            3: f'{a} {op} {b} = (     )'            # 等号右边括号（在allow_right_bracket=True时）
        }
        
        return expressions[bracket_pos]
    
    def _safe_generate_expression(self, generator_func: Callable[[], str], 
                                 max_attempts: int = Constants.MAX_GENERATION_ATTEMPTS) -> str:
        """安全地生成表达式，带重试机制
        
        Args:
            generator_func: 表达式生成函数
            max_attempts: 最大重试次数
            
        Returns:
            生成的表达式字符串，失败时返回默认表达式
        """
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
        """生成单个数学表达式

        Args:
            num_count: 等号左边数值数量（2或3）
            has_multiply: 是否包含乘法
            has_divide: 是否包含除法
            
        Returns:
            生成的表达式字符串
            
        Raises:
            ValueError: 当num_count不是2或3时
        """
        if num_count not in [2, 3]:
            raise ValueError("num_count必须是2或3")
        
        if num_count == 2:
            return self._generate_two_number_expression(has_multiply, has_divide)
        else:
            return self._generate_three_number_expression(has_multiply, has_divide)
        max_factor = Constants.MAX_MULTIPLICATION_FACTOR
        
        for i in range(min_factor, max_factor + 1):
            if number % i == 0:
                j = number // i
                if min_factor <= j <= max_factor:
                    factors.append((i, j))
        
        return factors
    
    def _generate_two_number_expression(self, has_multiply: bool, has_divide: bool) -> str:
        """生成两个数的表达式
        
        Args:
            has_multiply: 是否包含乘法
            has_divide: 是否包含除法
            
        Returns:
            生成的表达式字符串
        """
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
        if method:
            return method()
        else:
            return Constants.DEFAULT_PROBLEM
    
    def _generate_division_expression(self) -> str:
        """生成除法表达式(带余数)
        
        Returns:
            除法表达式字符串，格式: a ÷ b = quotient...remainder
        """
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
        """生成乘法表达式
        
        Returns:
            乘法表达式字符串，格式: a x b = result
        """
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
        """生成加法表达式
        
        Returns:
            加法表达式字符串，格式: a + b = result
        """
        # 生成两个加数，确保和在结果范围内
        a = self._generate_safe_random(self.min_number, self.max_number)
        max_b = min(self.max_number, self.max_result - a)
        
        if max_b < self.min_number:
            # 如果无法满足条件，调整a
            a = self._generate_safe_random(self.min_number, self.max_result - self.min_number)
            max_b = min(self.max_number, self.max_result - a)
        
        b = self._generate_safe_random(self.min_number, max_b)
        result = a + b
        
        expression = self._generate_bracket_expression(a, '+', b, result)
        return expression
    
    def _generate_subtraction_expression(self) -> str:
        """生成减法表达式(确保结果为正)
        
        Returns:
            减法表达式字符串，格式: a - b = result
        """
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
                result = self._generate_safe_random(
                    self.min_result, 
                    min(self.max_result, self.max_number - self.min_number)
                )
                b = self._generate_safe_random(self.min_number, self.max_number - result)
                a = result + b
                
        expression = self._generate_bracket_expression(a, '-', b, result)
        return expression

    def _generate_three_number_expression(self, has_multiply: bool, has_divide: bool) -> str:
        """生成三个数的表达式（混合运算）
        
        Args:
            has_multiply: 是否包含乘法
            has_divide: 是否包含除法
            
        Returns:
            生成的表达式字符串
        """
        # 获取可用的运算类型组合
        operation_pairs = self._get_operation_pairs(has_multiply, has_divide)
        
        if not operation_pairs:
            return Constants.DEFAULT_PROBLEM
        
        op1, op2 = random.choice(operation_pairs)
        
        # 生成表达式
        if op1 in ['x', '÷'] or op2 in ['x', '÷']:
            return self._generate_mixed_operation(op1, op2)
        else:
            return self._generate_addition_subtraction(op1, op2)
    
    def _get_operation_pairs(self, has_multiply: bool, has_divide: bool) -> list[tuple[str, str]]:
        """获取可用的运算类型组合
        
        Args:
            has_multiply: 是否包含乘法
            has_divide: 是否包含除法
            
        Returns:
            运算类型组合的列表，每个元素是 (op1, op2) 的元组
        """
        operation_pairs = []
        
        # 如果包含乘除法，添加混合运算组合
        if has_multiply:
            operation_pairs.extend([('x', '+'), ('x', '-'), ('+', 'x'), ('-', 'x')])
        
        if has_divide:
            operation_pairs.extend([('÷', '+'), ('÷', '-'), ('+', '÷'), ('-', '÷')])
        
        # 如果没有选择乘除法，只生成纯加减法
        if not operation_pairs:
            operation_pairs.extend([('+', '+'), ('+', '-'), ('-', '+'), ('-', '-')])
        
        return operation_pairs
    
    def _calculate_expression(self, numbers: tuple[int, int, int], 
                            ops: tuple[str, str]) -> int:
        """计算三个数的表达式结果
        
        Args:
            numbers: 三个数字的元组 (a, b, c)
            ops: 两个运算符的元组 (op1, op2)
            
        Returns:
            计算结果
            
        Note:
            遵循运算优先级：先乘除，后加减
        """
        a, b, c = numbers
        op1, op2 = ops
        
        # 先计算乘除法
        if op1 in ['x', '÷']:
            if op1 == 'x':
                temp = a * b
            else:
                temp = a // b if b != 0 else 0
            
            # 再计算加减法
            if op2 == '+':
                return temp + c
            else:
                return temp - c
        elif op2 in ['x', '÷']:
            # 先计算右边的乘除法
            if op2 == 'x':
                temp = b * c
            else:
                temp = b // c if c != 0 else 0
            
            # 再计算左边的加减法
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
    
    def _generate_mixed_operation(self, op1: str, op2: str) -> str:
        """生成包含乘除法的混合运算表达式
        
        Args:
            op1: 第一个运算符
            op2: 第二个运算符
            
        Returns:
            生成的表达式字符串
        """
        attempts = 0
        max_attempts = Constants.MAX_GENERATION_ATTEMPTS
        
        while attempts < max_attempts:
            try:
                result = self._try_generate_mixed(op1, op2)
                if result:
                    return result
            except Exception as e:
                attempts += 1
        return Constants.DEFAULT_PROBLEM
    
    def _try_generate_mixed(self, op1: str, op2: str) -> Optional[str]:
        """尝试生成混合运算表达式（内部方法）
        
        Args:
            op1: 第一个运算符
            op2: 第二个运算符
            
        Returns:
            表达式字符串，或None如果生成失败
        """
        # 根据运算符类型选择生成策略
        if op1 in ['x', '÷'] and op2 in ['+', '-']:
            return self._generate_mixed_first(op1, op2)
        elif op1 in ['+', '-'] and op2 in ['x', '÷']:
            return self._generate_mixed_second(op1, op2)
        else:
            # 两个都是乘除法的情况（不应发生）
            return None
    
    def _generate_mixed_first(self, op1: str, op2: str) -> Optional[str]:
        """生成第一个运算符是乘除法的表达式
        
        Args:
            op1: 第一个运算符（x或÷）
            op2: 第二个运算符（+或-）
            
        Returns:
            表达式字符串，或None如果生成失败
        """
        # 生成第一个运算的结果
        if op1 == 'x':
            a = self._generate_safe_random(2, min(self.max_number, 9))
            b = self._generate_safe_random(2, min(self.max_number, 9))
            temp_result = a * b
        else:  # op1 == '÷'
            b = self._generate_safe_random(2, min(self.max_number, 9))
            quotient = self._generate_safe_random(1, min(self.max_result, self.max_number // b if b > 0 else 1))
            a = b * quotient
            temp_result = quotient
        
        # 基于第一个结果生成第二个运算
        if op2 == '+':
            max_c = min(self.max_number, self.max_result - temp_result)
            if max_c < self.min_number:
                return None
            c = self._generate_safe_random(self.min_number, max_c)
        else:  # op2 == '-'
            max_c = min(self.max_number, temp_result - self.min_result)
            if max_c < self.min_number:
                return None
            c = self._generate_safe_random(self.min_number, max_c)
        
        # 验证最终结果
        final_result = self._calculate_expression((a, b, c), (op1, op2))
        if not self._is_valid_expression_result(final_result):
            return None
        
        return f'{a} {op1} {b} {op2} {c} ='
    
    def _generate_mixed_second(self, op1: str, op2: str) -> Optional[str]:
        """生成第二个运算符是乘除法的表达式
        
        Args:
            op1: 第一个运算符（+或-）
            op2: 第二个运算符（x或÷）
            
        Returns:
            表达式字符串，或None如果生成失败
        """
        # 先生成右边的乘除法
        if op2 == 'x':
            b = self._generate_safe_random(2, min(self.max_number, 9))
            c = self._generate_safe_random(2, min(self.max_number, 9))
            temp_result = b * c
        else:  # op2 == '÷'
            c = self._generate_safe_random(2, min(self.max_number, 9))
            quotient = self._generate_safe_random(1, min(self.max_result, self.max_number // c if c > 0 else 1))
            b = c * quotient
            temp_result = quotient
        
        # 基于右边结果生成左边的加减法
        if op1 == '+':
            max_a = min(self.max_number, self.max_result - temp_result)
            if max_a < self.min_number:
                return None
            a = self._generate_safe_random(self.min_number, max_a)
        else:  # op1 == '-'
            min_a = max(self.min_number, temp_result + self.min_result)
            if min_a > self.max_number:
                return None
            a = self._generate_safe_random(min_a, self.max_number)
        
        # 验证最终结果
        final_result = self._calculate_expression((a, b, c), (op1, op2))
        if not self._is_valid_expression_result(final_result):
            return None
        
        return f'{a} {op1} {b} {op2} {c} ='
    
    def _generate_addition_subtraction(self, op1: str, op2: str) -> str:
        """生成纯加减法的三个数表达式
        
        Args:
            op1: 第一个运算符（+或-）
            op2: 第二个运算符（+或-）
            
        Returns:
            表达式字符串
        """
        attempts = 0
        max_attempts = Constants.MAX_GENERATION_ATTEMPTS
        
        while attempts < max_attempts:
            try:
                result = self._try_generate_add_sub(op1, op2)
                if result:
                    return result
            except Exception as e:
                attempts += 1
        return Constants.DEFAULT_PROBLEM
    
    def _try_generate_add_sub(self, op1: str, op2: str) -> Optional[str]:
        """尝试生成加减法表达式（内部方法）
        
        Args:
            op1: 第一个运算符（+或-）
            op2: 第二个运算符（+或-）
            
        Returns:
            表达式字符串，或None如果生成失败
        """
        # 根据运算符组合选择生成策略
        if op1 == '+' and op2 == '+':
            return self._generate_add_add()
        elif op1 == '+' and op2 == '-':
            return self._generate_add_sub()
        elif op1 == '-' and op2 == '+':
            return self._generate_sub_add()
        else:  # op1 == '-' and op2 == '-'
            return self._generate_sub_sub()
    
    def _generate_add_add(self) -> Optional[str]:
        """生成 a + b + c 表达式
        
        Returns:
            表达式字符串，或None如果生成失败
        """
        # 平均分配结果范围
        a = self._generate_safe_random(self.min_number, 
                                      min(self.max_number, self.max_result // 3))
        b = self._generate_safe_random(self.min_number, 
                                      min(self.max_number, (self.max_result - a) // 2))
        c = self._generate_safe_random(self.min_number, 
                                      min(self.max_number, self.max_result - a - b))
        
        return f'{a} + {b} + {c} ='
    
    def _generate_add_sub(self) -> Optional[str]:
        """生成 a + b - c 表达式（确保 a + b > c）
        
        Returns:
            表达式字符串，或None如果生成失败
        """
        # 先确定c的范围
        max_c = min(self.max_number, self.max_result - self.min_result)
        if max_c < self.min_number:
            return None
        
        c = self._generate_safe_random(self.min_number, max_c)
        
        # 然后确定a + b的和
        min_sum = c + self.min_result
        max_sum = min(self.max_result + c, self.max_number * 2)
        
        if min_sum > max_sum:
            return None
        
        temp_sum = self._generate_safe_random(min_sum, max_sum)
        
        # 分配a和b
        a = self._generate_safe_random(self.min_number, min(self.max_number, temp_sum - self.min_number))
        b = temp_sum - a
        
        # 确保b在范围内
        if b < self.min_number or b > self.max_number:
            b = self.max_number
            a = temp_sum - b
        
        return f'{a} + {b} - {c} ='
    
    def _generate_sub_add(self) -> Optional[str]:
        """生成 a - b + c 表达式（确保 a > b）
        
        Returns:
            表达式字符串，或None如果生成失败
        """
        # 先确定b的范围
        b = self._generate_safe_random(self.min_number, self.max_number)
        
        # 确定a的最小值（必须大于b）
        min_a = max(self.min_number, b + self.min_result)
        if min_a > self.max_number:
            return None
        
        a = self._generate_safe_random(min_a, self.max_number)
        
        # 确定c的范围
        max_c = min(self.max_number, self.max_result - a + b)
        if max_c < self.min_number:
            return None
        
        c = self._generate_safe_random(self.min_number, max_c)
        
        return f'{a} - {b} + {c} ='
    
    def _generate_sub_sub(self) -> Optional[str]:
        """生成 a - b - c 表达式（确保 a > b + c）
        
        Returns:
            表达式字符串，或None如果生成失败
        """
        # 先确定b和c
        max_bc = self.max_number - self.min_result
        if max_bc < self.min_number * 2:
            # 范围太小，重新分配
            total_sub = self._generate_safe_random(self.min_number * 2, 
                                                  min(self.max_number * 2, self.max_result))
        else:
            total_sub = self._generate_safe_random(self.min_number * 2, max_bc)
        
        # 分配b和c
        b = self._generate_safe_random(self.min_number, min(self.max_number, total_sub - self.min_number))
        c = total_sub - b
        
        # 确保c在范围内
        if c < self.min_number or c > self.max_number:
            c = self.max_number
            b = total_sub - c
        
        # 确定a
        min_a = total_sub + self.min_result
        if min_a > self.max_number:
            return None
        
        a = self._generate_safe_random(min_a, self.max_number)
        
        return f'{a} - {b} - {c} ='

"""数学题生成器主程序

整合UI生成、算式生成、PDF生成等模块的入口文件
"""

import tkinter as tk
from tkinter import messagebox
import random
from constants import Constants
from ui_generator import UIGenerator
from math_engine import MathEngine
from pdf_generator import PDFGenerator

class MathProblemGenerator:
    """数学题生成器主类"""
    
    def __init__(self):
        """初始化数学题生成器"""
        self.root = tk.Tk()
        self.ui = UIGenerator(self.root, self.generate_problems)
        self.math_engine = MathEngine()
        self.pdf_generator = PDFGenerator()
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()
    
    def generate_problems(self):
        """生成数学题目"""
        try:
            # 获取用户设置
            settings = self.ui.get_user_settings()
            
            # 验证设置
            is_valid, error_msg = self._validate_settings(settings)
            if not is_valid:
                self.ui.show_error("设置错误", error_msg)
                return
            
            # 获取运算设置
            operation_settings = self._get_operation_settings(settings)
            if not any(operation_settings.values()):
                self.ui.show_error("设置错误", "请至少选择一种运算类型")
                return
            
            # 更新数学引擎的范围设置
            self.math_engine.update_ranges(
                int(settings['min_number']),
                int(settings['max_number']),
                int(settings['min_result']),
                int(settings['max_result'])
            )
            
            # 生成题目
            problems = self._generate_all_problems(
                int(settings['rows_per_page']),
                int(settings['cols_per_page']),
                int(settings['total_pages']),
                operation_settings
            )
            
            # 获取保存文件名
            save_filename = self.pdf_generator.get_save_filename(
                settings['save_path'],
                operation_settings['has_addition'],
                operation_settings['has_subtraction'],
                operation_settings['has_multiplication'],
                operation_settings['has_division'],
                operation_settings['has_mixed']
            )
            
            # 创建并保存PDF
            self._create_and_save_pdf(
                problems,
                save_filename,
                int(settings['rows_per_page']),
                int(settings['cols_per_page']),
                int(settings['total_pages']),
                int(settings['font_size'])
            )
            
            self.ui.show_success("生成成功", f"数学题已生成并保存到: {save_filename}")
            
        except Exception as e:
            self.ui.show_error("生成失败", f"生成数学题时发生错误: {str(e)}")
    
    def _validate_settings(self, settings):
        """验证用户设置
        
        参数:
            settings: 用户设置字典
            
        返回:
            (is_valid, error_message)
        """
        try:
            # 验证数字范围
            min_number = int(settings['min_number'])
            max_number = int(settings['max_number'])
            
            if not (Constants.MIN_RANGE_VALUE <= min_number <= Constants.MAX_RANGE_VALUE):
                return False, f"最小数字必须在{Constants.MIN_RANGE_VALUE}-{Constants.MAX_RANGE_VALUE}之间"
            
            if not (Constants.MIN_RANGE_VALUE <= max_number <= Constants.MAX_RANGE_VALUE):
                return False, f"最大数字必须在{Constants.MIN_RANGE_VALUE}-{Constants.MAX_RANGE_VALUE}之间"
            
            # 验证结果范围
            min_result = int(settings['min_result'])
            max_result = int(settings['max_result'])
            
            if not (Constants.MIN_RANGE_VALUE <= min_result <= Constants.MAX_RANGE_VALUE):
                return False, f"最小结果必须在{Constants.MIN_RANGE_VALUE}-{Constants.MAX_RANGE_VALUE}之间"
            
            if not (Constants.MIN_RANGE_VALUE <= max_result <= Constants.MAX_RANGE_VALUE):
                return False, f"最大结果必须在{Constants.MIN_RANGE_VALUE}-{Constants.MAX_RANGE_VALUE}之间"
            
            # PDF设置验证已移除，新的create_pdf函数会自动处理
            
            return True, ""
            
        except ValueError:
            return False, "请输入有效的数字"
        except Exception as e:
            return False, f"设置验证失败: {str(e)}"
    
    def _get_operation_settings(self, settings):
        """获取运算设置
        
        参数:
            settings: 用户设置字典
            
        返回:
            运算设置字典
        """
        # 处理数字数量选择
        num_count = 2 if settings['num_count'] == '2个数字' else 3
        
        return {
            'has_addition': settings['has_addition'],
            'has_subtraction': settings['has_subtraction'],
            'has_multiplication': settings['has_multiplication'],
            'has_division': settings['has_division'],
            'has_mixed': settings['has_mixed'],
            'num_count': num_count
        }
    
    def _generate_all_problems(self, rows_per_page, cols_per_page, total_pages, operation_settings):
        """生成所有题目
        
        参数:
            rows_per_page: 每页行数
            cols_per_page: 每页列数
            total_pages: 总页数
            operation_settings: 运算设置
            
        返回:
            题目列表
        """
        total_problems = rows_per_page * cols_per_page * total_pages
        problems = []
        
        # 获取可用的运算类型
        available_operations = self._get_available_operations(operation_settings)
        
        for _ in range(total_problems):
            problem = self._generate_single_problem(operation_settings, available_operations)
            problems.append(problem)
        
        return problems
    
    def _get_available_operations(self, operation_settings):
        """获取可用的运算类型列表"""
        operations = []
        operation_map = {
            'has_addition': 'addition',
            'has_subtraction': 'subtraction', 
            'has_multiplication': 'multiplication',
            'has_division': 'division'
        }
        
        for setting_key, operation_name in operation_map.items():
            if operation_settings.get(setting_key, False):
                operations.append(operation_name)
        
        return operations
    
    def _generate_single_problem(self, operation_settings, available_operations):
        """生成单个题目"""
        # 混合运算优先
        if operation_settings.get('has_mixed', False):
            return self.math_engine.generate_expression(
                num_count=operation_settings['num_count'],
                has_multiply=operation_settings.get('has_multiplication', False),
                has_divide=operation_settings.get('has_division', False)
            )
        
        # 单一运算类型
        if not available_operations:
            return Constants.DEFAULT_PROBLEM
            
        operation_type = random.choice(available_operations)
        
        # 三个数字的情况统一使用generate_expression
        if operation_settings['num_count'] == 3:
            return self._generate_three_number_problem(operation_type)
        
        # 两个数字的情况
        return self._generate_two_number_problem(operation_type)
    
    def _generate_three_number_problem(self, operation_type):
        """生成三个数字的题目"""
        has_multiply = operation_type == 'multiplication'
        has_divide = operation_type == 'division'
        return self.math_engine.generate_expression(
            num_count=3,
            has_multiply=has_multiply,
            has_divide=has_divide
        )
    
    def _generate_two_number_problem(self, operation_type):
        """生成两个数字的题目"""
        operation_methods = {
            'addition': self.math_engine._generate_addition_expression,
            'subtraction': self.math_engine._generate_subtraction_expression,
            'multiplication': self.math_engine._generate_multiplication_expression,
            'division': self.math_engine._generate_division_expression
        }
        
        method = operation_methods.get(operation_type)
        return method() if method else Constants.DEFAULT_PROBLEM
    
    def _create_and_save_pdf(self, problems, save_filename, rows_per_page, cols_per_page, total_pages, font_size):
        """创建并保存PDF
        
        参数:
            problems: 题目列表
            save_filename: 保存文件名
            rows_per_page: 每页行数
            cols_per_page: 每页列数
            total_pages: 总页数
            font_size: 字体大小
        """
        # 使用新的create_pdf函数签名
        self.pdf_generator.create_pdf(
            save_filename,
            problems,
            cols=cols_per_page,
            font_size=font_size,
            per_col=rows_per_page
        )

def main():
    """主函数"""
    app = MathProblemGenerator()
    app.run()

if __name__ == '__main__':
    main()
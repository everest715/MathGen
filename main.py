"""数学题生成器主程序

整合UI生成、算式生成、PDF生成等模块的入口文件
"""

import tkinter as tk
from tkinter import messagebox
from typing import Dict, List
import random
from constants import Constants
from ui_generator import UIGenerator
from math_engine import MathEngine
from pdf_generator import PDFGenerator


class MathProblemGenerator:
    """数学题生成器主类。"""
    
    def __init__(self):
        """初始化"""
        self.root = tk.Tk()
        self.ui = UIGenerator(self.root, self.generate_problems)
        self.math_engine = MathEngine()
        self.pdf_generator = PDFGenerator()
    
    def run(self):
        """运行应用程序"""
        self.root.mainloop()
    
    def generate_problems(self):
        """生成数学题目（主流程）"""
        try:
            # 获取并验证设置
            settings = self.ui.get_user_settings()
            is_valid, error_msg = self._validate_settings(settings)
            if not is_valid:
                self.ui.show_error("设置错误", error_msg)
                return
            
            # 验证运算类型
            operations = self._get_operation_settings(settings)
            if not any(operations.values()):
                self.ui.show_error("设置错误", "请至少选择一种运算类型")
                return
            
            # 生成题目
            problems = self._generate_all_problems(settings, operations)
            if not problems:
                return
            
            # 保存为PDF
            filename = self.pdf_generator.get_save_filename(
                settings['save_path'],
                operations['has_addition'],
                operations['has_subtraction'],
                operations['has_multiplication'],
                operations['has_division'],
                operations['has_mixed']
            )
            
            self.pdf_generator.create_pdf(
                filename,
                problems,
                cols=int(settings['cols_per_page']),
                font_size=int(settings['font_size']),
                per_col=int(settings['rows_per_page'])
            )
            
            self.ui.show_success("生成成功", f"数学题已保存到: {filename}")
            
        except Exception as e:
            self.ui.show_error("生成失败", f"生成数学题时发生错误: {str(e)}")
    
    def _validate_settings(self, settings: Dict) -> tuple:
        """验证用户设置"""
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
            
            # 更新数学引擎范围
            self.math_engine.update_ranges(
                min_number, max_number, min_result, max_result,
                settings['allow_left_bracket'],
                settings['allow_right_bracket'],
                settings['reduce_round_tens']
            )
            
            return True, ""
        except ValueError:
            return False, "请输入有效的数字"
        except Exception as e:
            return False, f"设置验证失败: {str(e)}"
    
    def _get_operation_settings(self, settings: Dict) -> Dict:
        """获取运算设置"""
        return {
            'has_addition': settings['has_addition'],
            'has_subtraction': settings['has_subtraction'],
            'has_multiplication': settings['has_multiplication'],
            'has_division': settings['has_division'],
            'has_mixed': settings['has_mixed'],
            'num_count': 2 if settings['num_count'] == '2个数字' else 3
        }
    
    def _generate_all_problems(self, settings: Dict, operations: Dict) -> List[str]:
        """生成所有题目"""
        total_problems = (int(settings['rows_per_page']) * 
                         int(settings['cols_per_page']) * 
                         int(settings['total_pages']))
        
        # 获取可用运算类型
        available_ops = []
        op_map = {
            'has_addition': 'addition',
            'has_subtraction': 'subtraction',
            'has_multiplication': 'multiplication',
            'has_division': 'division',
            'has_mixed': 'mixed'
        }
        for key, op in op_map.items():
            if operations.get(key, False):
                available_ops.append(op)
        
        if not available_ops:
            return []
        
        # 生成题目
        problems = []
        for _ in range(total_problems):
            op_type = random.choice(available_ops)
            
            if operations['has_mixed']:
                problem = self.math_engine.generate_expression(
                    num_count=3,
                    has_multiply=True,
                    has_divide=True
                )
            elif op_type == 'multiplication':
                problem = self.math_engine._generate_multiplication_expression()
            elif op_type == 'division':
                problem = self.math_engine._generate_division_expression()
            elif operations['num_count'] == 3:
                has_mul = op_type in ['multiplication', 'mixed']
                has_div = op_type in ['division', 'mixed']
                problem = self.math_engine.generate_expression(
                    num_count=3,
                    has_multiply=has_mul,
                    has_divide=has_div
                )
            elif op_type == 'addition':
                problem = self.math_engine._generate_addition_expression()
            elif op_type == 'subtraction':
                problem = self.math_engine._generate_subtraction_expression()
            else:
                problem = self.math_engine.generate_expression(
                    num_count=operations['num_count'],
                    has_multiply=op_type in ['multiplication', 'mixed'],
                    has_divide=op_type in ['division', 'mixed']
                )
            
            problems.append(problem)
        
        return problems


def main():
    """主函数"""
    app = MathProblemGenerator()
    app.run()


if __name__ == "__main__":
    main()
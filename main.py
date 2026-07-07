"""数学题生成器主程序

整合UI生成、算式生成、PDF生成等模块的入口文件
"""

import ctypes
import random
import tkinter as tk
from typing import Dict, List
from constants import Constants
from ui_generator import UIGenerator
from math_engine import MathEngine
from pdf_generator import PDFGenerator

# 启用 Windows 高 DPI 支持，解决文字模糊问题
ctypes.windll.shcore.SetProcessDpiAwareness(1)


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
            active_tab = self.ui.get_active_tab()

            if active_tab == '巧算':
                self._generate_clever_problems()
            else:
                self._generate_normal_problems()
        except Exception as e:
            self.ui.show_error("生成失败", f"生成数学题时发生错误: {str(e)}")

    def _generate_normal_problems(self):
        """普通页生成流程"""
        settings = self.ui.get_user_settings()
        is_valid, error_msg = self._validate_settings(settings)
        if not is_valid:
            self.ui.show_error("设置错误", error_msg)
            return

        operations = self._get_operation_settings(settings)
        if not any(v for k, v in operations.items() if k != 'num_count'):
            self.ui.show_error("设置错误", "请至少选择一种运算类型")
            return

        problems = self._generate_all_problems(settings, operations)
        if not problems:
            return

        filename = self.pdf_generator.get_save_filename(
            settings['save_path'],
            operations['has_addition'],
            operations['has_subtraction'],
            operations['has_multiplication'],
            operations['has_division'],
            operations['has_division_no_remainder']
        )

        self.pdf_generator.create_pdf(
            filename, problems,
            cols=int(settings['cols_per_page']),
            font_size=int(settings['font_size']),
            per_col=int(settings['rows_per_page'])
        )

        self.ui.show_success("生成成功", f"数学题已保存到: {filename}")

    def _generate_clever_problems(self):
        """巧算页生成流程"""
        settings = self.ui.get_clever_settings()
        is_valid, error_msg = self._validate_clever_settings(settings)
        if not is_valid:
            self.ui.show_error("设置错误", error_msg)
            return

        self.math_engine.update_ranges(
            int(settings['min_number']), int(settings['max_number']),
            int(settings['min_result']), int(settings['max_result']),
            settings['allow_left_bracket'],
            settings['allow_right_bracket']
        )

        total_problems = (int(settings['rows_per_page']) *
                          int(settings['cols_per_page']) *
                          int(settings['total_pages']))

        problems = []
        for _ in range(total_problems):
            problem = self.math_engine.generate_clever_expression(settings['clever_type'])
            problems.append(problem)

        filename = settings['save_path'] or f"数学题_{settings['clever_type']}.pdf"

        self.pdf_generator.create_pdf(
            filename, problems,
            cols=int(settings['cols_per_page']),
            font_size=int(settings['font_size']),
            per_col=int(settings['rows_per_page'])
        )

        self.ui.show_success("生成成功", f"数学题已保存到: {filename}")

    def _validate_settings(self, settings: Dict) -> tuple:
        """验证普通页用户设置"""
        try:
            for field, label in [('min_number', '最小数字'), ('max_number', '最大数字'),
                                 ('min_result', '最小结果'), ('max_result', '最大结果')]:
                value = int(settings[field])
                if not (Constants.MIN_RANGE_VALUE <= value <= Constants.MAX_RANGE_VALUE):
                    return False, f"{label}必须在{Constants.MIN_RANGE_VALUE}-{Constants.MAX_RANGE_VALUE}之间"

            page_validations = [
                ('rows_per_page', '每页行数', Constants.MIN_ROWS_PER_PAGE, Constants.MAX_ROWS_PER_PAGE),
                ('cols_per_page', '每页列数', Constants.MIN_COLS_PER_PAGE, Constants.MAX_COLS_PER_PAGE),
                ('total_pages', '总页数', Constants.MIN_TOTAL_PAGES, Constants.MAX_TOTAL_PAGES),
                ('font_size', '字体大小', Constants.MIN_FONT_SIZE, Constants.MAX_FONT_SIZE),
            ]
            for field, label, min_val, max_val in page_validations:
                value = int(settings[field])
                if not (min_val <= value <= max_val):
                    return False, f"{label}必须在{min_val}-{max_val}之间"

            total = (int(settings['rows_per_page']) *
                     int(settings['cols_per_page']) *
                     int(settings['total_pages']))
            if total > Constants.MAX_TOTAL_PROBLEMS:
                return False, f"总题数不能超过{Constants.MAX_TOTAL_PROBLEMS}题（当前{total}题）"

            self.math_engine.update_ranges(
                int(settings['min_number']), int(settings['max_number']),
                int(settings['min_result']), int(settings['max_result']),
                settings['allow_left_bracket'],
                settings['allow_right_bracket']
            )

            return True, ""
        except ValueError:
            return False, "请输入有效的数字"
        except Exception as e:
            return False, f"设置验证失败: {str(e)}"

    def _validate_clever_settings(self, settings: Dict) -> tuple:
        """验证巧算页用户设置"""
        try:
            for field, label in [('min_number', '最小数字'), ('max_number', '最大数字'),
                                 ('min_result', '最小结果'), ('max_result', '最大结果')]:
                value = int(settings[field])
                if not (Constants.MIN_RANGE_VALUE <= value <= Constants.MAX_RANGE_VALUE):
                    return False, f"{label}必须在{Constants.MIN_RANGE_VALUE}-{Constants.MAX_RANGE_VALUE}之间"

            page_validations = [
                ('rows_per_page', '每页行数', Constants.MIN_ROWS_PER_PAGE, Constants.MAX_ROWS_PER_PAGE),
                ('cols_per_page', '每页列数', Constants.MIN_COLS_PER_PAGE, Constants.MAX_COLS_PER_PAGE),
                ('total_pages', '总页数', Constants.MIN_TOTAL_PAGES, Constants.MAX_TOTAL_PAGES),
                ('font_size', '字体大小', Constants.MIN_FONT_SIZE, Constants.MAX_FONT_SIZE),
            ]
            for field, label, min_val, max_val in page_validations:
                value = int(settings[field])
                if not (min_val <= value <= max_val):
                    return False, f"{label}必须在{min_val}-{max_val}之间"

            total = (int(settings['rows_per_page']) *
                     int(settings['cols_per_page']) *
                     int(settings['total_pages']))
            if total > Constants.MAX_TOTAL_PROBLEMS:
                return False, f"总题数不能超过{Constants.MAX_TOTAL_PROBLEMS}题（当前{total}题）"

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
            'has_division_no_remainder': settings['has_division_no_remainder'],
            'num_count': 2 if settings['num_count'] == '2' else 3
        }

    def _generate_all_problems(self, settings: Dict, operations: Dict) -> List[str]:
        """生成所有题目"""
        total_problems = (int(settings['rows_per_page']) *
                          int(settings['cols_per_page']) *
                          int(settings['total_pages']))

        available_ops = []
        op_map = {
            'has_addition': 'addition',
            'has_subtraction': 'subtraction',
            'has_multiplication': 'multiplication',
            'has_division': 'division',
            'has_division_no_remainder': 'division_no_remainder',
        }
        for key, op in op_map.items():
            if operations.get(key, False):
                available_ops.append(op)

        if not available_ops:
            return []

        two_num_methods = {
            'addition': self.math_engine._generate_addition_expression,
            'subtraction': self.math_engine._generate_subtraction_expression,
            'multiplication': self.math_engine._generate_multiplication_expression,
            'division': self.math_engine._generate_division_expression,
            'division_no_remainder': self.math_engine._generate_division_no_remainder_expression,
        }

        num_count = operations['num_count']

        problems = []
        for _ in range(total_problems):
            op_type = random.choice(available_ops)

            if num_count == 2:
                method = two_num_methods.get(op_type)
                problem = method() if method else Constants.DEFAULT_PROBLEM
            else:
                has_mul = op_type == 'multiplication'
                has_div = op_type in ['division', 'division_no_remainder']
                problem = self.math_engine.generate_expression(
                    num_count=3, has_multiply=has_mul, has_divide=has_div
                )

            problems.append(problem)

        return problems


def main():
    """主函数"""
    app = MathProblemGenerator()
    app.run()


if __name__ == "__main__":
    main()

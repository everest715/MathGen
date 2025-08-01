import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QSpinBox, QPushButton,
                             QFileDialog, QMessageBox, QComboBox, QCheckBox)
from PyQt6.QtCore import Qt
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Preformatted, BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.units import inch

# 常量定义
class Constants:
    # 数值范围
    MIN_MULTIPLICATION_FACTOR = 2
    MAX_MULTIPLICATION_FACTOR = 9
    MAX_ADDITION_VALUE = 999
    MIN_ADDITION_VALUE = 1
    
    # UI配置
    DEFAULT_PAGES = 10
    DEFAULT_COLS = 3
    DEFAULT_PER_COL = 25
    DEFAULT_FONT_SIZE = 16
    
    # 范围限制
    MAX_PAGES = 100
    MAX_COLS = 5
    MIN_PER_COL = 5
    MAX_PER_COL = 50
    MIN_FONT_SIZE = 12
    MAX_FONT_SIZE = 24

class MathProblemGenerator(QMainWindow):
    """数学题目生成器主窗口类

    功能：
    - 生成加减法填空题
    - 支持多页、多列、自定义每列题数
    - 可调节字号和行间距
    - 导出为PDF格式
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('数学题目生成器')
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # 创建各种控件
        self._create_basic_controls(layout)
        self._create_operation_controls(layout)
        self._create_action_controls(layout)

        central_widget.setLayout(layout)
        self.update_preview()

    def _create_spinbox_layout(self, label_text, min_val, max_val, default_val, callback=None):
        """创建SpinBox布局的通用方法"""
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label_text))
        
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.setValue(default_val)
        
        if callback:
            spinbox.valueChanged.connect(callback)
            
        layout.addWidget(spinbox)
        layout.addStretch()
        
        return layout, spinbox

    def _create_checkbox_layout(self, label_text):
        """创建CheckBox布局的通用方法"""
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label_text))
        
        checkbox = QCheckBox()
        layout.addWidget(checkbox)
        layout.addStretch()
        
        return layout, checkbox

    def _create_basic_controls(self, main_layout):
        """创建基础控件"""
        # 页数设置
        pages_layout, self.pages_spinbox = self._create_spinbox_layout(
            '页数:', 1, Constants.MAX_PAGES, Constants.DEFAULT_PAGES)
        main_layout.addLayout(pages_layout)

        # 列数设置
        cols_layout, self.cols_spinbox = self._create_spinbox_layout(
            '每页列数:', 1, Constants.MAX_COLS, Constants.DEFAULT_COLS, self.update_preview)
        main_layout.addLayout(cols_layout)

        # 每列题目数设置
        per_col_layout, self.per_col_spinbox = self._create_spinbox_layout(
            '每列题数:', Constants.MIN_PER_COL, Constants.MAX_PER_COL, 
            Constants.DEFAULT_PER_COL, self.update_preview)
        main_layout.addLayout(per_col_layout)

        # 字号设置
        font_layout, self.font_spinbox = self._create_spinbox_layout(
            '字号:', Constants.MIN_FONT_SIZE, Constants.MAX_FONT_SIZE, 
            Constants.DEFAULT_FONT_SIZE, self.update_preview)
        main_layout.addLayout(font_layout)

    def _create_operation_controls(self, main_layout):
        """创建运算类型控件"""
        # 数字个数
        num_count_layout = QHBoxLayout()
        num_count_layout.addWidget(QLabel('数字个数:'))
        self.num_count_combo = QComboBox()
        self.num_count_combo.addItems(['2个数字', '3个数字'])
        num_count_layout.addWidget(self.num_count_combo)
        num_count_layout.addStretch()
        main_layout.addLayout(num_count_layout)

        # 包含乘法
        multiply_layout, self.multiply_check = self._create_checkbox_layout('包含乘法:')
        main_layout.addLayout(multiply_layout)

        # 包含除法
        divide_layout, self.divide_check = self._create_checkbox_layout('包含除法:')
        main_layout.addLayout(divide_layout)

    def _create_action_controls(self, main_layout):
        """创建操作控件"""
        # 生成按钮
        self.generate_btn = QPushButton('生成PDF')
        self.generate_btn.clicked.connect(self.generate_problems)
        main_layout.addWidget(self.generate_btn)
        
        main_layout.addStretch()
        
        # 预览标签
        self.preview_label = QLabel('总题数: 0')
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.preview_label)

    def update_preview(self):
        """实时更新预览总题数"""
        pages = self.pages_spinbox.value()
        cols = self.cols_spinbox.value()
        per_col = self.per_col_spinbox.value()
        total_problems = pages * per_col * cols
        self.preview_label.setText(f'总题数: {total_problems}')

    def generate_expression(self, num_count=2, has_multiply=False, has_divide=False):
        """生成单个数学表达式

        参数：
            num_count: 等号左边数值数量（2或3）
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
            operation_choices.append('divide')
        if has_multiply:
            operation_choices.append('multiply')
        operation_choices.extend(['add', 'subtract'])  # 总是包含加减法
        
        operation = random.choice(operation_choices)
        
        if operation == 'divide':
            return self._generate_division_expression()
        elif operation == 'multiply':
            return self._generate_multiplication_expression()
        elif operation == 'add':
            return self._generate_addition_expression()
        else:  # subtract
            return self._generate_subtraction_expression()

    def _generate_division_expression(self):
        """生成除法表达式（带余数）"""
        divisor = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, Constants.MAX_MULTIPLICATION_FACTOR)
        dividend = (random.randint(1, Constants.MAX_MULTIPLICATION_FACTOR) * divisor + 
                   random.randint(1, divisor-1))
        quotient = dividend // divisor
        remainder = dividend % divisor

        bracket_pos = random.choice([0, 1, 2])
        if bracket_pos == 0:
            return f'(     ) ÷ {divisor} = {quotient}...{remainder}'
        elif bracket_pos == 1:
            return f'{dividend} ÷ (     ) = {quotient}...{remainder}'
        else:
            return f'{dividend} ÷ {divisor} = (     )...{remainder}'

    def _generate_multiplication_expression(self):
        """生成乘法表达式（99乘法表）"""
        a = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, Constants.MAX_MULTIPLICATION_FACTOR)
        b = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, Constants.MAX_MULTIPLICATION_FACTOR)
        result = a * b

        bracket_pos = random.choice([0, 1, 2])
        if bracket_pos == 0:
            return f'(     ) × {b} = {result}'
        elif bracket_pos == 1:
            return f'{a} × (     ) = {result}'
        else:
            return f'{a} × {b} = (     )'

    def _generate_addition_expression(self):
        """生成加法表达式"""
        a = random.randint(Constants.MIN_ADDITION_VALUE, Constants.MAX_ADDITION_VALUE)
        result = random.randint(a+1, Constants.MAX_ADDITION_VALUE)
        b = result - a

        bracket_pos = random.choice([0, 1, 2])
        if bracket_pos == 0:
            return f'(     ) + {b} = {result}'
        elif bracket_pos == 1:
            return f'{a} + (     ) = {result}'
        else:
            return f'{a} + {b} = (     )'

    def _generate_subtraction_expression(self):
        """生成减法表达式（确保结果为正）"""
        a = random.randint(2, Constants.MAX_ADDITION_VALUE)
        b = random.randint(Constants.MIN_ADDITION_VALUE, a-1)
        result = a - b

        bracket_pos = random.choice([0, 1, 2])
        if bracket_pos == 0:
            return f'(     ) - {b} = {result}'
        elif bracket_pos == 1:
            return f'{a} - (     ) = {result}'
        else:
            return f'{a} - {b} = (     )'

    def _generate_three_number_expression(self, has_multiply, has_divide):
        """生成三个数的表达式"""
        # 确定运算符组合
        if has_multiply and has_divide:
            operations = [('×', '÷'), ('÷', '×')]
        elif has_multiply:
            operations = [('×', '+'), ('×', '-'), ('+', '×'), ('-', '×')]
        elif has_divide:
            operations = [('÷', '+'), ('÷', '-'), ('+', '÷'), ('-', '÷')]
        else:
            operations = [('+', '+'), ('+', '-'), ('-', '+'), ('-', '-')]
        
        op1, op2 = random.choice(operations)
        
        # 生成数值
        if '×' in [op1, op2] or '÷' in [op1, op2]:
            return self._generate_mixed_operation_expression(op1, op2)
        else:
            return self._generate_addition_subtraction_expression(op1, op2)

    def _generate_mixed_operation_expression(self, op1, op2):
        """生成包含乘除法的混合运算表达式"""
        a = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, Constants.MAX_MULTIPLICATION_FACTOR)
        b = random.randint(Constants.MIN_MULTIPLICATION_FACTOR, Constants.MAX_MULTIPLICATION_FACTOR)
        
        if op1 == '÷' or op2 == '÷':
            a = a * b  # 确保整除
        
        c = random.randint(Constants.MIN_ADDITION_VALUE, 99)
        
        return f'{a} {op1} {b} {op2} {c} = (     )'

    def _generate_addition_subtraction_expression(self, op1, op2):
        """生成纯加减法表达式"""
        # 生成合理的数值组合，确保结果为正
        a = random.randint(10, 200)
        b = random.randint(1, 50)
        c = random.randint(1, 50)
        
        return f'{a} {op1} {b} {op2} {c} = (     )'

    def create_pdf(self, filename, problems, cols=3, font_size=16, per_col=25):
        """创建PDF文档

        参数：
            filename: 输出文件名
            problems: 题目列表
            cols: 每页列数
            font_size: 题目字号大小
            per_col: 每列题目数量
        """
        # 自定义多列文档模板
        class MultiColumnDocTemplate(BaseDocTemplate):
            def __init__(self, filename, cols=3, **kwargs):
                super().__init__(filename, **kwargs)
                self.cols = cols

            def build(self, flowables, **kwargs):
                """构建多列布局"""
                frame_width = (self.width) / self.cols
                frames = []
                for i in range(self.cols):
                    left = self.leftMargin + i * frame_width
                    width = frame_width - 12  # 留出间距
                    frame = Frame(left, 0,
                                width, self.height,
                                leftPadding=6, bottomPadding=0, rightPadding=6, topPadding=0)
                    frames.append(frame)

                template = PageTemplate(frames=frames)
                self.addPageTemplates([template])
                super().build(flowables, **kwargs)

        # 创建PDF文档
        doc = MultiColumnDocTemplate(filename, cols=cols,
                                   pagesize=letter,
                                   rightMargin=48, leftMargin=48,
                                   topMargin=18, bottomMargin=36)

        # 计算可用的列高度 (letter页面高度 - 上下边距)
        available_height = letter[1] - 18 - 36  # topMargin + bottomMargin

        # 计算每道题目的最大高度，确保每列不超过指定数量
        max_line_height = available_height / per_col

        # 设置样式
        styles = getSampleStyleSheet()
        style = styles['Normal']
        style.fontSize = font_size
        style.leading = max_line_height - font_size / inch  # 使用动态计算的行间距

        # 添加内容
        content = []
        for i, prob in enumerate(problems):
            p = Preformatted(f"{prob}", style)
            content.append(p)

        doc.build(content)

    def _validate_settings(self):
        """验证用户设置"""
        errors = []
        
        pages = self.pages_spinbox.value()
        cols = self.cols_spinbox.value()
        per_col = self.per_col_spinbox.value()
        total_problems = pages * per_col * cols
        
        if total_problems > 10000:
            errors.append(f'总题数过多({total_problems})，建议不超过10000题')
        
        if total_problems == 0:
            errors.append('题目数量不能为0')
            
        return errors

    def _get_operation_settings(self):
        """获取运算设置"""
        num_count = 2 if self.num_count_combo.currentText() == '2个数字' else 3
        has_multiply = self.multiply_check.isChecked()
        has_divide = self.divide_check.isChecked()
        
        return num_count, has_multiply, has_divide

    def generate_problems(self):
        """生成题目并创建PDF"""
        # 验证设置
        validation_errors = self._validate_settings()
        if validation_errors:
            QMessageBox.warning(self, '设置错误', '\n'.join(validation_errors))
            return
        
        # 获取设置
        pages = self.pages_spinbox.value()
        cols = self.cols_spinbox.value()
        per_col = self.per_col_spinbox.value()
        font_size = self.font_spinbox.value()
        
        num_count, has_multiply, has_divide = self._get_operation_settings()
        total_problems = pages * per_col * cols

        try:
            # 生成所有题目
            problems = self._generate_all_problems(total_problems, num_count, has_multiply, has_divide)

            # 选择保存位置
            filename = self._get_save_filename()
            if not filename:
                return

            # 创建PDF
            self._create_and_save_pdf(filename, problems, cols, font_size, per_col, total_problems)

        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成失败：{str(e)}')

    def _generate_all_problems(self, total_problems, num_count, has_multiply, has_divide):
        """生成所有题目"""
        problems = []
        for i in range(total_problems):
            try:
                problem = self.generate_expression(num_count, has_multiply, has_divide)
                problems.append(problem)
            except Exception as e:
                # 如果单个题目生成失败，使用默认题目
                problems.append(f'1 + 1 = (     )')  # 默认题目
                print(f'题目生成失败 {i+1}: {e}')  # 调试信息
        return problems

    def _get_save_filename(self):
        """获取保存文件名"""
        filename, _ = QFileDialog.getSaveFileName(
            self, '保存PDF文件', '数学题目.pdf', 'PDF文件 (*.pdf)')
        return filename

    def _create_and_save_pdf(self, filename, problems, cols, font_size, per_col, total_problems):
        """创建并保存PDF"""
        self.create_pdf(filename, problems, cols, font_size, per_col)
        QMessageBox.information(
            self, '成功',
            f'已生成{total_problems}道题目到\n{filename}')

if __name__ == '__main__':
    # 启动应用程序
    app = QApplication(sys.argv)
    window = MathProblemGenerator()
    window.show()
    sys.exit(app.exec())
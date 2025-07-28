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

        # 页数设置
        pages_layout = QHBoxLayout()
        pages_layout.addWidget(QLabel('页数:'))
        self.pages_spinbox = QSpinBox()
        self.pages_spinbox.setRange(1, 50)
        self.pages_spinbox.setValue(10)
        pages_layout.addWidget(self.pages_spinbox)
        pages_layout.addStretch()

        # 列数设置
        cols_layout = QHBoxLayout()
        cols_layout.addWidget(QLabel('每页列数:'))
        self.cols_spinbox = QSpinBox()
        self.cols_spinbox.setRange(1, 5)
        self.cols_spinbox.setValue(4)
        cols_layout.addWidget(self.cols_spinbox)
        cols_layout.addStretch()

        # 每列题目数设置
        per_col_layout = QHBoxLayout()
        per_col_layout.addWidget(QLabel('每列题目数:'))
        self.per_col_spinbox = QSpinBox()
        self.per_col_spinbox.setRange(10, 80)
        self.per_col_spinbox.setValue(25)
        self.per_col_spinbox.valueChanged.connect(self.update_preview)
        per_col_layout.addWidget(self.per_col_spinbox)
        per_col_layout.addStretch()

        # 字号设置
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel('字号:'))
        self.font_spinbox = QSpinBox()
        self.font_spinbox.setRange(12, 24)
        self.font_spinbox.setValue(14)
        self.font_spinbox.valueChanged.connect(self.update_preview)
        font_layout.addWidget(self.font_spinbox)
        font_layout.addStretch()

        # 数字个数
        num_count_layout = QHBoxLayout()
        num_count_layout.addWidget(QLabel('数字个数:'))
        self.num_count_combo = QComboBox()
        self.num_count_combo.addItems(['2个数字', '3个数字'])
        num_count_layout.addWidget(self.num_count_combo)
        num_count_layout.addStretch()

        # 包含乘法
        multiply_layout = QHBoxLayout()
        multiply_layout.addWidget(QLabel('包含乘法:'))
        self.multiply_check = QCheckBox()
        multiply_layout.addWidget(self.multiply_check)
        multiply_layout.addStretch()

        # 包含除法
        divide_layout = QHBoxLayout()
        divide_layout.addWidget(QLabel('包含除法:'))
        self.divide_check = QCheckBox()
        divide_layout.addWidget(self.divide_check)
        divide_layout.addStretch()

        # 预览标签
        self.preview_label = QLabel('总题数: 0')
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 生成按钮
        self.generate_btn = QPushButton('生成PDF')
        self.generate_btn.clicked.connect(self.generate_problems)

        # 添加到主布局
        layout.addLayout(pages_layout)
        layout.addLayout(cols_layout)
        layout.addLayout(per_col_layout)
        layout.addLayout(font_layout)
        layout.addLayout(num_count_layout)
        layout.addLayout(multiply_layout)
        layout.addLayout(divide_layout)
        layout.addWidget(self.generate_btn)
        layout.addStretch()
        layout.addWidget(self.preview_label)

        central_widget.setLayout(layout)

        self.update_preview()

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

        返回格式：
        - 加减法：(     ) + b = c 或 a - (     ) = b
        - 乘除法：遵循99乘法表限制
        - 除法：2个数时等号右边显示余数
        """
        # 确定可用的运算符
        operators = ['+', '-']
        if has_multiply:
            operators.append('*')
        if has_divide:
            operators.append('/')

        if num_count == 2:
            # 2个数的情况
            if has_divide and '/' in operators and random.choice([True, False]):
                # 除法且显示余数
                divisor = random.randint(2, 9)
                dividend = random.randint(1, 9) * divisor + random.randint(1, divisor-1)
                quotient = dividend // divisor
                remainder = dividend % divisor

                bracket_pos = random.choice([0, 1, 2])
                match bracket_pos:
                    case 0:
                        return f'(     ) ÷ {divisor} = {quotient}...{remainder}'
                    case 1:
                        return f'{dividend} ÷ (     ) = {quotient}...{remainder}'
                    case 2:
                        return f'{dividend} ÷ {divisor} = (     )...(     )'

            elif has_multiply and '*' in operators and random.choice([True, False]):
                # 乘法（99乘法表）
                a = random.randint(2, 9)
                b = random.randint(2, 9)
                result = a * b

                bracket_pos = random.choice([0, 1, 2])
                match bracket_pos:
                    case 0:
                        return f'(     ) × {b} = {result}'
                    case 1:
                        return f'{a} × (     ) = {result}'
                    case 2:
                        return f'{a} × {b} ='

            else:
                # 只有加减法，1000以内
                operator = random.choice(['+', '-'])
                if operator == '+':
                    a = random.randint(1, 999)
                    result = random.randint(a+1, 999)
                    b = result - a

                    bracket_pos = random.choice([0, 1, 2])
                    match bracket_pos:
                        case 0:
                            return f'(     ) + {b} = {result}'
                        case 1:
                            return f'{a} + (     ) = {result}'
                        case 2:
                            return f'{a} + {b} ='
                else:
                    # 减法确保结果为正
                    a = random.randint(2, 999)
                    b = random.randint(1, a-1)
                    result = a - b

                    bracket_pos = random.choice([0, 1, 2])
                    match bracket_pos:
                        case 0:
                            return f'(     ) - {b} = {result}'
                        case 1:
                            return f'{a} - (     ) = {result}'
                        case 2:
                            return f'{a} - {b} ='

        else:  # num_count == 3
            a,b,c = 0,0,0
            op = random.choice(['+', '-'])  # 确保至少有一个运算符
            match op:
                case '+':
                    op2 = random.choice(['×', '÷'])  # 确保至少有一个乘除法
                    firstPos = random.choice([True, False])
                    match op2:
                        case '×':
                            a = random.randint(2, 9)
                            b = random.randint(2, 9)
                            c = random.randint(1, 999-a*b)
                        case '÷':
                            a = random.randint(2, 9)
                            b = random.randint(2, 9)
                            a = a*b
                            c = random.randint(1, 999-a)

                    if firstPos:
                        return f'{a} {op2} {b} {op} {c} ='
                    else:
                        return f'{c} {op} {a} {op2} {b} ='
                case '-':
                    op2 = random.choice(['×', '÷'])  # 确保至少有一个乘除法
                    firstPos = random.choice([True, False])
                    match op2:
                        case '×':
                            a = random.randint(2, 9)
                            b = random.randint(2, 9)
                            if firstPos:
                                c = random.randint(1, a*b-1)
                            else:
                                c = random.randint(a*b+1, 999)
                        case '÷':
                            a = random.randint(2, 9)
                            b = random.randint(2, 9)
                            a = a*b
                            if firstPos:
                                c = random.randint(1, a-1)
                            else:
                                c = random.randint(a+1, 999)
                    if firstPos:
                        return f'{a} {op2} {b} {op} {c} ='
                    else:
                        return f'{c} {op} {a} {op2} {b} ='

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

    def generate_problems(self):
        """生成题目并创建PDF"""
        pages = self.pages_spinbox.value()
        cols = self.cols_spinbox.value()
        per_col = self.per_col_spinbox.value()
        font_size = self.font_spinbox.value()

        # 获取运算设置
        num_count = 2 if self.num_count_combo.currentText() == '2个数字' else 3
        has_multiply = self.multiply_check.isChecked()
        has_divide = self.divide_check.isChecked()

        total_problems = pages * per_col * cols

        try:
            # 生成所有题目
            problems = [self.generate_expression(num_count, has_multiply, has_divide)
                       for _ in range(total_problems)]

            # 选择保存位置
            filename, _ = QFileDialog.getSaveFileName(
                self, '保存PDF文件', '数学题目.pdf', 'PDF文件 (*.pdf)')

            if filename:
                # 创建PDF
                self.create_pdf(filename, problems, cols, font_size, per_col)
                QMessageBox.information(
                    self, '成功',
                    f'已生成{total_problems}道题目到\n{filename}')

        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成失败：{str(e)}')

if __name__ == '__main__':
    # 启动应用程序
    app = QApplication(sys.argv)
    window = MathProblemGenerator()
    window.show()
    sys.exit(app.exec())
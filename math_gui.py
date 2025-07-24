import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QSpinBox, QPushButton,
                             QFileDialog, QMessageBox)
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
        self.pages_spinbox.setValue(5)
        pages_layout.addWidget(self.pages_spinbox)
        pages_layout.addStretch()

        # 列数设置
        cols_layout = QHBoxLayout()
        cols_layout.addWidget(QLabel('每页列数:'))
        self.cols_spinbox = QSpinBox()
        self.cols_spinbox.setRange(1, 5)
        self.cols_spinbox.setValue(3)
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
        self.font_spinbox.setValue(16)
        self.font_spinbox.valueChanged.connect(self.update_preview)
        font_layout.addWidget(self.font_spinbox)
        font_layout.addStretch()

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

    def generate_expression(self):
        """生成单个数学表达式

        返回格式：
        - 加法：(     ) + b = a 或 b + (     ) = a
        - 减法：(     ) - b = a-b 或 a - (     ) = b

        确保减法结果为正数
        """
        operator = random.choice(['+', '-'])
        a = random.randint(1, 99)
        b = random.randint(1, 99)
        a, b = max(a, b), min(a, b)  # 确保a >= b，减法结果为正

        bracket_pos = random.choice([0, 1])  # 括号位置：0=左边，1=右边

        if bracket_pos == 0:
            if operator == "+":
                return f'(     ) + {b} = {a}'
            else:
                return f'(     ) - {b} = {a - b}'
        else:
            if operator == "+":
                return f'{b} + (     ) = {a}'
            else:
                return f'{a} - (     ) = {b}'

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
                                   topMargin=36, bottomMargin=18)

        # 计算可用的列高度 (letter页面高度 - 上下边距)
        available_height = letter[1] - 36 - 18  # topMargin + bottomMargin

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

        total_problems = pages * per_col * cols

        try:
            # 生成所有题目
            problems = [self.generate_expression() for _ in range(total_problems)]

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
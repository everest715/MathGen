import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QSpinBox, QPushButton, 
                             QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Preformatted
from reportlab.lib.units import inch

class MathProblemGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('数学题目生成器')
        self.setGeometry(100, 100, 400, 300)
        self.init_ui()

    def init_ui(self):
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
        self.per_col_spinbox.setRange(10, 50)
        self.per_col_spinbox.setValue(25)
        per_col_layout.addWidget(self.per_col_spinbox)
        per_col_layout.addStretch()
        
        # 生成按钮
        self.generate_btn = QPushButton('生成PDF')
        self.generate_btn.clicked.connect(self.generate_problems)
        
        # 添加到主布局
        layout.addLayout(pages_layout)
        layout.addLayout(cols_layout)
        layout.addLayout(per_col_layout)
        layout.addWidget(self.generate_btn)
        layout.addStretch()
        
        central_widget.setLayout(layout)

    def generate_expression(self):
        operator = random.choice(['+', '-'])
        a = random.randint(1, 99)
        b = random.randint(1, 99)
        a, b = max(a, b), min(a, b)

        bracket_pos = random.choice([0, 1])

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

    def create_pdf(self, filename, problems, cols=3):
        class MultiColumnDocTemplate(BaseDocTemplate):
            def __init__(self, filename, cols=3, **kwargs):
                super().__init__(filename, **kwargs)
                self.cols = cols
                
            def build(self, flowables, **kwargs):
                frame_width = (self.width) / self.cols
                frames = []
                for i in range(self.cols):
                    left = self.leftMargin + i * frame_width
                    width = frame_width - 12
                    frame = Frame(left, self.bottomMargin, 
                                width, self.height, 
                                leftPadding=6, rightPadding=6)
                    frames.append(frame)
                
                template = PageTemplate(frames=frames)
                self.addPageTemplates([template])
                super().build(flowables, **kwargs)

        doc = MultiColumnDocTemplate(filename, cols=cols,
                                   pagesize=letter,
                                   rightMargin=48, leftMargin=48,
                                   topMargin=36, bottomMargin=18)

        styles = getSampleStyleSheet()
        style = styles['Normal']
        style.fontSize = 16
        style.leading = 22

        content = []
        for i, prob in enumerate(problems):
            p = Preformatted(f"{i+1}. {prob}", style)
            content.append(p)

        doc.build(content)

    def generate_problems(self):
        pages = self.pages_spinbox.value()
        cols = self.cols_spinbox.value()
        per_col = self.per_col_spinbox.value()
        
        total_problems = pages * per_col * cols
        
        try:
            problems = [self.generate_expression() for _ in range(total_problems)]
            
            filename, _ = QFileDialog.getSaveFileName(
                self, '保存PDF文件', '数学题目.pdf', 'PDF文件 (*.pdf)')
            
            if filename:
                self.create_pdf(filename, problems, cols)
                QMessageBox.information(
                    self, '成功', 
                    f'已生成{total_problems}道题目到\n{filename}')
                
        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成失败：{str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MathProblemGenerator()
    window.show()
    sys.exit(app.exec())
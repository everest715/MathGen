import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QSpinBox, QPushButton,
                             QFileDialog, QMessageBox, QComboBox, QCheckBox)
from PyQt6.QtCore import Qt
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Preformatted, BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.units import inch
from math_engine import MathExpressionEngine, Constants

class MathProblemGeneratorUI(QMainWindow):
    """数学题目生成器UI界面类

    功能：
    - 提供用户界面控件
    - 处理用户交互
    - 调用算式生成引擎
    - 生成PDF文件
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle('数学题目生成器')
        self.setGeometry(100, 100, 400, 300)
        
        # 初始化算式生成引擎
        self.math_engine = MathExpressionEngine()
        
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

    def _create_basic_controls(self, layout):
        """创建基本控件"""
        # 数字范围设置
        number_range_group = QWidget()
        number_range_layout = QHBoxLayout()
        number_range_layout.addWidget(QLabel('数字范围:'))
        
        self.min_number_spinbox = QSpinBox()
        self.min_number_spinbox.setRange(Constants.MIN_RANGE_VALUE, Constants.MAX_RANGE_VALUE)
        self.min_number_spinbox.setValue(Constants.DEFAULT_MIN_NUMBER)
        number_range_layout.addWidget(self.min_number_spinbox)
        
        number_range_layout.addWidget(QLabel('到'))
        
        self.max_number_spinbox = QSpinBox()
        self.max_number_spinbox.setRange(Constants.MIN_RANGE_VALUE, Constants.MAX_RANGE_VALUE)
        self.max_number_spinbox.setValue(Constants.DEFAULT_MAX_NUMBER)
        number_range_layout.addWidget(self.max_number_spinbox)
        
        number_range_group.setLayout(number_range_layout)
        layout.addWidget(number_range_group)
        
        # 结果范围设置
        result_range_group = QWidget()
        result_range_layout = QHBoxLayout()
        result_range_layout.addWidget(QLabel('结果范围:'))
        
        self.min_result_spinbox = QSpinBox()
        self.min_result_spinbox.setRange(Constants.MIN_RANGE_VALUE, Constants.MAX_RANGE_VALUE)
        self.min_result_spinbox.setValue(Constants.DEFAULT_MIN_RESULT)
        result_range_layout.addWidget(self.min_result_spinbox)
        
        result_range_layout.addWidget(QLabel('到'))
        
        self.max_result_spinbox = QSpinBox()
        self.max_result_spinbox.setRange(Constants.MIN_RANGE_VALUE, Constants.MAX_RANGE_VALUE)
        self.max_result_spinbox.setValue(Constants.DEFAULT_MAX_RESULT)
        result_range_layout.addWidget(self.max_result_spinbox)
        
        result_range_group.setLayout(result_range_layout)
        layout.addWidget(result_range_group)
        
        # 页数设置
        pages_layout, self.pages_spinbox = self._create_spinbox_layout(
            '页数:', 1, Constants.MAX_PAGES, Constants.DEFAULT_PAGES)
        layout.addLayout(pages_layout)

        # 列数设置
        cols_layout, self.cols_spinbox = self._create_spinbox_layout(
            '每页列数:', 1, Constants.MAX_COLS, Constants.DEFAULT_COLS, self.update_preview)
        layout.addLayout(cols_layout)

        # 每列题目数设置
        per_col_layout, self.per_col_spinbox = self._create_spinbox_layout(
            '每列题数:', Constants.MIN_PER_COL, Constants.MAX_PER_COL, 
            Constants.DEFAULT_PER_COL, self.update_preview)
        layout.addLayout(per_col_layout)

        # 字号设置
        font_layout, self.font_spinbox = self._create_spinbox_layout(
            '字号:', Constants.MIN_FONT_SIZE, Constants.MAX_FONT_SIZE, 
            Constants.DEFAULT_FONT_SIZE, self.update_preview)
        layout.addLayout(font_layout)
        
        # 数字范围设置
        number_range_layout = QHBoxLayout()
        number_range_layout.addWidget(QLabel('数字范围:'))
        
        self.min_number_spinbox = QSpinBox()
        self.min_number_spinbox.setRange(Constants.MIN_RANGE_VALUE, Constants.MAX_RANGE_VALUE)
        self.min_number_spinbox.setValue(Constants.DEFAULT_MIN_NUMBER)
        number_range_layout.addWidget(self.min_number_spinbox)
        
        number_range_layout.addWidget(QLabel('到'))
        
        self.max_number_spinbox = QSpinBox()
        self.max_number_spinbox.setRange(Constants.MIN_RANGE_VALUE, Constants.MAX_RANGE_VALUE)
        self.max_number_spinbox.setValue(Constants.DEFAULT_MAX_NUMBER)
        number_range_layout.addWidget(self.max_number_spinbox)
        
        number_range_layout.addStretch()
        layout.addLayout(number_range_layout)
        
        # 结果范围设置
        result_range_layout = QHBoxLayout()
        result_range_layout.addWidget(QLabel('结果范围:'))
        
        self.min_result_spinbox = QSpinBox()
        self.min_result_spinbox.setRange(Constants.MIN_RANGE_VALUE, Constants.MAX_RANGE_VALUE)
        self.min_result_spinbox.setValue(Constants.DEFAULT_MIN_RESULT)
        result_range_layout.addWidget(self.min_result_spinbox)
        
        result_range_layout.addWidget(QLabel('到'))
        
        self.max_result_spinbox = QSpinBox()
        self.max_result_spinbox.setRange(Constants.MIN_RANGE_VALUE, Constants.MAX_RANGE_VALUE)
        self.max_result_spinbox.setValue(Constants.DEFAULT_MAX_RESULT)
        result_range_layout.addWidget(self.max_result_spinbox)
        
        result_range_layout.addStretch()
        layout.addLayout(result_range_layout)
    
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
        """更新总题数预览"""
        pages = self.pages_spinbox.value()
        cols = self.cols_spinbox.value()
        per_col = self.per_col_spinbox.value()
        total = pages * cols * per_col
        self.preview_label.setText(f'总题数: {total}')
    
    def _validate_settings(self):
        """验证用户设置"""
        errors = []
        
        pages = self.pages_spinbox.value()
        cols = self.cols_spinbox.value()
        per_col = self.per_col_spinbox.value()
        total_problems = pages * per_col * cols
        
        if total_problems > Constants.MAX_TOTAL_PROBLEMS:
            errors.append(f'总题数过多({total_problems})，建议不超过{Constants.MAX_TOTAL_PROBLEMS}题')
        
        if total_problems == 0:
            errors.append('题目数量不能为0')
        
        # 验证数字范围
        min_num = self.min_number_spinbox.value()
        max_num = self.max_number_spinbox.value()
        if min_num > max_num:
            errors.append('数字范围设置错误：最小值不能大于最大值')
        
        # 验证结果范围
        min_result = self.min_result_spinbox.value()
        max_result = self.max_result_spinbox.value()
        if min_result > max_result:
            errors.append('结果范围设置错误：最小值不能大于最大值')
        
        # 验证范围的合理性
        if min_num < Constants.MIN_RANGE_VALUE or max_num > Constants.MAX_RANGE_VALUE:
            errors.append(f'数字范围应在{Constants.MIN_RANGE_VALUE}-{Constants.MAX_RANGE_VALUE}之间')
        
        if min_result < Constants.MIN_RANGE_VALUE or max_result > Constants.MAX_RANGE_VALUE:
            errors.append(f'结果范围应在{Constants.MIN_RANGE_VALUE}-{Constants.MAX_RANGE_VALUE}之间')
            
        return errors
    

    
    def generate_problems(self):
        """生成PDF文件"""
        # 验证设置
        errors = self._validate_settings()
        if errors:
            QMessageBox.warning(self, '设置错误', '\n'.join(errors))
            return
        
        # 选择保存文件
        filename, _ = QFileDialog.getSaveFileName(
            self, '保存PDF文件', 'math_problems.pdf', 'PDF文件 (*.pdf)'
        )
        
        if not filename:
            return
        
        try:
            # 获取设置
            pages = self.pages_spinbox.value()
            cols = self.cols_spinbox.value()
            per_col = self.per_col_spinbox.value()
            font_size = self.font_spinbox.value()
            
            # 计算总题数
            total_problems = pages * cols * per_col
            
            # 更新算式引擎的范围设置
            self.math_engine.update_ranges(
                self.min_number_spinbox.value(),
                self.max_number_spinbox.value(),
                self.min_result_spinbox.value(),
                self.max_result_spinbox.value()
            )
            
            # 获取运算设置
            num_count = 3 if self.num_count_combo.currentText() == '3个数字' else 2
            include_multiply = self.multiply_check.isChecked()
            include_divide = self.divide_check.isChecked()
            
            # 生成题目
            problems = []
            for _ in range(total_problems):
                problem = self.math_engine.generate_expression(
                    num_count=num_count,
                    include_multiply=include_multiply,
                    include_divide=include_divide
                )
                problems.append(problem)
            
            # 创建PDF
            self.create_pdf(filename, problems, cols, font_size)
            
            QMessageBox.information(self, '成功', f'PDF文件已生成: {filename}')
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成PDF时出错: {str(e)}')
    
    def create_pdf(self, filename, problems, cols, font_size):
        """创建PDF文件"""
        class MultiColumnDocTemplate(BaseDocTemplate):
            def __init__(self, filename, cols, **kwargs):
                BaseDocTemplate.__init__(self, filename, **kwargs)
                self.cols = cols
                
                # 计算每列的宽度
                frame_width = (self.width) / cols
                frames = []
                
                for i in range(self.cols):
                    left = self.leftMargin + i * frame_width
                    width = frame_width - Constants.PDF_FRAME_SPACING  # 留出间距
                    frame = Frame(left, 0,
                                width, self.height,
                                leftPadding=Constants.PDF_FRAME_PADDING, bottomPadding=0, 
                                rightPadding=Constants.PDF_FRAME_PADDING, topPadding=0)
                    frames.append(frame)

                template = PageTemplate(id='multi_col', frames=frames)
                self.addPageTemplates([template])
        
        # 创建文档
        doc = MultiColumnDocTemplate(filename, cols=cols,
                                   pagesize=letter,
                                   rightMargin=Constants.PDF_MARGIN, leftMargin=Constants.PDF_MARGIN,
                                   topMargin=Constants.PDF_TOP_MARGIN, bottomMargin=Constants.PDF_BOTTOM_MARGIN)

        # 计算可用的列高度 (letter页面高度 - 上下边距)
        available_height = letter[1] - Constants.PDF_TOP_MARGIN - Constants.PDF_BOTTOM_MARGIN

        # 计算每道题目的最大高度，确保每列不超过指定数量
        problems_per_col = len(problems) // cols
        if len(problems) % cols != 0:
            problems_per_col += 1
        
        max_line_height = available_height / problems_per_col if problems_per_col > 0 else 20
        line_height = min(max_line_height, font_size * 1.5)  # 行高不超过字号的1.5倍
        
        # 创建样式
        styles = getSampleStyleSheet()
        style = styles['Normal']
        style.fontSize = font_size
        style.leading = line_height
        style.fontName = 'Helvetica'
        
        # 创建内容
        story = []
        for problem in problems:
            p = Preformatted(problem, style)
            story.append(p)
        
        # 生成PDF
        doc.build(story)
    


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = MathProblemGeneratorUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
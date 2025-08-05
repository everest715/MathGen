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
        pages_group = QWidget()
        pages_layout = QHBoxLayout()
        pages_layout.addWidget(QLabel('页数:'))
        self.pages_spinbox = QSpinBox()
        self.pages_spinbox.setRange(1, 100)
        self.pages_spinbox.setValue(10)
        self.pages_spinbox.valueChanged.connect(self.update_preview)
        pages_layout.addWidget(self.pages_spinbox)
        pages_group.setLayout(pages_layout)
        layout.addWidget(pages_group)

        # 列数设置
        cols_group = QWidget()
        cols_layout = QHBoxLayout()
        cols_layout.addWidget(QLabel('列数:'))
        self.cols_spinbox = QSpinBox()
        self.cols_spinbox.setRange(1, 5)
        self.cols_spinbox.setValue(3)
        self.cols_spinbox.valueChanged.connect(self.update_preview)
        cols_layout.addWidget(self.cols_spinbox)
        cols_group.setLayout(cols_layout)
        layout.addWidget(cols_group)

        # 每列题数设置
        per_col_group = QWidget()
        per_col_layout = QHBoxLayout()
        per_col_layout.addWidget(QLabel('每列题数:'))
        self.per_col_spinbox = QSpinBox()
        self.per_col_spinbox.setRange(5, 50)
        self.per_col_spinbox.setValue(25)
        self.per_col_spinbox.valueChanged.connect(self.update_preview)
        per_col_layout.addWidget(self.per_col_spinbox)
        per_col_group.setLayout(per_col_layout)
        layout.addWidget(per_col_group)

        # 字号设置
        font_group = QWidget()
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel('字号:'))
        self.font_spinbox = QSpinBox()
        self.font_spinbox.setRange(12, 24)
        self.font_spinbox.setValue(16)
        font_layout.addWidget(self.font_spinbox)
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)

        # 总题数预览
        self.preview_label = QLabel('总题数: 0')
        layout.addWidget(self.preview_label)
    
    def _create_operation_controls(self, layout):
        """创建运算类型控件"""
        operation_group = QWidget()
        operation_layout = QVBoxLayout()
        
        operation_layout.addWidget(QLabel('运算类型:'))
        
        # 运算类型选择
        self.operation_combo = QComboBox()
        self.operation_combo.addItems(['加法', '减法', '乘法', '除法', '混合运算'])
        operation_layout.addWidget(self.operation_combo)
        
        operation_group.setLayout(operation_layout)
        layout.addWidget(operation_group)
    
    def _create_action_controls(self, layout):
        """创建操作按钮"""
        # 生成PDF按钮
        self.generate_button = QPushButton('生成PDF')
        self.generate_button.clicked.connect(self.generate_pdf)
        layout.addWidget(self.generate_button)
    
    def update_preview(self):
        """更新总题数预览"""
        pages = self.pages_spinbox.value()
        cols = self.cols_spinbox.value()
        per_col = self.per_col_spinbox.value()
        total = pages * cols * per_col
        self.preview_label.setText(f'总题数: {total}')
    
    def _validate_settings(self):
        """验证设置的有效性"""
        errors = []
        
        # 验证总题数
        total_problems = self.pages_spinbox.value() * self.cols_spinbox.value() * self.per_col_spinbox.value()
        if total_problems > Constants.MAX_TOTAL_PROBLEMS:
            errors.append(f'总题数不能超过{Constants.MAX_TOTAL_PROBLEMS}题')
        
        # 获取范围值
        min_num = self.min_number_spinbox.value()
        max_num = self.max_number_spinbox.value()
        min_result = self.min_result_spinbox.value()
        max_result = self.max_result_spinbox.value()
        
        # 验证范围的合理性
        if min_num > max_num:
            errors.append('数字范围最小值不能大于最大值')
        
        if min_result > max_result:
            errors.append('结果范围最小值不能大于最大值')
        
        # 验证范围的合理性
        if min_num < Constants.MIN_RANGE_VALUE or max_num > Constants.MAX_RANGE_VALUE:
            errors.append(f'数字范围应在{Constants.MIN_RANGE_VALUE}-{Constants.MAX_RANGE_VALUE}之间')
        
        if min_result < Constants.MIN_RANGE_VALUE or max_result > Constants.MAX_RANGE_VALUE:
            errors.append(f'结果范围应在{Constants.MIN_RANGE_VALUE}-{Constants.MAX_RANGE_VALUE}之间')
            
        return errors
    
    def _get_operation_settings(self):
        """获取运算设置"""
        operation_map = {
            '加法': 'addition',
            '减法': 'subtraction', 
            '乘法': 'multiplication',
            '除法': 'division',
            '混合运算': 'mixed'
        }
        
        selected_text = self.operation_combo.currentText()
        return operation_map.get(selected_text, 'mixed')
    
    def generate_problems(self, operation_type, count):
        """生成指定数量的题目"""
        # 更新算式引擎的范围设置
        self.math_engine.update_ranges(
            self.min_number_spinbox.value(),
            self.max_number_spinbox.value(),
            self.min_result_spinbox.value(),
            self.max_result_spinbox.value()
        )
        
        problems = []
        for _ in range(count):
            problem = self.math_engine.generate_expression(operation_type)
            problems.append(problem)
        return problems
    
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
    
    def generate_pdf(self):
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
            operation_type = self._get_operation_settings()
            
            # 计算总题数
            total_problems = pages * cols * per_col
            
            # 生成题目
            problems = self.generate_problems(operation_type, total_problems)
            
            # 创建PDF
            self.create_pdf(filename, problems, cols, font_size)
            
            QMessageBox.information(self, '成功', f'PDF文件已生成: {filename}')
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成PDF时出错: {str(e)}')

def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = MathProblemGeneratorUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
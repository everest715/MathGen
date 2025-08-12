"""PDF生成器

包含所有PDF文档生成相关的逻辑
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Preformatted, BaseDocTemplate, Frame, PageTemplate
import os
from constants import Constants

class PDFGenerator:
    """PDF生成器"""
    
    def __init__(self):
        """初始化PDF生成器"""
        self.register_fonts()
    
    def register_fonts(self):
        """注册中文字体"""
        try:
            # 尝试注册系统中的中文字体
            font_paths = [
                'C:/Windows/Fonts/simsun.ttc',  # 宋体
                'C:/Windows/Fonts/simhei.ttf',  # 黑体
                'C:/Windows/Fonts/msyh.ttc',    # 微软雅黑
                '/System/Library/Fonts/PingFang.ttc',  # macOS
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'  # Linux
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                        self.font_name = 'ChineseFont'
                        return
                    except Exception:
                        continue
            
            # 如果没有找到中文字体，使用默认字体
            self.font_name = 'Helvetica'
            
        except Exception:
            self.font_name = 'Helvetica'
    
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
                    width = frame_width - Constants.PDF_FRAME_SPACING  # 留出间距
                    frame = Frame(left, 0,
                                width, self.height,
                                leftPadding=Constants.PDF_FRAME_PADDING, bottomPadding=0, 
                                rightPadding=Constants.PDF_FRAME_PADDING, topPadding=0)
                    frames.append(frame)

                template = PageTemplate(frames=frames)
                self.addPageTemplates([template])
                super().build(flowables, **kwargs)

        # 创建PDF文档
        doc = MultiColumnDocTemplate(filename, cols=cols,
                                   pagesize=letter,
                                   rightMargin=Constants.PDF_MARGIN, leftMargin=Constants.PDF_MARGIN,
                                   topMargin=Constants.PDF_TOP_MARGIN, bottomMargin=Constants.PDF_BOTTOM_MARGIN)

        # 计算可用的列高度 (letter页面高度 - 上下边距)
        available_height = letter[1] - Constants.PDF_TOP_MARGIN - Constants.PDF_BOTTOM_MARGIN

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
    

    
    def get_save_filename(self, save_path, has_addition, has_subtraction, has_multiplication, has_division, has_mixed):
        """生成保存文件名
        
        参数:
            save_path: 用户指定的保存路径
            has_addition: 是否包含加法
            has_subtraction: 是否包含减法
            has_multiplication: 是否包含乘法
            has_division: 是否包含除法
            has_mixed: 是否包含混合运算
            
        返回:
            最终的保存文件名
        """
        if save_path and save_path.strip():
            return save_path.strip()
        
        # 根据选择的运算类型生成默认文件名
        operation_types = []
        if has_addition:
            operation_types.append("加法")
        if has_subtraction:
            operation_types.append("减法")
        if has_multiplication:
            operation_types.append("乘法")
        if has_division:
            operation_types.append("除法")
        if has_mixed:
            operation_types.append("混合运算")
        
        if operation_types:
            operation_str = "_".join(operation_types)
            return f"数学题_{operation_str}.pdf"
        else:
            return Constants.DEFAULT_SAVE_PATH
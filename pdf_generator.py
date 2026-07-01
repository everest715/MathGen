"""PDF生成器

包含所有PDF文档生成相关的逻辑
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Preformatted, BaseDocTemplate, Frame, PageTemplate
import os
from typing import Optional
from constants import Constants


class MultiColumnDocTemplate(BaseDocTemplate):
    """多列PDF文档模板"""

    def __init__(self, filename, cols=3, **kwargs):
        super().__init__(filename, **kwargs)
        self.cols = cols

    def build(self, flowables, **kwargs):
        """构建多列布局"""
        frame_width = self.width / self.cols
        frames = []
        for i in range(self.cols):
            left = self.leftMargin + i * frame_width
            width = frame_width - Constants.PDF_FRAME_SPACING
            frame = Frame(left, 0,
                        width, self.height,
                        leftPadding=Constants.PDF_FRAME_PADDING, bottomPadding=0,
                        rightPadding=Constants.PDF_FRAME_PADDING, topPadding=0)
            frames.append(frame)

        template = PageTemplate(frames=frames)
        self.addPageTemplates([template])
        super().build(flowables, **kwargs)


class PDFGenerator:
    """PDF生成器"""

    def __init__(self):
        """初始化PDF生成器"""
        self.register_fonts()

    def register_fonts(self):
        """注册中文字体"""
        font_configs = [
            ('C:/Windows/Fonts/simsun.ttc', 'ChineseFont'),
            ('C:/Windows/Fonts/simhei.ttf', 'ChineseFont'),
            ('C:/Windows/Fonts/msyh.ttc', 'ChineseFont'),
            ('/System/Library/Fonts/PingFang.ttc', 'ChineseFont'),
            ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 'ChineseFont')
        ]

        self.font_name = 'Helvetica'

        for font_path, font_name in font_configs:
            if self._try_register_font(font_path, font_name):
                self.font_name = font_name
                break

    def _try_register_font(self, font_path, font_name):
        """尝试注册单个字体"""
        try:
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                return True
        except Exception:
            pass
        return False

    def create_pdf(self, filename, problems, cols=3, font_size=16, per_col=25):
        """创建PDF文档

        参数：
            filename: 输出文件名
            problems: 题目列表
            cols: 每页列数
            font_size: 题目字号大小
            per_col: 每列题目数量
        """
        doc = MultiColumnDocTemplate(filename, cols=cols,
                                   pagesize=A4,
                                   rightMargin=Constants.PDF_MARGIN, leftMargin=Constants.PDF_MARGIN,
                                   topMargin=Constants.PDF_TOP_MARGIN, bottomMargin=Constants.PDF_BOTTOM_MARGIN)

        available_height = A4[1] - Constants.PDF_TOP_MARGIN - Constants.PDF_BOTTOM_MARGIN
        max_line_height = available_height / per_col

        styles = getSampleStyleSheet()
        style = styles['Normal']
        style.fontSize = font_size
        style.leading = max_line_height - font_size / inch

        content = [Preformatted(prob, style) for prob in problems]
        doc.build(content)

    def get_save_filename(self,
                         save_path: Optional[str],
                         has_addition: bool,
                         has_subtraction: bool,
                         has_multiplication: bool,
                         has_division: bool,
                         has_division_no_remainder: bool) -> str:
        """生成保存文件名"""
        if save_path and save_path.strip():
            return save_path.strip()

        selected = []
        if has_addition: selected.append('加法')
        if has_subtraction: selected.append('减法')
        if has_multiplication: selected.append('乘法')
        if has_division: selected.append('除法')
        if has_division_no_remainder: selected.append('除法')

        if selected:
            return f"数学题_{'_'.join(selected)}.pdf"
        return Constants.DEFAULT_SAVE_PATH

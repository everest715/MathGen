"""PDF生成器

包含所有PDF文档生成相关的逻辑
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
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
    
    def create_pdf(self, problems, save_path, rows_per_page, cols_per_page, total_pages, font_size):
        """创建PDF文件
        
        参数:
            problems: 题目列表
            save_path: 保存路径
            rows_per_page: 每页行数
            cols_per_page: 每页列数
            total_pages: 总页数
            font_size: 字体大小
        """
        try:
            # 创建PDF画布
            c = canvas.Canvas(save_path, pagesize=A4)
            
            # 设置字体
            c.setFont(self.font_name, font_size)
            
            # 计算页面布局
            page_width, page_height = A4
            margin = Constants.PDF_MARGIN * mm
            
            # 计算可用空间
            usable_width = page_width - 2 * margin
            usable_height = page_height - 2 * margin
            
            # 计算每个题目的空间
            col_width = usable_width / cols_per_page
            row_height = usable_height / rows_per_page
            
            # 生成每一页
            problems_per_page = rows_per_page * cols_per_page
            problem_index = 0
            
            for page in range(total_pages):
                if page > 0:
                    c.showPage()  # 新建页面
                    c.setFont(self.font_name, font_size)
                
                # 在当前页面绘制题目
                for row in range(rows_per_page):
                    for col in range(cols_per_page):
                        if problem_index < len(problems):
                            # 计算题目位置
                            x = margin + col * col_width
                            y = page_height - margin - (row + 1) * row_height + row_height * 0.3
                            
                            # 绘制题目
                            problem_text = f"{problem_index + 1}. {problems[problem_index]}"
                            c.drawString(x, y, problem_text)
                            
                            problem_index += 1
                        else:
                            break
                    
                    if problem_index >= len(problems):
                        break
            
            # 保存PDF
            c.save()
            return True
            
        except Exception as e:
            raise Exception(f"PDF生成失败: {str(e)}")
    
    def validate_pdf_settings(self, rows_per_page, cols_per_page, total_pages, font_size):
        """验证PDF设置参数
        
        参数:
            rows_per_page: 每页行数
            cols_per_page: 每页列数
            total_pages: 总页数
            font_size: 字体大小
            
        返回:
            (is_valid, error_message)
        """
        try:
            # 验证每页行数
            if not (Constants.MIN_ROWS_PER_PAGE <= rows_per_page <= Constants.MAX_ROWS_PER_PAGE):
                return False, f"每页行数必须在{Constants.MIN_ROWS_PER_PAGE}-{Constants.MAX_ROWS_PER_PAGE}之间"
            
            # 验证每页列数
            if not (Constants.MIN_COLS_PER_PAGE <= cols_per_page <= Constants.MAX_COLS_PER_PAGE):
                return False, f"每页列数必须在{Constants.MIN_COLS_PER_PAGE}-{Constants.MAX_COLS_PER_PAGE}之间"
            
            # 验证总页数
            if not (Constants.MIN_TOTAL_PAGES <= total_pages <= Constants.MAX_TOTAL_PAGES):
                return False, f"总页数必须在{Constants.MIN_TOTAL_PAGES}-{Constants.MAX_TOTAL_PAGES}之间"
            
            # 验证字体大小
            if not (Constants.MIN_FONT_SIZE <= font_size <= Constants.MAX_FONT_SIZE):
                return False, f"字体大小必须在{Constants.MIN_FONT_SIZE}-{Constants.MAX_FONT_SIZE}之间"
            
            return True, ""
            
        except Exception as e:
            return False, f"参数验证失败: {str(e)}"
    
    def calculate_total_problems(self, rows_per_page, cols_per_page, total_pages):
        """计算总题目数量
        
        参数:
            rows_per_page: 每页行数
            cols_per_page: 每页列数
            total_pages: 总页数
            
        返回:
            总题目数量
        """
        return rows_per_page * cols_per_page * total_pages
    
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
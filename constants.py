"""常量定义模块

包含数学题目生成器的所有常量定义
"""

class Constants:
    """常量定义"""
    # 计算结果的最大最小值
    MAX_RESULT = 999
    MIN_RESULT = 1
    
    # 乘数的最大最小值（除法中计算除数时也使用这个定义）
    MIN_MULTIPLICATION_FACTOR = 2
    MAX_MULTIPLICATION_FACTOR = 9
    
    # UI配置
    WINDOW_TITLE = "数学题生成器"
    WINDOW_SIZE = "600x580"
    DEFAULT_PAGES = 10
    DEFAULT_COLS = 3
    DEFAULT_PER_COL = 25
    DEFAULT_FONT_SIZE = 16
    
    # 页面设置默认值
    DEFAULT_ROWS_PER_PAGE = 10
    DEFAULT_COLS_PER_PAGE = 3
    DEFAULT_TOTAL_PAGES = 10
    
    # 页面设置范围
    MIN_ROWS_PER_PAGE = 1
    MAX_ROWS_PER_PAGE = 20
    MIN_COLS_PER_PAGE = 1
    MAX_COLS_PER_PAGE = 5
    MIN_TOTAL_PAGES = 1
    MAX_TOTAL_PAGES = 100
    
    # 保存路径
    DEFAULT_SAVE_PATH = "数学题.pdf"
    
    # 数字数量选择
    DEFAULT_NUM_COUNT = 2
    NUM_COUNT_OPTIONS = ['2个数字', '3个数字']
    
    # 范围限制
    MAX_PAGES = 100
    MAX_COLS = 5
    MIN_PER_COL = 5
    MAX_PER_COL = 50
    MIN_FONT_SIZE = 12
    MAX_FONT_SIZE = 24
    
    # 数字和结果范围常量
    MIN_RANGE_VALUE = 1
    MAX_RANGE_VALUE = 999
    DEFAULT_MIN_NUMBER = 1
    DEFAULT_MAX_NUMBER = 100
    DEFAULT_MIN_RESULT = 1
    DEFAULT_MAX_RESULT = 100
    
    # PDF生成相关常量
    PDF_MARGIN = 48
    PDF_TOP_MARGIN = 18
    PDF_BOTTOM_MARGIN = 36
    PDF_FRAME_PADDING = 6
    PDF_FRAME_SPACING = 12
    
    # 错误处理
    MAX_TOTAL_PROBLEMS = 10000
    MAX_GENERATION_ATTEMPTS = 10
    DEFAULT_PROBLEM = '1 + 1 ='
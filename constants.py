"""常量定义模块

包含数学题目生成器的所有常量定义，按功能分组组织
"""

class Constants:
    """数学题生成器常量定义类"""
    
    # ==================== UI界面配置 ====================
    WINDOW_TITLE = "数学题生成器"
    WINDOW_SIZE = "600x580"
    
    # ==================== 数学运算配置 ====================
    # 乘除法因子范围
    MIN_MULTIPLICATION_FACTOR = 2
    MAX_MULTIPLICATION_FACTOR = 9
    
    # 数字数量选择
    DEFAULT_NUM_COUNT = 2
    NUM_COUNT_OPTIONS = ['2个数字', '3个数字']
    
    # ==================== 数字和结果范围 ====================
    # 全局范围限制
    MIN_RANGE_VALUE = 1
    MAX_RANGE_VALUE = 999
    
    # 默认数字范围
    DEFAULT_MIN_NUMBER = 1
    DEFAULT_MAX_NUMBER = 999
    
    # 默认结果范围
    DEFAULT_MIN_RESULT = 1
    DEFAULT_MAX_RESULT = 999
    
    # 兼容性常量（保持向后兼容）
    MAX_RESULT = MAX_RANGE_VALUE
    MIN_RESULT = MIN_RANGE_VALUE
    
    # ==================== 页面布局配置 ====================
    # 默认页面设置
    DEFAULT_ROWS_PER_PAGE = 25
    DEFAULT_COLS_PER_PAGE = 3
    DEFAULT_TOTAL_PAGES = 10
    DEFAULT_FONT_SIZE = 14
    
    # 页面设置范围
    MIN_ROWS_PER_PAGE = 1
    MAX_ROWS_PER_PAGE = 20
    MIN_COLS_PER_PAGE = 1
    MAX_COLS_PER_PAGE = 5
    MIN_TOTAL_PAGES = 1
    MAX_TOTAL_PAGES = 100
    MIN_FONT_SIZE = 12
    MAX_FONT_SIZE = 24
    
    # 兼容性常量（保持向后兼容）
    DEFAULT_PAGES = DEFAULT_TOTAL_PAGES
    DEFAULT_COLS = DEFAULT_COLS_PER_PAGE
    DEFAULT_PER_COL = DEFAULT_ROWS_PER_PAGE
    MAX_PAGES = MAX_TOTAL_PAGES
    MAX_COLS = MAX_COLS_PER_PAGE
    MIN_PER_COL = MIN_ROWS_PER_PAGE
    MAX_PER_COL = MAX_ROWS_PER_PAGE
    
    # ==================== 文件处理配置 ====================
    DEFAULT_SAVE_PATH = "数学题.pdf"
    
    # ==================== PDF生成配置 ====================
    PDF_MARGIN = 48
    PDF_TOP_MARGIN = 18
    PDF_BOTTOM_MARGIN = 36
    PDF_FRAME_PADDING = 6
    PDF_FRAME_SPACING = 12
    
    # ==================== 错误处理和限制 ====================
    MAX_TOTAL_PROBLEMS = 10000
    MAX_GENERATION_ATTEMPTS = 10
    DEFAULT_PROBLEM = '1 + 1 ='
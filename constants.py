"""常量定义模块

包含数学题目生成器的所有常量定义，按功能分组组织
"""

from typing import Final, List


class Constants:
    """数学题生成器常量定义类
    
    所有配置常量集中管理，按功能模块分组组织
    """
    
    # ==================== UI界面配置 ====================
    WINDOW_TITLE: Final[str] = "数学题生成器"
    WINDOW_SIZE: Final[str] = "600x580"
    
    # ==================== 数学运算配置 ====================
    # 乘除法因子范围
    MIN_MULTIPLICATION_FACTOR: Final[int] = 2
    MAX_MULTIPLICATION_FACTOR: Final[int] = 9
    
    # 数字数量选择
    DEFAULT_NUM_COUNT: Final[int] = 2
    NUM_COUNT_OPTIONS: Final[List[str]] = ['2个数字', '3个数字']
    
    # ==================== 数字和结果范围 ====================
    # 全局范围限制
    MIN_RANGE_VALUE: Final[int] = 1
    MAX_RANGE_VALUE: Final[int] = 999
    
    # 默认数字范围
    DEFAULT_MIN_NUMBER: Final[int] = 1
    DEFAULT_MAX_NUMBER: Final[int] = 999
    
    # 默认结果范围
    DEFAULT_MIN_RESULT: Final[int] = 1
    DEFAULT_MAX_RESULT: Final[int] = 999
    
    # 兼容性常量（保持向后兼容）
    MAX_RESULT: Final[int] = MAX_RANGE_VALUE
    MIN_RESULT: Final[int] = MIN_RANGE_VALUE
    
    # ==================== 页面布局配置 ====================
    # 默认页面设置
    DEFAULT_ROWS_PER_PAGE: Final[int] = 25
    DEFAULT_COLS_PER_PAGE: Final[int] = 4
    DEFAULT_TOTAL_PAGES: Final[int] = 10
    DEFAULT_FONT_SIZE: Final[int] = 12
    
    # 页面设置范围
    MIN_ROWS_PER_PAGE: Final[int] = 1
    MAX_ROWS_PER_PAGE: Final[int] = 20
    MIN_COLS_PER_PAGE: Final[int] = 1
    MAX_COLS_PER_PAGE: Final[int] = 5
    MIN_TOTAL_PAGES: Final[int] = 1
    MAX_TOTAL_PAGES: Final[int] = 100
    MIN_FONT_SIZE: Final[int] = 12
    MAX_FONT_SIZE: Final[int] = 24
    
    # 兼容性常量（保持向后兼容）
    DEFAULT_PAGES: Final[int] = DEFAULT_TOTAL_PAGES
    DEFAULT_COLS: Final[int] = DEFAULT_COLS_PER_PAGE
    DEFAULT_PER_COL: Final[int] = DEFAULT_ROWS_PER_PAGE
    MAX_PAGES: Final[int] = MAX_TOTAL_PAGES
    MAX_COLS: Final[int] = MAX_COLS_PER_PAGE
    MIN_PER_COL: Final[int] = MIN_ROWS_PER_PAGE
    MAX_PER_COL: Final[int] = MAX_ROWS_PER_PAGE
    
    # ==================== 文件处理配置 ====================
    DEFAULT_SAVE_PATH: Final[str] = "数学题.pdf"
    
    # ==================== PDF生成配置 ====================
    PDF_MARGIN: Final[int] = 48
    PDF_TOP_MARGIN: Final[int] = 18
    PDF_BOTTOM_MARGIN: Final[int] = 36
    PDF_FRAME_PADDING: Final[int] = 6
    PDF_FRAME_SPACING: Final[int] = 12
    
    # ==================== 错误处理和限制 ====================
    MAX_TOTAL_PROBLEMS: Final[int] = 10000
    MAX_GENERATION_ATTEMPTS: Final[int] = 10
    DEFAULT_PROBLEM: Final[str] = '1 + 1 ='
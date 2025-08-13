"""用户界面生成器

包含所有用户界面相关的逻辑
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from constants import Constants

class UIGenerator:
    """用户界面生成器"""
    
    def __init__(self, root, generate_callback=None):
        """初始化UI生成器
        
        参数:
            root: tkinter根窗口
            generate_callback: 生成按钮的回调函数
        """
        self.root = root
        self.generate_callback = generate_callback
        self.setup_window()
        self.create_variables()
        self.create_widgets()
        
    def setup_window(self):
        """设置窗口属性"""
        self.root.title(Constants.WINDOW_TITLE)
        self.root.geometry(Constants.WINDOW_SIZE)
        self.root.resizable(False, False)
        
        # 设置窗口居中
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_variables(self):
        """创建界面变量"""
        # 题目类型选择
        self.has_addition = tk.BooleanVar(value=True)
        self.has_subtraction = tk.BooleanVar(value=True)
        self.has_multiplication = tk.BooleanVar(value=False)
        self.has_division = tk.BooleanVar(value=False)
        self.has_mixed = tk.BooleanVar(value=False)
        
        # 数字数量选择
        self.num_count = tk.StringVar(value=Constants.NUM_COUNT_OPTIONS[0])
        
        # 数字范围
        self.min_number = tk.StringVar(value=str(Constants.DEFAULT_MIN_NUMBER))
        self.max_number = tk.StringVar(value=str(Constants.DEFAULT_MAX_NUMBER))
        
        # 结果范围
        self.min_result = tk.StringVar(value=str(Constants.DEFAULT_MIN_RESULT))
        self.max_result = tk.StringVar(value=str(Constants.DEFAULT_MAX_RESULT))
        
        # 页面设置
        self.rows_per_page = tk.StringVar(value=str(Constants.DEFAULT_ROWS_PER_PAGE))
        self.cols_per_page = tk.StringVar(value=str(Constants.DEFAULT_COLS_PER_PAGE))
        self.total_pages = tk.StringVar(value=str(Constants.DEFAULT_TOTAL_PAGES))
        
        # 字体大小
        self.font_size = tk.StringVar(value=str(Constants.DEFAULT_FONT_SIZE))
        
        # 括号位置设置
        self.allow_right_bracket = tk.BooleanVar(value=False)
        
        # 保存路径
        self.save_path = tk.StringVar(value=Constants.DEFAULT_SAVE_PATH)
    
    def create_widgets(self):
        """创建界面组件"""
        # 配置根窗口的grid权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置主框架的grid权重
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 题目类型选择
        self.create_problem_type_frame(main_frame)
        
        # 数字数量选择
        self.create_num_count_frame(main_frame)
        
        # 数字范围设置
        self.create_number_range_frame(main_frame)
        
        # 结果范围设置
        self.create_result_range_frame(main_frame)
        
        # 页面设置
        self.create_page_settings_frame(main_frame)
        
        # 字体设置
        self.create_font_settings_frame(main_frame)
        
        # 括号设置
        self.create_bracket_settings_frame(main_frame)
        
        # 保存路径设置
        self.create_save_path_frame(main_frame)
        
        # 生成按钮
        self.create_generate_button(main_frame)
    
    def create_problem_type_frame(self, parent):
        """创建题目类型选择框架"""
        type_frame = ttk.LabelFrame(parent, text="题目类型", padding="5")
        type_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(type_frame, text="加法", variable=self.has_addition).grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        ttk.Checkbutton(type_frame, text="减法", variable=self.has_subtraction).grid(row=0, column=1, sticky=tk.W, padx=(0, 10))
        ttk.Checkbutton(type_frame, text="乘法", variable=self.has_multiplication).grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        ttk.Checkbutton(type_frame, text="除法(带余数)", variable=self.has_division).grid(row=0, column=3, sticky=tk.W, padx=(0, 10))
        ttk.Checkbutton(type_frame, text="混合运算", variable=self.has_mixed).grid(row=0, column=4, sticky=tk.W)
    
    def create_num_count_frame(self, parent):
        """创建数字数量选择框架"""
        num_count_frame = ttk.LabelFrame(parent, text="数字个数", padding="5")
        num_count_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(num_count_frame, text="数字个数:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        num_count_combo = ttk.Combobox(num_count_frame, textvariable=self.num_count, values=Constants.NUM_COUNT_OPTIONS, state="readonly", width=15)
        num_count_combo.grid(row=0, column=1, sticky=tk.W)
    
    def _create_range_frame(self, parent, title, row, min_var, max_var):
        """创建范围设置框架的通用方法"""
        frame = ttk.LabelFrame(parent, text=title, padding="5")
        frame.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(frame, text="最小值:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(frame, textvariable=min_var, width=10).grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(frame, text="最大值:").grid(row=0, column=2, sticky=tk.W, padx=(0, 5))
        ttk.Entry(frame, textvariable=max_var, width=10).grid(row=0, column=3)
        
        return frame
    
    def create_number_range_frame(self, parent):
        """创建数字范围设置框架"""
        return self._create_range_frame(parent, "数字范围 (1-999)", 2, self.min_number, self.max_number)
    
    def create_result_range_frame(self, parent):
        """创建结果范围设置框架"""
        return self._create_range_frame(parent, "结果范围 (1-999)", 3, self.min_result, self.max_result)
    
    def _create_labeled_entry(self, parent, text, variable, row, column, width=10, padx=(0, 5)):
        """创建带标签的输入框"""
        ttk.Label(parent, text=text).grid(row=row, column=column, sticky=tk.W, padx=padx)
        ttk.Entry(parent, textvariable=variable, width=width).grid(row=row, column=column+1, padx=(0, 20) if column < 4 else (0, 0))
    
    def create_page_settings_frame(self, parent):
        """创建页面设置框架"""
        page_frame = ttk.LabelFrame(parent, text="页面设置", padding="5")
        page_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self._create_labeled_entry(page_frame, "每页行数:", self.rows_per_page, 0, 0)
        self._create_labeled_entry(page_frame, "每页列数:", self.cols_per_page, 0, 2)
        self._create_labeled_entry(page_frame, "总页数:", self.total_pages, 0, 4)
    
    def create_font_settings_frame(self, parent):
        """创建字体设置框架"""
        font_frame = ttk.LabelFrame(parent, text="字体设置", padding="5")
        font_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self._create_labeled_entry(font_frame, "字体大小:", self.font_size, 0, 0)
    
    def create_bracket_settings_frame(self, parent):
        """创建括号设置框架"""
        bracket_frame = ttk.LabelFrame(parent, text="括号设置", padding="5")
        bracket_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Checkbutton(bracket_frame, text="允许括号出现在等号右边", variable=self.allow_right_bracket).grid(row=0, column=0, sticky=tk.W)
    
    def create_save_path_frame(self, parent):
        """创建保存路径设置框架"""
        path_frame = ttk.LabelFrame(parent, text="保存路径", padding="5")
        path_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Entry(path_frame, textvariable=self.save_path, width=50).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(path_frame, text="浏览", command=self.browse_save_path).grid(row=0, column=1)
    
    def create_generate_button(self, parent):
        """创建生成按钮"""
        ttk.Button(parent, text="生成数学题", command=self.generate_callback).grid(row=8, column=0, columnspan=2, pady=20)
    
    def browse_save_path(self):
        """浏览保存路径"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            self.save_path.set(filename)
    

    
    def get_user_settings(self):
        """获取用户设置"""
        return {
            'has_addition': self.has_addition.get(),
            'has_subtraction': self.has_subtraction.get(),
            'has_multiplication': self.has_multiplication.get(),
            'has_division': self.has_division.get(),
            'has_mixed': self.has_mixed.get(),
            'num_count': self.num_count.get(),
            'min_number': self.min_number.get(),
            'max_number': self.max_number.get(),
            'min_result': self.min_result.get(),
            'max_result': self.max_result.get(),
            'rows_per_page': self.rows_per_page.get(),
            'cols_per_page': self.cols_per_page.get(),
            'total_pages': self.total_pages.get(),
            'font_size': self.font_size.get(),
            'allow_right_bracket': self.allow_right_bracket.get(),
            'save_path': self.save_path.get()
        }
    
    def show_error(self, title, message):
        """显示错误消息"""
        messagebox.showerror(title, message)
    
    def show_success(self, title, message):
        """显示成功消息"""
        messagebox.showinfo(title, message)
    
    def show_warning(self, title, message):
        """显示警告消息"""
        messagebox.showwarning(title, message)
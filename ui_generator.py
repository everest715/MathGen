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
        # === 普通页变量 ===
        self.has_addition = tk.BooleanVar(value=True)
        self.has_subtraction = tk.BooleanVar(value=True)
        self.has_multiplication = tk.BooleanVar(value=False)
        self.has_division = tk.BooleanVar(value=False)
        self.has_division_no_remainder = tk.BooleanVar(value=False)

        self.num_count = tk.StringVar(value=Constants.NUM_COUNT_OPTIONS[0])

        self.min_number = tk.StringVar(value=str(Constants.DEFAULT_MIN_NUMBER))
        self.max_number = tk.StringVar(value=str(Constants.DEFAULT_MAX_NUMBER))
        self.min_result = tk.StringVar(value=str(Constants.DEFAULT_MIN_RESULT))
        self.max_result = tk.StringVar(value=str(Constants.DEFAULT_MAX_RESULT))

        self.rows_per_page = tk.StringVar(value=str(Constants.DEFAULT_ROWS_PER_PAGE))
        self.cols_per_page = tk.StringVar(value=str(Constants.DEFAULT_COLS_PER_PAGE))
        self.total_pages = tk.StringVar(value=str(Constants.DEFAULT_TOTAL_PAGES))
        self.font_size = tk.StringVar(value=str(Constants.DEFAULT_FONT_SIZE))

        self.allow_left_bracket = tk.BooleanVar(value=False)
        self.allow_right_bracket = tk.BooleanVar(value=False)
        self.save_path = tk.StringVar(value=Constants.DEFAULT_SAVE_PATH)

        # === 巧算页变量 ===
        self.clever_type = tk.StringVar(value='凑整加减法')

        self.clever_min_number = tk.StringVar(value=str(Constants.DEFAULT_MIN_NUMBER))
        self.clever_max_number = tk.StringVar(value=str(Constants.DEFAULT_MAX_NUMBER))
        self.clever_min_result = tk.StringVar(value=str(Constants.DEFAULT_MIN_RESULT))
        self.clever_max_result = tk.StringVar(value=str(Constants.DEFAULT_MAX_RESULT))

        self.clever_rows_per_page = tk.StringVar(value=str(Constants.DEFAULT_ROWS_PER_PAGE))
        self.clever_cols_per_page = tk.StringVar(value=str(Constants.DEFAULT_COLS_PER_PAGE))
        self.clever_total_pages = tk.StringVar(value=str(Constants.DEFAULT_TOTAL_PAGES))
        self.clever_font_size = tk.StringVar(value=str(Constants.DEFAULT_FONT_SIZE))

        self.clever_allow_left_bracket = tk.BooleanVar(value=False)
        self.clever_allow_right_bracket = tk.BooleanVar(value=False)
        self.clever_save_path = tk.StringVar(value=Constants.DEFAULT_SAVE_PATH)

    def create_widgets(self):
        """创建界面组件"""
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # 普通页
        normal_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(normal_tab, text="普通")
        normal_tab.columnconfigure(0, weight=1)
        normal_tab.columnconfigure(1, weight=1)
        self._create_normal_tab(normal_tab)

        # 巧算页
        clever_tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(clever_tab, text="巧算")
        clever_tab.columnconfigure(0, weight=1)
        clever_tab.columnconfigure(1, weight=1)
        self._create_clever_tab(clever_tab)

    # ==================== 普通页 ====================

    def _create_normal_tab(self, parent):
        """创建普通页组件"""
        self.create_problem_type_frame(parent)
        self.create_num_count_frame(parent)
        self.create_number_range_frame(parent)
        self.create_result_range_frame(parent)
        self.create_page_settings_frame(parent)
        self.create_font_settings_frame(parent)
        self.create_bracket_settings_frame(parent)
        self.create_save_path_frame(parent)
        self.create_generate_button(parent)

    def create_problem_type_frame(self, parent):
        """创建题目类型选择框架"""
        type_frame = ttk.LabelFrame(parent, text="题目类型", padding="5")
        type_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(type_frame, text="加法", variable=self.has_addition).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Checkbutton(type_frame, text="减法", variable=self.has_subtraction).grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        ttk.Checkbutton(type_frame, text="乘法", variable=self.has_multiplication).grid(row=0, column=2, sticky=tk.W, padx=(0, 20))
        ttk.Checkbutton(type_frame, text="除法", variable=self.has_division_no_remainder).grid(row=0, column=3, sticky=tk.W, padx=(0, 20))
        ttk.Checkbutton(type_frame, text="除法(带余数)", variable=self.has_division).grid(row=0, column=4, sticky=tk.W)

    def create_num_count_frame(self, parent):
        """创建数字数量选择框架"""
        num_count_frame = ttk.LabelFrame(parent, text="数字个数", padding="5")
        num_count_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(num_count_frame, text="数字个数:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Combobox(num_count_frame, textvariable=self.num_count, values=Constants.NUM_COUNT_OPTIONS, state="readonly", width=15).grid(row=0, column=1, sticky=tk.W)

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
        return self._create_range_frame(parent, "数字范围 (2-999)", 2, self.min_number, self.max_number)

    def create_result_range_frame(self, parent):
        """创建结果范围设置框架"""
        return self._create_range_frame(parent, "结果范围 (2-999)", 3, self.min_result, self.max_result)

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

        ttk.Checkbutton(bracket_frame, text="允许等号左边出现括号", variable=self.allow_left_bracket).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Checkbutton(bracket_frame, text="允许等号右边出现括号", variable=self.allow_right_bracket).grid(row=0, column=1, sticky=tk.W)

    def create_save_path_frame(self, parent):
        """创建保存路径设置框架"""
        path_frame = ttk.LabelFrame(parent, text="保存路径", padding="5")
        path_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Entry(path_frame, textvariable=self.save_path, width=50).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(path_frame, text="浏览", command=lambda: self._browse_save_path(self.save_path)).grid(row=0, column=1)

    def create_generate_button(self, parent):
        """创建生成按钮"""
        ttk.Button(parent, text="生成数学题", command=self.generate_callback).grid(row=8, column=0, columnspan=2, pady=20)

    # ==================== 巧算页 ====================

    def _create_clever_tab(self, parent):
        """创建巧算页组件"""
        # 题型选择
        type_frame = ttk.LabelFrame(parent, text="巧算类型", padding="5")
        type_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        clever_types = ['凑整加减法', '乘法交换律']
        for i, ct in enumerate(clever_types):
            ttk.Radiobutton(type_frame, text=ct, variable=self.clever_type, value=ct).grid(row=0, column=i, sticky=tk.W, padx=(0, 20))

        # 数字范围
        self._create_range_frame(parent, "数字范围 (2-999)", 1, self.clever_min_number, self.clever_max_number)

        # 结果范围
        self._create_range_frame(parent, "结果范围 (2-999)", 2, self.clever_min_result, self.clever_max_result)

        # 页面设置
        page_frame = ttk.LabelFrame(parent, text="页面设置", padding="5")
        page_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self._create_labeled_entry(page_frame, "每页行数:", self.clever_rows_per_page, 0, 0)
        self._create_labeled_entry(page_frame, "每页列数:", self.clever_cols_per_page, 0, 2)
        self._create_labeled_entry(page_frame, "总页数:", self.clever_total_pages, 0, 4)

        # 字体设置
        font_frame = ttk.LabelFrame(parent, text="字体设置", padding="5")
        font_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        self._create_labeled_entry(font_frame, "字体大小:", self.clever_font_size, 0, 0)

        # 括号设置
        bracket_frame = ttk.LabelFrame(parent, text="括号设置", padding="5")
        bracket_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Checkbutton(bracket_frame, text="允许等号左边出现括号", variable=self.clever_allow_left_bracket).grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        ttk.Checkbutton(bracket_frame, text="允许等号右边出现括号", variable=self.clever_allow_right_bracket).grid(row=0, column=1, sticky=tk.W)

        # 保存路径
        path_frame = ttk.LabelFrame(parent, text="保存路径", padding="5")
        path_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Entry(path_frame, textvariable=self.clever_save_path, width=50).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(path_frame, text="浏览", command=lambda: self._browse_save_path(self.clever_save_path)).grid(row=0, column=1)

        # 生成按钮
        ttk.Button(parent, text="生成数学题", command=self.generate_callback).grid(row=7, column=0, columnspan=2, pady=20)

    # ==================== 公共方法 ====================

    def _browse_save_path(self, target_var):
        """浏览保存路径"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if filename:
            target_var.set(filename)

    def get_active_tab(self) -> str:
        """获取当前激活的页签"""
        current = self.notebook.select()
        return self.notebook.tab(current, "text")

    def get_user_settings(self):
        """获取普通页用户设置"""
        return {
            'has_addition': self.has_addition.get(),
            'has_subtraction': self.has_subtraction.get(),
            'has_multiplication': self.has_multiplication.get(),
            'has_division': self.has_division.get(),
            'has_division_no_remainder': self.has_division_no_remainder.get(),
            'num_count': self.num_count.get(),
            'min_number': self.min_number.get(),
            'max_number': self.max_number.get(),
            'min_result': self.min_result.get(),
            'max_result': self.max_result.get(),
            'rows_per_page': self.rows_per_page.get(),
            'cols_per_page': self.cols_per_page.get(),
            'total_pages': self.total_pages.get(),
            'font_size': self.font_size.get(),
            'allow_left_bracket': self.allow_left_bracket.get(),
            'allow_right_bracket': self.allow_right_bracket.get(),
            'save_path': self.save_path.get()
        }

    def get_clever_settings(self):
        """获取巧算页用户设置"""
        return {
            'clever_type': self.clever_type.get(),
            'min_number': self.clever_min_number.get(),
            'max_number': self.clever_max_number.get(),
            'min_result': self.clever_min_result.get(),
            'max_result': self.clever_max_result.get(),
            'rows_per_page': self.clever_rows_per_page.get(),
            'cols_per_page': self.clever_cols_per_page.get(),
            'total_pages': self.clever_total_pages.get(),
            'font_size': self.clever_font_size.get(),
            'allow_left_bracket': self.clever_allow_left_bracket.get(),
            'allow_right_bracket': self.clever_allow_right_bracket.get(),
            'save_path': self.clever_save_path.get()
        }

    def show_error(self, title, message):
        """显示错误消息"""
        messagebox.showerror(title, message)

    def show_success(self, title, message):
        """显示成功消息"""
        messagebox.showinfo(title, message)

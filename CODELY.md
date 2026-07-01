# CODELY.md — 数学题生成器项目指令

## 项目概览

数学题生成器（MathGen）是一个基于 Python + Tkinter 的桌面应用，用于批量生成小学数学练习题并导出为 PDF。

**核心功能：**
- 支持加法、减法、乘法、除法（带余数）、混合运算五种题型
- 支持 2 数和 3 数运算表达式
- 可自定义数字范围（1-999）和结果范围（1-999）
- 支持括号位置控制：等号左边括号、等号右边括号可独立开关
- 支持减少整十数字（10、20、30 等）在加减法中的出现频率
- 可配置页面布局：页数、列数（1-5）、每列题数、字号（12-24pt）
- 自动生成多列排版的 PDF 文件，支持中文字体

**技术栈：**
- **GUI 框架：** Tkinter（`tkinter` + `ttk`）
- **PDF 生成：** reportlab
- **Python 版本：** 3.12+
- **运行平台：** Windows（主），兼容 macOS / Linux

## 架构与模块

```
MathGen/
├── main.py              # 入口文件，整合 UI / 算式引擎 / PDF 生成
├── ui_generator.py      # Tkinter GUI 界面生成器
├── math_engine.py       # 数学表达式生成引擎（核心逻辑）
├── pdf_generator.py     # PDF 文档生成器（reportlab）
├── constants.py         # 全局常量定义（UI 配置、范围限制、PDF 参数等）
├── requirements.txt     # Python 依赖
├── legacy/              # 旧版本代码（math_gen.py 命令行版、math_gui.py PyQt 版）
├── results/             # 生成的 PDF 输出目录（已 gitignore）
└── CHANGELOG.md         # 更新日志
```

### 模块职责

| 模块 | 职责 |
|------|------|
| `main.py` | `MathProblemGenerator` 主类，编排 UI → 算式生成 → PDF 导出流程 |
| `ui_generator.py` | `UIGenerator` 类，构建全部 GUI 控件并管理用户设置 |
| `math_engine.py` | `MathEngine` 类，负责所有算式生成逻辑、范围验证、括号位置控制 |
| `pdf_generator.py` | `PDFGenerator` 类，使用 reportlab 生成多列排版 PDF，自动注册中文字体 |
| `constants.py` | `Constants` 类，集中管理窗口尺寸、默认值、范围限制等常量 |

### 关键设计

- **表达式生成流程：** 先随机生成结果值，再根据结果反推操作数，确保结果在用户设定范围内均匀分布
- **整十数字控制：** `_generate_random_with_round_tens_control` 方法以 50% 概率重新生成整十数字，应用于操作数和结果
- **括号位置控制：** `allow_left_bracket` 和 `allow_right_bracket` 独立开关，2 数运算支持 4 种位置，3 数运算支持 5 种位置
- **PDF 多列布局：** 自定义 `MultiColumnDocTemplate`，基于 reportlab `BaseDocTemplate` + `Frame` 实现多列排版
- **中文字体注册：** 按平台自动查找 SimSun / SimHei / Microsoft YaHei / PingFang / DejaVu 字体

## 构建和运行

### 安装依赖

```bash
pip install -r requirements.txt
```

依赖列表：
- `PyQt6>=6.5.0`（仅 legacy 版本使用）
- `reportlab>=3.6.0`

### 运行程序

```bash
python main.py
```

启动后将弹出 Tkinter GUI 窗口，用户可：
1. 勾选题型（加法 / 减法 / 乘法 / 除法 / 混合运算）
2. 选择数字个数（2 个或 3 个）
3. 设置数字范围和结果范围
4. 配置页面布局（行数、列数、页数、字号）
5. 设置括号位置（等号左边 / 等号右边）
6. 可选减少整十数字出现频率
7. 选择保存路径
8. 点击"生成数学题"按钮生成 PDF

### 运行旧版本（可选）

```bash
python legacy/math_gen.py    # 命令行版
python legacy/math_gui.py    # PyQt6 GUI 版
```

### 测试

> TODO: 项目当前没有自动化测试。如需验证功能，手动运行 `python main.py` 并通过 GUI 生成 PDF 检查。

### 构建检查

```bash
# 语法检查
python -m py_compile main.py math_engine.py ui_generator.py pdf_generator.py constants.py
```

## 开发约定

### 代码风格

- 使用中文 docstring 描述函数用途，保持简洁（通常一行）
- 类型提示使用 Python 3.10+ 语法（`tuple[int, int]` 而非 `Tuple[int, int]`）
- 常量集中管理在 `constants.py` 的 `Constants` 类中，使用 `Final` 类型标注
- UI 布局使用 `ttk` 控件 + `grid` 布局管理器
- 私有方法以单下划线前缀命名（如 `_generate_addition_expression`）

### 提交规范

从最近提交历史推断的 commit message 风格：

```
<type>: <简短描述>

<可选的详细说明，列出主要修改点>
```

常用 type：`feat`（新功能）、`fix`（修复）、`docs`（文档）

### Git 工作流

- 当前开发分支：`codely`
- 远程仓库已配置，提交后使用 `git push` 推送

## Codely Added Memories

- 当前项目默认使用中文与用户交流；除非用户明确要求其他语言，否则请用中文回答。

import random
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Preformatted, Frame, PageTemplate
from reportlab.lib.units import inch

def generate_expression():
    operator = random.choice(['+', '-'])
    a = random.randint(1, 99)
    b = random.randint(1, 99)
    a, b = max(a, b), min(a, b)

    # 随机选择要加括号的位置（0-左边 1-右边）
    bracket_pos = random.choice([0, 1])

    if bracket_pos == 0:
        if operator == "+":
            return f'(     ) + {b} = {a}'  # 使用中文全角空格
        else:
            return f'(     ) - {b} = {a - b}'
    else:
        if operator == "+":
            return f'{b} + (     ) = {a}'
        else:
            return f'{a} - (     ) = {b}'

def create_pdf(filename, problems, cols=3):
    doc = SimpleDocTemplate(filename, pagesize=letter,
                        rightMargin=36, leftMargin=36,
                        topMargin=36, bottomMargin=18)

    frame_width = (doc.width + doc.leftMargin) / cols
    frames = [
        Frame(doc.leftMargin + i*frame_width, doc.bottomMargin,
              frame_width - 6, doc.height, id=f'col{i}')
        for i in range(cols)
    ]

    # Apply the same column layout to all pages
    doc.addPageTemplates([PageTemplate(frames=frames, id='multi_col')])

    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontSize = 14
    style.leading = 28
    # style.spaceBefore = 6  # 增加段落前间距

    content = []
    for i, prob in enumerate(problems):
        p = Preformatted(f"{prob}", style)
        content.append(p)

    doc.build(content)

if __name__ == '__main__':
    pages = 10
    cols = 4
    perCol = 25
    count = pages * perCol * cols
    problems = [generate_expression() for _ in range(count)]

    # 保存txt
    # with open('math_problems.txt', 'w', encoding='utf-8') as f:
    #     f.write('\n'.join([f'{p}' for i, p in enumerate(problems)]))

    # 生成PDF
    create_pdf('math_problems.pdf', problems, cols)
    print(f'\n已生成{count}道题目到 math_problems.pdf')
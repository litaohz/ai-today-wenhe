import re

# 读取文件
file_path = r'c:\Users\98554\Downloads\ai-today-wenhe\archives-260120\ai_posts_summary_2026-01-20.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 提取概览表格的4行（第8-11行）
lines = content.split('\n')
table_rows = []
for i in range(7, 11):  # 第8-11行 (0-indexed 为 7-10)
    table_rows.append(lines[i])

# 反转表格行
table_rows_reversed = list(reversed(table_rows))

# 替换概览表格
for i in range(4):
    lines[7 + i] = table_rows_reversed[i]

# 现在需要重新排序详细内容部分
# 找到并提取4个详细内容块

# 分割详细内容
detail_sections = []
current_section = []
in_detail = False
detail_start_line = 0

for i, line in enumerate(lines):
    if line.startswith('#### 1. Google Antigravity'):
        detail_start_line = i
        in_detail = True
    
    if in_detail:
        if line.startswith('#### ') and current_section:
            detail_sections.append('\n'.join(current_section))
            current_section = [line]
        else:
            current_section.append(line)

# 添加最后一个section
if current_section:
    detail_sections.append('\n'.join(current_section))

# 反转详细内容并更新编号
reversed_details = list(reversed(detail_sections))

for i, section in enumerate(reversed_details):
    # 更新编号 (从1-4)
    reversed_details[i] = re.sub(r'^#### \d+\.', f'#### {i+1}.', section)

# 重新组合内容
result_lines = lines[:detail_start_line] + ['\n'.join(reversed_details)]

# 写回文件
with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(result_lines))

print("✓ 已成功调整顺序：")
print("  - 概览表格：4→1, 3→2, 2→3, 1→4")
print(" print("  - 详细内容：4个项目顺序已反转并重新编号")

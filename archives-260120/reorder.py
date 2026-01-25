import re

# 读取文件
file_path = r'c:\Users\98554\Downloads\ai-today-wenhe\archives-260120\ai_posts_summary_2026-01-20.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 分行
lines = content.splitlines()

# Step 1: 反转概览表格 (行8-11, 0-indexed: 7-10)
table_rows = lines[7:11]
table_rows_reversed = list(reversed(table_rows))
lines[7:11] = table_rows_reversed

# Step 2: 找出详细内容的4个部分
sections = []
current = []
start_idx = None

for i, line in enumerate(lines):
    if line.startswith('#### 1. Google Antigravity'):
        start_idx = i
    
    if start_idx is not None:
        if line.startswith('#### ') and current:
            sections.append(current[:])
            current = [line]
        elif start_idx is not None:
            current.append(line)

# 添加最后一个部分
if current:
    sections.append(current)

# 反转4个部分
sections_reversed = list(reversed(sections))

# 更新编号
for idx, section in enumerate(sections_reversed):
    # 找到标题行并更新编号
    section[0] = re.sub(r'^#### \d+\.', f'#### {idx + 1}.', section[0])


# 重新组装文件
new_content = '\n'.join(lines[:start_idx])
new_content += '\n'

for section in sections_reversed:
    new_content += '\n'.join(section)
    if section != sections_reversed[-1]:
        new_content += '\n\n'

# 写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✓ 已成功调整顺序")
print("  - 概览表格：4→1, 3→2, 2→3, 1→4")
print("  - 详细内容：4个项目顺序已反转并重新编号")

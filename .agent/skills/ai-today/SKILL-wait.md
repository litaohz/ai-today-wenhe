---
name: ai-today
description: 自动化生成 X (Twitter) AI 动态日报，包括信息收集、总结、生成HTML报告及截图。
---

# AI Today Daily Workflow

此技能执行完整的 AI 日报生成流程，从 Twitter 列表获取信息，生成中文摘要，如果不满意可以人工修改，最后生成美观的 HTML 并自动截图。

## 默认配置
- **Assets Dir**: `c:\Users\taoli1\ai-today\260113 X大佬-v2` (包含 Logo 和二维码的文件夹)
- **Twitter List**: `https://x.com/i/lists/2010748418889752969`

## 步骤 (Steps)

### 1. 收集信息与总结 (Gather & Summarize)
首先，确定目标日期和时间范围。
- 默认范围: 过去 24 小时 (05:30 UTC 到 05:30 UTC)。
- 目标文件: `summaries/ai_posts_summary_{DATE}.md` (如果 summaries 文件夹不存在请创建)

执行 `gather-twitter-info` 技能：
- 确保涵盖所有 AI 相关内容（宁可错杀不可放过）。
- 生成中文 Markdown 摘要。

### 2. 等待翻译确认 (Wait for Translation/Review)
在生成 HTML 之前，必须暂停并通知用户。
**Action**: 调用 `notify_user`。
- **Message**: "摘要已生成 (ai_posts_summary_{DATE}.md)。请检查内容和中文翻译。如果需要修改，请直接编辑文件。确认无误后请回复继续。"
- **PathsToReview**: `[生成的 Markdown 文件路径]`

### 3. 生成 HTML (Generate HTML)
用户确认后，使用 Python 脚本将 Markdown 转换为 HTML。

**Command**:
```bash
python .agent/skills/ai-today/scripts/md_to_html.py "{Markdown文件绝对路径}" "{输出HTML文件绝对路径}" "c:\Users\taoli1\ai-today\260113 X大佬-v2"
```

### 4. 自动截图 (Auto Screenshot)
使用浏览器子代理 (Browser Sub-agent) 打开生成的 HTML 并截图。

**Browser Task Instruction**:
"打开本地 HTML 文件 `{HTML文件绝对路径}`。请按照以下顺序截图：
1.  **总览图**: 找到 ID 为 `screenshot-1` 的元素，截取该元素。保存为 `summary_01_overview.png`。
2.  **分块截图**: 查找所有 ID 以 `section-` 开头的元素 (如 `section-1`, `section-2` 等)。依次对每一个元素进行元素截图 (Element Screenshot)。保存为 `summary_02_section_1.png`, `summary_03_section_2.png` 等。
"

## 交付
将所有截图和 HTML 文件告知用户。

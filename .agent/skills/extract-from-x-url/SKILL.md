---
name: extract-from-x-url
description: 根据用户提供的X/Twitter链接列表，打开浏览器查看推文原文，提取内容并生成结构化的AI动态摘要Markdown文件。
---

# 从X链接提取推文内容并生成摘要

此技能旨在根据用户提供的X/Twitter链接列表，通过浏览器查看推文原文，提取内容并生成结构化的"硅谷AI圈动态"Markdown摘要文件。

## 背景
当用户已经收集了一批X/Twitter推文链接（通常来自AI领域重要人物），需要将这些链接转化为一份结构化的中文摘要报告时，使用此技能。

## 输入

### 输入类型1: 直接链接列表
- **X链接列表**: 用户提供的一组X/Twitter推文URL
- **可选的初步摘要**: 用户可能提供每条链接的简要描述

### 输入类型2: 对话内容 (含总体观察) -> 转化为 Raw 文件
用户在对话框中直接发送包含"总体观察"和"链接列表"的文本内容。

**Agent 必须执行的前置动作**:
1.  解析用户内容中的日期（或使用当前日期）
2.  新建文件夹 `archive/archives-YYMMDD`
3.  新建文件 `raw-YYMMDD.md`
4.  将用户在对话中提供的所有内容，**原封不动**地写入该文件

**内容示例**:
```markdown
总体观察：过去24小时AI动态以产品更新（Gemini/Anthropic）、研究发布和合作为主，无重大突破性新闻。

@mntruell
（Cursor CEO）Cursor代理最佳实践分享
...
```

**处理规则**: 当提供 raw 文件时，"总体观察"内容应该被改写并用于生成最终文档中"📊 总览"部分的第一句话

## 指令 (Instructions)

### 1. 浏览器查看推文 (Browser Navigation)
对于每个提供的X链接，使用浏览器子代理 (Browser Sub-agent) 进行访问：

```
使用 browser_subagent 工具，为每个链接创建独立任务：
- 导航至推文URL
- 等待页面完全加载
- 提取以下信息：
  1. 推文完整文本内容
  2. 作者名称和handle (@username)
  3. 发布时间戳
  4. 如果是回复/引用，获取上下文
  5. 如果有媒体（图片/视频），简要描述
```

- 确保页面完全加载。
- **信任列表**: 若用户提供了链接列表，**严格逐个访问**。严禁企图通过滚动去“搜寻”同线程的其他推文，以免陷入评论区死循环。
- **适度滚动**: 仅在需要展示当前推文的完整内容时才下滑，不要遍历历史列表。

**注意**: 可以并行访问多个链接以提高效率，每个链接使用不同的 `RecordingName`。

### 1.1 智能截图 (Smart Screenshot Capture)

在访问链接时，**仅对 X (Twitter) 推文进行截图**。对于博客、官网、论文等其他类型链接，**只提取文本，不要截图**。
截图必须高质量、干净，不应包含任何不相关的浏览器UI、侧边栏或焦点框。

#### 实施步骤 (Implementation Steps)

1.  **准备环境 (Cleanup & Layout)**:
    - **隐藏基础干扰元素**: 使用 JavaScript 隐藏以下元素：
        - 左侧导航栏: `header[role="banner"]`
        - 右侧搜索/推荐栏: `[data-testid="sidebarColumn"]`
        - 底部登录/注册提示: `[data-testid="bottom_bar"]`, `#layers`
        - 内联回复框: `[data-testid="inline_reply_offering_container"]`
    
    - **清除所有浮动元素**: 遍历所有 `fixed` 和 `sticky` 定位的元素并隐藏：
        ```javascript
        const allElements = document.querySelectorAll('*');
        allElements.forEach(el => {
            const style = window.getComputedStyle(el);
            if (style.position === 'fixed' || style.position === 'sticky') {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
            }
        });
        ```
        **注意**: 这会移除翻译小部件、浮动按钮等所有干扰元素。
    
    - **调整布局**: 
        - 主内容列居中: 设置 `[data-testid="primaryColumn"]` 的样式：
            ```javascript
            primaryColumn.style.float = 'none';
            primaryColumn.style.margin = '0 auto';
            primaryColumn.style.maxWidth = '600px';
            primaryColumn.style.width = '100%';
            ```
        - 调整父容器以支持居中效果
    
    - **移除焦点**: `if (document.activeElement) document.activeElement.blur();`

2.  **验证翻译**:
    - **检查并点击翻译按钮**: 在执行 UI 清理前，先确保翻译已激活：
        ```javascript
        const translateButton = Array.from(article.querySelectorAll('[role="button"], span'))
            .find(el => el.textContent.toLowerCase().includes('translate post'));
        if (translateButton) translateButton.click();
        ```
    - **等待翻译加载**: 点击后等待 1-2 秒让翻译内容完全显示

3.  **上下文判断与处理 (Context Preservation)**:
    - **自动检测回复关系**: 检查页面中是否有多个 `article` 元素：
        ```javascript
        const articles = document.querySelectorAll('article');
        const isReply = articles.length >= 2;
        ```
    - **包含原推文的条件**:
        - 目标推文是回复（URL 包含上下文或页面显示多条推文）
        - 目标推文本身内容较短或引用了上文（如 "This is huge", "Nice work"）
    - **确保两条推文都可见**:
        - 调整窗口高度: `browser_resize_window` 增加高度至 2000px
        - 滚动到对话顶部: `articles[0].scrollIntoView({ behavior: 'auto', block: 'start' });`
        - 移除原推文前的所有内容以避免截图时被裁切

4.  **精确控制滚动位置**:
    - **重置所有边距和填充**:
        ```javascript
        document.documentElement.style.marginTop = '0';
        document.body.style.marginTop = '0';
        const primaryColumn = document.querySelector('[data-testid="primaryColumn"]');
        if (primaryColumn) {
            primaryColumn.style.marginTop = '0';
            primaryColumn.style.paddingTop = '0';
        }
        ```
    - **滚动到绝对顶部**: 
        - 先执行 `window.scrollTo(0, 0);`
        - 如果顶部有固定头部，再向上偏移: `window.scrollBy(0, -100);`
    - **验证可见性**: 确保第一条推文的头像和用户名完全可见

5.  **执行截图**:
    - **优先尝试元素级截图**: 
        - 找到包含所有相关推文的共同父元素
        - 使用 `capture_browser_screenshot` 的 `CaptureByElementIndex` 功能
    - **Fallback 到视口截图**: 
        - 确保内容居中、完整
        - 无多余白边或裁切
    - **最终检查**: 截图应包含：
        - ✅ 完整的用户头像和名称
        - ✅ 推文正文（英文原文）
        - ✅ 中文翻译
        - ✅ 如有媒体内容（图片、链接卡片），应完整显示
        - ✅ 互动数据（回复数、转发数、点赞数）
        - ✅ 发布时间
        - ❌ 无浏览器 UI、导航栏、侧边栏
        - ❌ 无焦点框、浮动按钮

6.  **保存路径**: 
    - 目标目录: `archive/archives-YYMMDD`（根据当前日期自动生成）
    - 文件命名: `1.png`, `2.png`, `3.png`... (对应链接在列表中的顺序)
    - 确保目录存在再保存文件

#### 常见问题与解决方案 (Troubleshooting)

- **问题**: 截图顶部被裁切，看不到用户头像
  - **解决**: 增加向上滚动偏移量 `window.scrollBy(0, -200);` 或 `window.scrollBy(0, -300);`

- **问题**: 浮动翻译按钮出现在截图右侧
  - **解决**: 在截图前确保已执行完整的 `fixed`/`sticky` 元素清理

- **问题**: 无法同时看到原推文和回复推文
  - **解决**: 增加浏览器窗口高度至 2000px 或更高，并隐藏中间无关的回复

- **问题**: 翻译未显示
  - **解决**: 在 UI 清理前先点击翻译按钮，并等待 1-2 秒

- **问题**: 元素级截图失败 (element index not found)
  - **解决**: 切换到视口截图，确保内容已正确滚动到可见区域

### 2. 内容分析与合并 (Content Analysis & Merging)

提取完所有推文内容后，进行智能分析。

> **⚠️ 重要原则**: 在总结内容前，请务必阅读 [内容提取原则](resources/content-extraction-principles.md) 以避免遗漏推文核心新闻点。

**主题合并规则**:
- 如果多条推文来自**同一作者**且讨论**同一主题**，应合并为一条
- 例如：Elon Musk 的 AI 芯片路线图推文 + Dojo3 确认推文 → 合并为"AI芯片战略与Dojo3重启确认"
- 合并时保留所有关键信息点和所有相关链接

**判断是否合并的标准**:
1. 发布者相同
2. 主题高度相关（如同一技术/产品的不同方面）
3. 时间接近（通常在24小时内）

### 3. 生成Markdown报告 (Generate Markdown Report)

#### 文件命名
`ai_posts_summary_YYYY-MM-DD.md`

#### 报告结构

```markdown
# YYYY/MM/DD 硅谷AI圈动态

**时间范围**: YYYY-MM-DD HH:MM UTC - YYYY-MM-DD HH:MM UTC

---

## 📊 总览

[总结性开场语句 - 如果用户提供了raw文件中的"总体观察"，则基于此改写；否则根据提取的内容自行总结]

| 主题 | 关键事件 |
| :--- | :--- |
| **[主题1]** | [一句话摘要] |
| **[主题2]** | [一句话摘要] |
...

---

## 🔥 重点帖子详情

#### 1. [公司/实体] - [标题/主题]
**发布者**: [姓名] (@handle)，[职位]
**时间**: YYYY-MM-DD HH:MM UTC
**核心内容**:
- [要点1]
- [要点2]
- [要点3]

**核心内容的内容要求**:
- 1. 根据推文的内容，理解原文并总结，不要只100%照搬原文；
- 2. 如果该推文的内容，只能总结为一句话，则不要强行分点，可以灵活一些；
- 3. 每一条要点前，用关键词提炼该要点，并加粗
- 4. 总结的文案，不要泛泛而谈，不要用很空洞的词。最好能具体到一些数据，或者一些细节。
- 5. **每一条要点文案最后，不要加句号“。”或分号“；”**

**链接**: [URL] 或多个链接列表
![screenshot](N.png)  (注意：对应本条内容的截图文件, N为序号)

#### 2. [公司/实体] - [下一个主题]
...
```

### 4. 格式规范 (Formatting Rules)


**必须遵循**:
- 所有文本使用**中文**（技术术语可保留英文）
- **中英文/数字间距**：英文单词和数字的前后需添加空格；若位于句首或紧跟标点符号后，则前面不加空格（如：`定价：6 元`）
- 概览表格的关键事件必须简洁（30字以内），**且结尾不要加句号或分号**
- **一步到位**: 对于 X 推文，生成的 Markdown 文件必须包含截图引用 (`![xxx](N.png)`)；非 X 链接无需截图。
- 链接放在每条内容的最后，紧接着是截图
- 如果一条内容有多个相关链接，使用列表格式

**核心内容格式**:
- 使用 bullet points 组织
- 可使用**加粗**标注子标题
- 保留关键英文原文的引用（用引号标注）

### 4.1 时间处理规则 (Time Handling)

**原则**: 相信源头 (Trust the Source)
- **X/Twitter 网页/截图**: 在浏览器环境或截图中看到的推文时间，默认已经是**北京时间**。提取时，**直接抄录**时间字符串（如 `2026-02-04 20:25`），并明确标记为 `北京时间`，**不要**标记为 `UTC`，也**不要**进行任何时区换算。
- **其他来源**: 仅当来源明确写有 `UTC` 或 `PST` 等时区后缀时，才保留该后缀。
- **总结**: 既然浏览器环境已设定为中文/北京时间，所见即所得。所见即北京时间。

### 5. 创建输出文件夹与文件

```
1. 创建目标文件夹 (如 archive/archives-260119)
2. 在文件夹内创建 ai_posts_summary_YYYY-MM-DD.md
3、文件夹名称和md文件名称中的日期，选择对话当天的日期
```

## 输出格式

- **文件夹**: `archive/archives-YYMMDD/`
- **文件**: 
  - `ai_posts_summary_YYYY-MM-DD.md`
  - 截图文件: `1.png`, `2.png`, ...

- **语言**: 中文

## 示例
请参考 `examples` 目录下的 `ai_posts_summary_2026-01-16.md` 文件作为风格参考。

## 常见场景

### 场景1: 用户提供链接和简要描述
```
@elonmusk (2026-01-18 05:18 GMT)
Tesla AI 芯片路线图：AI4-AI7/Dojo3
→ 链接: https://x.com/elonmusk/status/xxx
```
直接使用浏览器查看，获取完整内容后生成报告。

### 场景2: 用户只提供链接列表
逐个访问链接，提取内容，判断主题关联性，生成报告。

### 场景3: 需要合并相似主题
当两条来自同一作者、讨论同一话题的推文出现时，主动合并并告知用户。

### 场景4: 用户提供完整摘要文本（含总体观察）
用户在对话中发送了一大段文本，包含总体观察和多个推文链接信息。

**处理流程**:
1.  **创建原始归档**: 
    - 创建 `archive/archives-YYMMDD` 文件夹
    - 创建 `raw-YYMMDD.md`
    - 将用户的**完整输入内容**写入文件
2.  **执行提取**: 解析内容中的链接，并行访问、截图、提取
3.  **文件管理**: 将截图从临时目录复制到 `archive/archives-YYMMDD`
4.  **生成报告**: 
    - 引用 `raw-YYMMDD.md` 中的"总体观察"改写作为"📊 总览"开头
    - 生成 `ai_posts_summary_YYYY-MM-DD.md`

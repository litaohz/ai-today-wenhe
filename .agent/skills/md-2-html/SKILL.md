---
name: md-2-html
description: Convert AI Today Markdown summaries into a styled HTML page with the "Light Purple/White" design, refined typography, specific footer layout, and responsive structure.
---

# AI Today 日报 HTML 生成技能 (Light Theme)

## 概述

将 AI 日报的 Markdown 内容转换为**日系/清新/明亮**的紫色主题 HTML 页面。页面采用白色半透明叠加态设计，视觉轻盈，适合阅读和移动端分享。

## 内容生成规则

### 发布者身份格式

在生成HTML时，需要处理Markdown中的"发布者"信息，遵循以下规则：

1. **删除X账号@提及**：如果Markdown中写明了X账号（如@mntruell、@antigravity），在HTML中应删除@符号和账号名
2. **个人发布者需补充身份**：
   - 如果发布者是个人（如Elon Musk、Sam Altman、Michael Truell），需要补充其身份说明
   - 身份应选择该人担任的AI相关公司中最大、最高的那个职位
   - 身份使用括号格式，如：`Elon Musk (X CEO)`、`Michael Truell (Cursor AI CEO)`
3. **公司/产品发布者无需额外身份**：如果发布者是公司或产品（如OpenAI、GeminiApp、AnthropicAI），则不需要补充额外说明

**示例**：
- Markdown: `发布者: Elon Musk (@elonmusk)` → HTML: `Elon Musk (X CEO)`
- Markdown: `发布者: Michael Truell (@mntruell)` → HTML: `Michael Truell (Cursor AI CEO)`
- Markdown: `发布者: AnthropicAI (@AnthropicAI)` → HTML: `AnthropicAI`
- Markdown: `发布者: Google Antigravity (@antigravity)` → HTML: `Google Antigravity`

### 标点符号规范

HTML生成时，所有中文标点符号**必须使用全角**，括号除外：

- **全角标点**（必须转换）：
  - 逗号：`,` → `，`
  - 句号（如适用）：`.` → `。`
  - 冒号：`:` → `：`
  - 分号：`;` → `；`
  - 引号：`"` → `"`（使用全角CJK引号）
  - 问号（如适用）：`?` → `？`
  - 感叹号（如适用）：`!` → `！`

- **保持半角**（不转换）：
  - 括号：`()` 保持半角
  - 英文内容中的标点符号保持半角
  - 技术术语、代码相关内容中的标点符号保持原样
  - **列表项与关键事件**：
    - "总览"表中的关键事件描述，结尾**不要**加句号或分号
    - "核心内容"列表项，结尾**不要**加句号或分号

**示例**：
- `发布者: Elon Musk` → `发布者：Elon Musk`
- `时间: 2026-01-20` → `时间：2026-01-20`
- `"The Assistant Axis"研究,探索` → `"The Assistant Axis"研究，探索`
- `(word-level inline diffs),进一步` → `(word-level inline diffs)，进一步`（括号保持半角，逗号改全角）

### 中英文/数字间距

英文单词和数字的前后，需各添加 1 个空格。**例外**：若英文/数字位于句首或紧跟标点符号后，则前面不加空格。
- `发布2.5倍速更快版本` → `发布 2.5 倍速更快版本`
- `价格6倍` → `价格 6 倍`
- `支持Claude Code` → `支持 Claude Code`
- `定价：6元` → `定价：6 元`（冒号后的 6 前面不加空格）

### 关于链接
删除所有链接

### 总览文案 (Overview Text)

HTML 页面中 "总览" 模块的 `overview-text` 内容，**必须** 动态提取自 Markdown 文件。

- **来源**: Markdown 文件 `## 📊 总览` 标题下的第一段文本（通常为一句话总结）。
- **操作**: 提取该段文本，替换 HTML 模板中 `<p class="overview-text">...</p>` 的内容。

### 时间显示格式

HTML生成时，应严格根据 Markdown 中标注的时区进行处理：

1. **UTC 时间**: 如果时间字符串明确标记为 `UTC` (如 `2026-02-04 20:25 UTC`)，**必须**加上8小时转换为北京时间。
   - 例: `2026-02-02 20:25 UTC` -> `2026-02-03 04:25 北京时间`
2. **北京时间**: 如果时间字符串标记为 `北京时间` (或无时区标记但暗示为本地时间)，则**直接原样保留**数值，不进行转换。
   - 例: `2026-02-02 20:25 北京时间` -> `2026-02-02 20:25 北京时间`

**关键原则**: 依据文本中的标签判断。如果用户明确写了 UTC，说明那就是 UTC 时间，需要转换；如果用户写了北京时间（或由 X 截图提取而来），那就是北京时间，直接抄录。



## 设计规范

### 1. 配色方案 (Color Palette)

- **背景**: 浅紫色线性渐变 `linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 50%, #ddd6fe 100%)`
- **容器背景**: 高透白色毛玻璃 `rgba(255, 255, 255, 0.85)` + `backdrop-filter: blur(10px)`
- **主要文字**: 深灰 `#1f2937`
- **标题色**: 渐变紫 或 深紫 `#5b21b6` / `#4c1d95`
- **强调色**: 亮紫 `#8b5cf6` (边框、图标、修饰)
- **链接/标签背景**: 极浅紫 `#f3e8ff` 至 `#ede9fe`

### 2. 版式结构 (Layout)

- **容器 (Container)**:
    - `max-width: 800px` 居中显示
    - 整体为一个大卡片容器，内部通过分割线区分区块
    - `font-family: 'Noto Sans SC', sans-serif`

- **区块 (Sections)**:
    - 统一内边距: `padding: 40px 50px`
    - 分割线: `border-bottom: 1px solid rgba(167, 139, 250, 0.2)`
    - 概览、详情文章都作为独立的 `<section>` 堆叠

### 3. 组件样式

#### 头部 (Header)
```css
.header {
    text-align: center;
    padding: 50px 50px 40px;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.95) 0%, rgba(249, 245, 255, 0.9) 100%);
}
.main-title-inline {
    font-size: 2.5rem;
    font-weight: 700;
    /* 紫色渐变文字 */
    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
```

#### 表格 (Event Table)
- **表头**: 紫色渐变背景 `linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%)`，白字
- **单元格**: 白色背景，偶数行浅紫 `rgba(245, 243, 255, 0.5)`
- **圆角**: 表格整体 `border-radius: 12px`，overflow: hidden

#### 详情卡片 (Details)
- **序号球**: 32px 圆形，紫色渐变背景，白字
- **元数据框**: 浅色背景块 `linear-gradient(135deg, #faf5ff 0%, #f3e8ff 100%)`，左侧紫色竖线装饰
- **列表**: 实心圆点 • (紫色)
- **标签**: `border-radius: 20px`，带 emoji 前缀 (如 🎙️)

#### 截图展示

- 图片圆角 12px
- 阴影 `box-shadow: 0 8px 30px rgba(139, 92, 246, 0.2)`
- 边框 `1px solid #e9d5ff`

**特殊布局提示**：如果某个新闻有4张截图，其中1张图片较长（如完整推文），另外3张较短（如功能截图），可以考虑使用**左1右3布局**（左侧1张大图 + 右侧3张小图垂直排列），实现主次分明的视觉效果。详细实现方法见 [`LAYOUT-1-3-EXAMPLE.md`](./LAYOUT-1-3-EXAMPLE.md)。


### 4. 底部 (Footer - Redesigned)

底部需要特别注意新的设计结构：

- **背景**: 浅色渐变 `linear-gradient(to bottom, rgba(255, 255, 255, 0.9), rgba(245, 243, 255, 0.95))`
- **主要标题**: "✨ 加入「小禾AI交流群」" (左右可带星星 emoji)，加大字重
- **副标题 (Slogan)**:
    1. 第一行: 普通深灰色说明
    2. 第二行: **胶囊样式** (Capsule Style) -> `border-radius: 30px`, 淡紫背景, 深紫文字, `display: inline-block`, `margin-bottom: 50px` (大间距)
- **二维码**:
    - 单图居中展示
    - 图片带悬浮效果 (Hover transform)
    - 阴影加重

### 5. 水印 (Watermark - Content Protection)

**⚠️ 重要**: 所有生成的HTML页面都**必须**包含防盗用水印！

#### 设计理念
- **目的**: 防止内容被他人窃取或搬运，保护原创内容版权
- **原则**: 既要起到防盗作用，又不能影响用户阅读体验
- **平衡点**: 透明度控制在5%-8%之间，水印可见但不干扰

#### 实现方法
使用CSS `body::after` 伪元素 + 内联SVG背景图实现：

```css
body {
    position: relative; /* 必须设置，为水印定位提供基准 */
}

body::after {
    content: "";
    position: fixed;       /* 固定定位，滚动时水印始终覆盖 */
    top: 0;
    left: 0;
    width: 200%;          /* 超大尺寸确保完整覆盖 */
    height: 200%;
    pointer-events: none; /* 不阻挡页面交互 */
    z-index: 9999;        /* 最高层级 */
    background-size: 300px 150px;
    background-image: url("data:image/svg+xml,..."); /* SVG水印 */
    transform: translate(-25%, -25%);
}
```

#### 水印参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| **水印文字** | `清华小禾说AI` | 默认品牌名称 |
| **字体大小** | `16px` | SVG中的font-size |
| **旋转角度** | `-35度` | 斜角排列，与水平线夹角 |
| **透明度** | `0.06` (6%) | fill-opacity，**关键参数** |
| **颜色** | `#9333ea` | 紫色，与页面主题一致 |
| **间距** | `300x150px` | 水印重复单元大小 |

#### 透明度调整建议

```
太淡 (不推荐)     合适范围         太浓 (影响阅读)
    ↓               ↓                    ↓
   3%  4%   [5%  6%  7%  8%]   9%  10%  12%

推荐值: 6% (0.06) - 经过实测的最佳平衡点
```

#### 修改水印文字

如需修改水印内容，编辑SVG中的文字部分：

```svg
<!-- 当前: 清华小禾说AI -->
<text ...>清华小禾说AI</text>

<!-- 修改为其他品牌 -->
<text ...>小禾说AI (公众号)</text>
```

**注意**: 修改后需同步调整：
- `background-size`: 文字变长时增大宽度（如`350px 150px`）
- `transform rotate`: 旋转中心点需对应新的宽度（如`rotate(-35, 175, 75)`）

#### 实施检查清单

生成HTML时，确保：
- ✅ CSS文件中包含完整的水印代码
- ✅ `body` 元素有 `position: relative`
- ✅ `body::after` 伪元素存在且样式完整
- ✅ 透明度设置在 5%-8% 范围内
- ✅ 水印文字与品牌一致
- ✅ 在浏览器中预览，确认水印可见但不影响阅读

**📖 详细技术文档**: 见 [`WATERMARK.md`](./WATERMARK.md) - 包含完整的实现原理、参数调优经验、常见问题解决方案



## HTML 模板 (Template)

本技能使用预定义的 HTML 模板文件：
**文件路径**: `templates/layout.html` (相对于 SKILL.md 所在目录)

### 模板使用逻辑
1. 读取 `templates/layout.html` 内容。
2. 查找并替换以下占位符：
   - `{{TITLE}}`: 页面 `<title>` 标签内容 (例如 "2026/01/17 硅谷AI圈动态")
   - `{{DATE_TITLE}}`: 头部大标题 (例如 "2026/01/17 硅谷AI圈动态")
   - `<!-- OVERVIEW_ROWS_PLACEHOLDER -->`: 插入生成的表格行 `<tr>...</tr>` HTML
   - `<!-- DETAIL_CARDS_PLACEHOLDER -->`: 插入所有生成的详情卡片 `<section class="detail-card">...</section>` HTML

### 详情卡片生成逻辑
循环处理 Markdown 中的每个新闻条目，生成如下 HTML 结构并拼接：

```html
<section class="detail-card">
    <div class="detail-header">
        <div class="detail-number">N</div>
        <div class="detail-title-group">
            <h3 class="detail-title">Entity - Title</h3>
        </div>
    </div>
    <div class="detail-meta">
        <span><strong>发布者</strong>：Author Name</span>
        <span><strong>时间</strong>：Time info</span>
    </div>
    <div class="detail-content">
        <!-- Content sections converted from Markdown -->
        <div class="content-section">
            <h4>🚀 Subtitle</h4>
            <ul class="content-list">
                <li>List item content...</li>
            </ul>
        </div>
        <!-- Screenshots section -->
        <div class="content-section">
            <h4>📸 原帖截图</h4>
            <div class="screenshots">
                <div class="screenshot-item">
                    <img src="./path/to/screenshot.png" alt="Alt Text">
                </div>
            </div>
        </div>
    </div>
</section>
```


## 资源路径参考

- Logo: `../assets/小禾说AI logo.png`
- 加群二维码: (需确认最新资源) 暂时使用 `../assets/0116_1.JPG` 或根据日期推断
- 截图存放: `screenshots/`

## 输出文件命名

```
ai_posts_summary_YYYY-MM-DD.html
```

---
name: md-2-html
description: Convert AI Today Markdown summaries into a styled HTML page with the "Light Purple/White" design, refined typography, specific footer layout, and responsive structure.
---

# AI Today 日报 HTML 生成技能 (Light Theme)

## 概述

将 AI 日报的 Markdown 内容转换为**日系/清新/明亮**的紫色主题 HTML 页面。页面采用白色半透明叠加态设计，视觉轻盈，适合阅读和移动端分享。

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
            <h4>📸 相关截图</h4>
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

---
name: md-2-html
description: Convert AI Today Markdown summaries into a styled HTML page with the specified purple/glassmorphism design, layout sections, assets, and output naming; use when generating or updating the AI Today md-to-html output.
---

# AI Today 日报 HTML 生成技能

## 概述

将 AI 日报的 Markdown 内容转换为精美的紫色主题 HTML 页面，采用毛玻璃设计风格，移动端友好，适合发朋友圈分享。

## 设计规范

### 1. 紫色背景 (Purple Aesthetics)

```css
:root {
    --purple-deep: #1a0a2e;
    --purple-mid: #2d1b4e;
    --purple-light: #4a2c7a;
    --purple-glow: #7c3aed;
    --purple-aurora: #a855f7;
    --purple-soft: #c4b5fd;
    --text-primary: #f0e6ff;
    --text-secondary: #c9b8e8;
    --text-muted: #9d8abf;
    --glass-bg: rgba(255, 255, 255, 0.08);
    --glass-border: rgba(255, 255, 255, 0.15);
}
```

- 背景：深紫到极光紫的静态渐变 `linear-gradient(135deg, #0f0515, #1a0a2e, #2d1b4e, #1f1035, #150a25, #0a0510)`
- 静态光效背景（无动画，适合截图）
- 使用 `radial-gradient` 制造柔和光晕感

### 2. 毛玻璃卡片 (Glassmorphism)

```css
.glass-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    padding: 32px;
}
```

- 半透明磨砂质感
- 悬停时轻微上浮 `transform: translateY(-4px)`
- 边框泛起紫光 `border-color: rgba(168, 85, 247, 0.3)`
- 顶部高光线条装饰

### 3. 清新可爱 (Fresh & Cute)

- 大圆角设计：卡片 `24px`，标签 `20px`，按钮 `50px`
- 编号使用渐变圆角方块 `14px` 圆角
- 语音/标签使用 emoji + 文字组合
- 无动画效果，静态页面适合截图分享

### 4. 移动端友好 (Mobile Friendly)

```css
@media (max-width: 768px) {
    .container { padding: 24px 16px; }
    .main-title { font-size: 2rem; }
    .glass-card { padding: 24px 20px; border-radius: 20px; }
    .detail-content { padding-left: 0; margin-top: 16px; }
}
```

- 最大宽度 `900px`，居中布局
- 一个区块一个区块，垂直滚动
- 截图垂直排列，完整显示不裁剪

### 5. 截图展示 (Screenshots)

```css
.screenshots {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.screenshot-item {
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 8px;
}

.screenshot-item img {
    width: 100%;
    height: auto;
    border-radius: 12px;
}
```

- 垂直排列，每张截图一行
- 图片自适应宽度，保持原始比例
- 完整显示，不裁剪

## 页面结构

### 头部 (Header)
```html
<header class="header">
    <div class="logo-container">
        <img src="../assets/小禾说AI logo.png" class="logo">
        <span class="main-title-inline">硅谷 AI 圈动态</span>
    </div>
    <div class="date-badge-row">
        <div class="date-badge">日期 · 过去24小时精选</div>
    </div>
</header>
```

**注意**：
- Logo 和标题使用 `inline-flex` 对齐，标题使用 `<span>` 而非 `<h1>` 以确保垂直居中
- Logo 尺寸 56px，标题 line-height 也设为 56px 保持对齐
- 日期徽章单独一行，不包含 logo

### 概览卡片 (Overview)
```html
<section class="glass-card overview-card">
    <h2 class="overview-title">
        <img src="../assets/小禾说AI logo.png" class="section-logo">
        今日总览
    </h2>
    <p class="overview-text">概述文字，使用 <span class="highlight">高亮</span></p>
    <table class="event-table">...</table>
</section>
```

**注意**：使用小禾 logo 替代 emoji 作为标题图标

### 详情卡片 (Detail Card)
```html
<section class="glass-card detail-card">
    <div class="detail-header">
        <div class="detail-number">1</div>
        <div class="detail-title-group">
            <h3 class="detail-title">标题</h3>
            <div class="detail-meta">
                <span>👤 发布者</span>
                <span>🕐 时间</span>
            </div>
        </div>
    </div>
    <div class="detail-content">
        <div class="content-section">
            <h4>小标题</h4>
            <ul class="content-list">
                <li>内容项，<span class="highlight">高亮词</span></li>
            </ul>
        </div>
        <div class="screenshots">...</div>
    </div>
</section>
```

### 底部 (Footer)
```html
<footer class="footer">
    <div class="qr-section">
        <h3>📱 关注小禾说AI</h3>
        <div class="qr-grid">
            <div class="qr-item">
                <div class="qr-image"><img src="二维码路径"></div>
                <span class="qr-label">标签</span>
            </div>
        </div>
    </div>
    <p class="copyright">© 2026 小禾说AI</p>
</footer>
```

## 资源路径

- Logo: `../assets/小禾说AI logo.png`
- 公众号二维码: `../assets/【小禾说AI】公众号二维码.jpg`
- 视频号二维码: `../assets/【清华小禾说AI】视频号二维码.jpg`
- 截图目录: `screenshots/`

## 命名规范

生成的文件命名格式：`ai_posts_summary_YYYY-MM-DD-ghc.html`

## 参考模板

完整模板参考：`archives-260116/ai_posts_summary_2026-01-16-ghc.html`

## 使用说明

1. 读取 Markdown 日报内容
2. 解析标题、日期、概览、详情等结构
3. 按照上述设计规范生成 HTML
4. 保持一个区块一个区块的卡片布局
5. 确保移动端显示效果良好


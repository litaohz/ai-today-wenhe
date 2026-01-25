# 更新日志 - 左1右3布局功能

**更新日期**: 2026-01-24  
**更新人**: Antigravity  
**版本**: v2.1

## 更新内容

本次更新为 `md-2-html` 技能添加了全新的**左1右3特殊布局**功能，用于4张截图的主次分明展示。

## 新增文件

### 1. LAYOUT-1-3-EXAMPLE.md (布局使用示例)
- **字节数**: ~4,500
- **内容**: 完整的使用指南
  - 使用场景说明
  - HTML结构示例
  - 布局特性详解
  - 实现原理分析
  - 与其他布局的对比
  - 注意事项和最佳实践
  - 实际案例参考

## 修改文件

### 1. SKILL.md
- **修改位置**: 第119-151行
- **新增章节**: "特殊布局：左1右3 (1+3 Layout)"
- **新增内容**:
  - 布局结构说明
  - 使用场景定义
  - 完整HTML结构示例
  - 关键特性列表（4个要点）
  - 响应式说明

### 2. scripts/style.css
- **修改位置**: 第524-570行（桌面端）+ 第736-743行（移动端）
- **新增内容**:
  - `.screenshots-layout-1-3` 容器样式
  - `.screenshot-main` 左侧主图样式
  - `.screenshot-side` 右侧容器样式
  - `.screenshot-item` 右侧图片项样式
  - 移动端响应式适配

## 技术细节

### 核心实现

```css
/* 桌面端：Grid布局 */
.screenshots-layout-1-3 {
    display: grid;
    grid-template-columns: 1.5fr 1fr;  /* 左侧占1.5份，右侧占1份 */
    gap: 15px;
}

/* 左侧主图：完整显示 */
.screenshot-main img {
    object-fit: contain;  /* 不裁剪 */
    height: auto;
}

/* 右侧3图：均匀分布 */
.screenshot-side {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.screenshot-side .screenshot-item {
    flex: 1;  /* 平均分配高度 */
}
```

### 关键特性

1. **主次分明**: 左侧1.5倍宽度，突出主图
2. **底部对齐**: 通过flex布局实现左右底部完美对齐
3. **内容完整**: 左侧使用contain，确保不裁剪重要内容
4. **响应式**: 移动端自动切换为单列布局

## HTML 结构

```html
<div class="screenshots-layout-1-3">
    <div class="screenshot-main">
        <img src="./1-0.png" alt="主要截图">
    </div>
    <div class="screenshot-side">
        <div class="screenshot-item"><img src="./1-1.png" alt="截图1"></div>
        <div class="screenshot-item"><img src="./1-2.png" alt="截图2"></div>
        <div class="screenshot-item"><img src="./1-3.png" alt="截图3"></div>
    </div>
</div>
```

## 使用场景

### ✅ 适用场景
- 产品发布（主图展示产品，右侧展示功能）
- 功能演示（主图展示核心，右侧展示步骤）
- 对比展示（主图展示整体，右侧展示细节）

### ❌ 不适用场景
- 4张图同等重要（建议使用2x2网格布局）
- 图片尺寸差异过大
- 需要横向对比的场景

## 实际案例

**参考文件**: `archives-260123/ai_posts_summary_2026-01-23.html`

在 **Cursor 2.4 版本发布** 的新闻中首次使用此布局：
- **左侧**: 完整的推文截图（包含文字说明和视频预览）
- **右侧**: 3张功能演示截图（Subagents、Image Generation、Ask Questions）

**效果评价**: 
- ✅ 主次分明，视觉焦点清晰
- ✅ 左右底部对齐，布局平衡
- ✅ 左侧内容完整显示，无裁剪
- ✅ 移动端自动适配，体验良好

## 开发历程

### 问题1: 左侧图片内容被裁剪
- **原因**: 使用了 `object-fit: cover`
- **解决**: 改为 `object-fit: contain`
- **效果**: 图片完整显示，文字不被截断

### 问题2: 左右底部不对齐
- **原因**: 左侧固定高度 + 垂直居中导致上下留白
- **解决**: 
  - 左侧改为 `align-items: flex-start` + `height: auto`
  - 右侧使用 `flex: 1` 让3张图平均分配高度
- **效果**: 左右底部完美对齐

### 问题3: 右侧图片高度不一致
- **原因**: 使用 `height: auto` 导致图片按原始比例显示
- **解决**: 使用 `flex: 1` + `height: 100%` + `object-fit: cover`
- **效果**: 右侧3张图高度一致，均匀分布

## 响应式设计

### 桌面端 (≥768px)
- 左右两列布局
- 左侧占 1.5fr，右侧占 1fr
- 图片间距 15px

### 移动端 (<768px)
- 单列布局
- 图片按顺序垂直排列
- 每张图片宽度 100%
- 右侧图片取消 `flex: 1`，恢复自然高度

## 文件结构

```
.agent/skills/md-2-html/
├── SKILL.md                      (已更新：新增左1右3说明)
├── LAYOUT-1-3-EXAMPLE.md         (新增：使用示例)
├── CHANGELOG-LAYOUT-1-3.md       (新增：本更新日志)
├── CHANGELOG-WATERMARK.md        (已有：水印功能日志)
├── WATERMARK.md                  (已有：水印详细文档)
├── WATERMARK-QUICK-REF.md        (已有：水印快速参考)
├── scripts/
│   └── style.css                 (已更新：新增左1右3样式)
└── templates/
    └── layout.html               (无需修改)
```

## 兼容性

- ✅ Chrome (所有版本)
- ✅ Firefox (所有版本)
- ✅ Safari (所有版本)
- ✅ Edge (所有版本)
- ⚠️ IE 11 (Grid布局需polyfill)

## 性能影响

- **渲染**: 无明显影响（使用原生Grid和Flex）
- **内存**: 无额外开销
- **交互**: 无影响

## 后续维护

### 调整布局比例

如需修改左右比例，编辑 `style.css` 第526行：

```css
/* 当前：左侧1.5倍，右侧1倍 */
grid-template-columns: 1.5fr 1fr;

/* 示例：左侧2倍，右侧1倍（更突出主图） */
grid-template-columns: 2fr 1fr;

/* 示例：左右相等 */
grid-template-columns: 1fr 1fr;
```

### 调整图片间距

修改 `gap` 属性（第528行）：

```css
gap: 15px;  /* 当前值 */
gap: 20px;  /* 增大间距 */
gap: 10px;  /* 减小间距 */
```

## 与现有布局的集成

本次更新与现有布局完全兼容，不影响：
- ✅ 单图布局
- ✅ 2图并排布局 (`.screenshots-grid-2`)
- ✅ 3图并排布局 (`.screenshots-grid-3`)
- ✅ 4图2x2布局 (`.screenshots-grid-4`)

## 使用建议

1. **优先使用场景**: 产品发布、功能演示类新闻
2. **图片选择**: 左侧选择信息量大的图片，右侧选择细节图
3. **图片尺寸**: 左侧建议竖图或方图，右侧建议尺寸相近
4. **测试验证**: 生成后在桌面端和移动端都要预览验证

## 注意事项

1. **左侧图片**: 使用 `contain` 模式，确保内容完整
2. **右侧图片**: 使用 `cover` 模式，可能裁剪边缘
3. **移动端**: 自动切换为单列，确保每张图都清晰
4. **命名规范**: 建议使用 `1-0.png`, `1-1.png`, `1-2.png`, `1-3.png`

## 参考链接

- 使用示例: [LAYOUT-1-3-EXAMPLE.md](./LAYOUT-1-3-EXAMPLE.md)
- 主技能文档: [SKILL.md](./SKILL.md)
- 实际案例: `archives-260123/ai_posts_summary_2026-01-23.html`

## 问题反馈

如遇到布局相关问题，请查阅 `LAYOUT-1-3-EXAMPLE.md` 的使用说明。

---

**更新完成** ✅

本次更新为AI Today日报增加了更灵活的截图展示方式，特别适合产品发布类新闻的视觉呈现。

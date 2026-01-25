# 左1右3 布局使用示例

## 概述

这是一个特殊的4图布局方案，适用于需要突出展示主图的场景。

## 使用场景

- ✅ **产品发布**：主图展示产品界面，右侧3张图展示功能细节
- ✅ **功能演示**：主图展示核心功能，右侧展示使用步骤
- ✅ **对比展示**：主图展示整体效果，右侧展示局部细节
- ❌ **不适用**：4张图同等重要的场景（建议使用2x2网格布局）

## HTML 结构示例

```html
<div class="content-section">
    <h4>📸 原帖截图</h4>
    <div class="screenshots-layout-1-3">
        <!-- 左侧主图 -->
        <div class="screenshot-main">
            <img src="./1-0.png" alt="Cursor 2.4 主要功能截图">
        </div>
        
        <!-- 右侧3张小图 -->
        <div class="screenshot-side">
            <div class="screenshot-item">
                <img src="./1-1.png" alt="Subagents 功能">
            </div>
            <div class="screenshot-item">
                <img src="./1-2.png" alt="Image Generation 功能">
            </div>
            <div class="screenshot-item">
                <img src="./1-3.png" alt="Ask Questions 功能">
            </div>
        </div>
    </div>
</div>
```

## 布局特性

### 桌面端（Desktop）

- **左侧大图**：
  - 占据 1.5 份宽度
  - 使用 `object-fit: contain` 完整显示内容
  - 顶部对齐（`align-items: flex-start`）
  - 高度自适应（`height: auto`）

- **右侧3图**：
  - 占据 1 份宽度
  - 垂直排列，均匀分布（`flex: 1`）
  - 使用 `object-fit: cover` 填充容器
  - 自动匹配左侧图片高度

- **视觉效果**：
  - 左右两侧底部完美对齐
  - 图片间距 15px
  - 统一的圆角和阴影效果

### 移动端（Mobile）

- 自动切换为单列布局
- 图片按顺序垂直排列：1-0.png → 1-1.png → 1-2.png → 1-3.png
- 每张图片宽度100%，高度自适应

## 实现原理

### 关键CSS技术

1. **Grid 布局**：
   ```css
   grid-template-columns: 1.5fr 1fr;
   ```
   左侧占1.5份，右侧占1份，实现主次分明

2. **Flexbox 垂直分布**：
   ```css
   flex-direction: column;
   justify-content: space-between;
   ```
   右侧3张图均匀分布

3. **高度自适应**：
   ```css
   .screenshot-side .screenshot-item {
       flex: 1;  /* 平均分配可用空间 */
   }
   ```
   每张小图自动填充1/3高度

4. **底部对齐**：
   - 左侧：`height: auto` + `align-items: flex-start`
   - 右侧：`flex: 1` 让3张图总高度匹配左侧

## 与其他布局的对比

| 布局方式 | 适用场景 | 图片数量 | 视觉效果 |
|---------|---------|---------|---------|
| **左1右3** | 主次分明 | 4张 | 突出主图 |
| **2x2网格** | 同等重要 | 4张 | 平衡展示 |
| **3列网格** | 并列展示 | 3张 | 横向对比 |
| **2列网格** | 对比展示 | 2张 | 左右对比 |

## 注意事项

1. **图片尺寸**：
   - 左侧主图建议使用竖图或方图
   - 右侧3张图建议尺寸相近
   - 避免使用超宽横图作为主图

2. **内容完整性**：
   - 左侧使用 `contain` 确保内容不被裁剪
   - 右侧使用 `cover` 填充容器，可能裁剪边缘

3. **响应式**：
   - 移动端会自动切换为单列
   - 确保每张图片在移动端也清晰可见

## 实际案例

参考文件：`archives-260123/ai_posts_summary_2026-01-23.html`

在 Cursor 2.4 版本发布的新闻中使用了此布局：
- 左侧：完整的推文截图（包含文字和视频）
- 右侧：3张功能演示截图

效果：主次分明，视觉平衡，阅读体验优秀。

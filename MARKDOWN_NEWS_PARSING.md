# Markdown 新闻解析功能说明

## 功能概述

将 Markdown 文件（`data/chatgpt_scheduler/{date}.md`）中的"要闻 Top 8"解析成单独的新闻条目，并自动合并到"其他资讯"模块中显示。

## 实现方式

### 1. 数据解析（`frontend-react/src/store/appStore.ts`）

当用户选择日期后，系统会：

1. **获取 TLDR 数据**：从后端获取爬取的数据
2. **获取 Markdown 内容**：调用 `/api/v1/scheduler/markdown/{date}` 获取对应日期的 MD 文件
3. **解析新闻条目**：使用正则表达式提取每条新闻
4. **合并数据**：将解析出的新闻添加到"其他资讯" section 中

### 2. 解析规则

**匹配模式**：
```javascript
/\d+\.\s+\*\*(.+?)\*\*\s+来源：(.+?)｜(.+?)\s+链接：(https?:\/\/[^\s]+)/g
```

**匹配格式**：
```
1. **中文标题｜English Title**  
   来源：Reuters｜2025‑10‑07 20:00 JST  
   链接：https://example.com/article
```

**提取内容**：
- **标题**：`**...**` 中 `｜` 之前的中文部分
- **来源**：`来源：` 后面到 `｜` 之前的内容
- **时间**：第二个 `｜` 后到换行前的内容
- **链接**：`链接：` 后面的 URL

### 3. 数据结构

每条解析的新闻会被转换为：

```typescript
{
  title: "中文标题",
  content: "来源：Reuters | 2025‑10‑07 20:00 JST",
  links: [{
    url: "https://...",
    text: "查看原文"
  }],
  word_count: 标题字数
}
```

### 4. 展示方式（`frontend-react/src/components/DataDisplay.tsx`）

- **模块标题**：🌐 其他资讯
- **列表样式**：每条新闻显示为一个可点击的卡片
- **卡片内容**：
  - 📰 图标 + 新闻标题
  - 来源和时间信息
- **交互效果**：
  - hover 时卡片高亮并向右移动
  - 点击跳转到原文链接

## 显示效果

```
┌─────────────────────────────────────────┐
│ 🌐 其他资讯                              │
├─────────────────────────────────────────┤
│ 📰 OpenAI 禁止疑似中国关联账号...        │
│    来源：Reuters | 2025‑10‑07 20:00 JST │
├─────────────────────────────────────────┤
│ 📰 OpenAI 与 AMD 签定芯片供给协议...     │
│    来源：Reuters | 2025‑10‑07 03:00 JST │
├─────────────────────────────────────────┤
│ ... (TLDR 原有的其他资讯)                │
└─────────────────────────────────────────┘
```

## 数据流程

```
用户选择日期 (2025-10-07)
    ↓
获取 TLDR 数据
    ↓
获取 Markdown 文件 (2025-10-07.md)
    ↓
解析"要闻 Top 8"
    ↓
提取每条新闻的标题、来源、时间、链接
    ↓
查找或创建"其他资讯" section
    ↓
将解析的新闻添加到 section.articles 中
    ↓
前端渲染显示
```

## 合并逻辑

1. **如果 TLDR 数据中已存在"其他资讯" section**：
   - 将解析的新闻追加到现有 articles 中
   - 更新 article_count

2. **如果不存在**：
   - 创建新的"其他资讯" section
   - 包含解析的新闻条目

## 过滤规则

只显示以下 section：
- ✅ `Miscellaneous` / `其他资讯`
- ✅ `Quick Links` / `快速链接`

隐藏其他所有 section：
- ❌ `Headlines & Launches`
- ❌ `Deep Dives & Analysis`
- ❌ `Engineering & Research`
- ❌ 其他所有 section

## 测试

运行测试脚本：
```bash
node test_markdown_parse.js
```

## 注意事项

1. **Markdown 格式要求**：
   - 必须严格按照指定格式编写
   - 标题必须用 `**...**` 包裹
   - 必须包含 `来源：`、`｜` 和 `链接：` 标记

2. **容错处理**：
   - 如果 Markdown 文件不存在，不影响主流程
   - 如果解析失败，显示原有的 TLDR 数据
   - 不会中断页面渲染

3. **性能考虑**：
   - 解析在前端进行，不增加后端负担
   - 正则匹配效率高
   - 只在选择日期时触发一次

## 相关文件

- `frontend-react/src/store/appStore.ts` - 数据获取和解析逻辑
- `frontend-react/src/components/DataDisplay.tsx` - 展示组件
- `frontend-react/src/services/apiManager.ts` - API 调用
- `src/api/routes.py` - 后端 Markdown 文件读取接口
- `test_markdown_parse.js` - 解析逻辑测试脚本

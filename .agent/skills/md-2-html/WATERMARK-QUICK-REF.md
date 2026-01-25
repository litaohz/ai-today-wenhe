# 水印快速参考 (Quick Reference)

## 最小可用配置

```css
body {
    position: relative;
}

body::after {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 200%;
    height: 200%;
    pointer-events: none;
    z-index: 9999;
    background-size: 300px 150px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='150'%3E%3Ctext x='50%25' y='50%25' font-family='Noto Sans SC, sans-serif' font-size='16' fill='%239333ea' fill-opacity='0.06' text-anchor='middle' dominant-baseline='middle' transform='rotate(-35, 150, 75)'%3E清华小禾说AI%3C/text%3E%3C/svg%3E");
    transform: translate(-25%, -25%);
}
```

## 常用配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 水印文字 | `清华小禾说AI` | 品牌名称 |
| 透明度 | `0.06` | 6%，推荐值 |
| 颜色 | `#9333ea` | 紫色 |
| 字体大小 | `16px` | 文字尺寸 |
| 旋转角度 | `-35度` | 斜角 |
| 重复间距 | `300x150px` | 水印间距 |

## 一行命令

复制CSS文件：
```bash
cp .agent/skills/md-2-html/scripts/style.css archives-YYMMDD/style.css
```

## 调整透明度

只需修改一个值（`fill-opacity`）：

```
0.05 → 5%  (最淡)
0.06 → 6%  (推荐)
0.07 → 7%  (稍浓)
0.08 → 8%  (最浓)
```

## 修改文字

在SVG中找到并替换：
```xml
<text ...>清华小禾说AI</text>
```

## 检查清单

- [ ] `body` 有 `position: relative`
- [ ] `body::after` 存在
- [ ] `pointer-events: none`
- [ ] `z-index: 9999`
- [ ] 透明度 5%-8%
- [ ] 浏览器预览确认

## 故障排查

| 问题 | 解决 |
|------|------|
| 看不到水印 | 检查 `z-index` 和透明度 |
| 无法点击页面 | 添加 `pointer-events: none` |
| 滚动后消失 | 使用 `position: fixed` |

## 更多信息

详见 [WATERMARK.md](./WATERMARK.md)

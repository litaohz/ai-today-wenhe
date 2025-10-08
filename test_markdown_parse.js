// 测试 Markdown 解析逻辑

const testContent = `
# AI 每日简报 — 2025‑10‑08 (JST)

## 1) 要闻 Top 8  
（中文 / English + 原文链接 + 来源 + 发布时间 JST）

1. **OpenAI 禁止疑似中国关联账号寻求监控方案｜OpenAI bans suspected China‑linked accounts for seeking surveillance proposals**  
   来源：Reuters｜2025‑10‑07 20:00 JST  
   链接：https://www.reuters.com/world/china/openai-bans-suspected-china-linked-accounts-seeking-surveillance-proposals-2025-10-07/ :contentReference[oaicite:0]{index=0}

2. **OpenAI 与 AMD 签定芯片供给协议 & 获 AMD 股权期权｜AMD signs AI chip‑supply deal with OpenAI, gives it option to take a 10% stake**  
   来源：Reuters｜2025‑10‑07 03:00 JST  
   链接：https://www.reuters.com/business/amd-signs-ai-chip-supply-deal-with-openai-gives-it-option-take-10-stake-2025-10-06/ :contentReference[oaicite:1]{index=1}
`;

function parseMarkdownNews(mdContent) {
  const articles = [];
  
  // 匹配格式：数字. **标题｜英文标题**
  // 然后提取来源和链接
  const newsPattern = /\d+\.\s+\*\*(.+?)\*\*\s+来源：(.+?)｜(.+?)\s+链接：(https?:\/\/[^\s]+)/g;
  
  let match;
  while ((match = newsPattern.exec(mdContent)) !== null) {
    const [, title, source, time, url] = match;
    
    // 提取中文标题（｜之前的部分）
    const chineseTitle = title.split('｜')[0].trim();
    
    articles.push({
      title: chineseTitle,
      content: `来源：${source} | ${time}`,
      links: [{
        url: url,
        text: '查看原文'
      }],
      word_count: chineseTitle.length
    });
  }
  
  return articles;
}

const result = parseMarkdownNews(testContent);
console.log('解析结果：');
console.log(JSON.stringify(result, null, 2));
console.log(`\n共解析出 ${result.length} 条新闻`);

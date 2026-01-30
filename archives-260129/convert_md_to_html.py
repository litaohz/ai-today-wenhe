
import re
import os
import shutil
from datetime import datetime, timedelta, timezone

# Paths
BASE_DIR = r"c:\Users\98554\Downloads\ai-today-wenhe"
ARCHIVE_FOLDER = "archives-260129"
DATE_STR = "2026-01-29"

INPUT_MD = os.path.join(BASE_DIR, ARCHIVE_FOLDER, f"ai_posts_summary_{DATE_STR}.md")
OUTPUT_HTML = os.path.join(BASE_DIR, ARCHIVE_FOLDER, f"ai_posts_summary_{DATE_STR}.html")
TEMPLATE_HTML = os.path.join(BASE_DIR, ".agent", "skills", "md-2-html", "templates", "layout.html")
STYLE_CSS_SRC = os.path.join(BASE_DIR, ".agent", "skills", "md-2-html", "scripts", "style.css")
STYLE_CSS_DEST = os.path.join(BASE_DIR, ARCHIVE_FOLDER, "style.css")

def clean_punctuation(text):
    if not text:
        return ""
    
    # Preserve times like 12:34
    times = re.findall(r'\d{1,2}:\d{2}(?::\d{2})?', text)
    for i, t in enumerate(times):
        text = text.replace(t, f"__TIME_{i}__")

    # Replace only if surrounded by non-ASCII or if it's a common case
    # Actually the skill says "all Chinese punctuation must use full-width", 
    # but lets be smart to not mess up URLs or code.
    # URLs are already removed, and markdown is processed later.
    
    text = text.replace(",", "，")
    text = text.replace(":", "：")
    text = text.replace(";", "；")
    text = text.replace("?", "？")
    text = text.replace("!", "！")
    
    # Restore times
    for i, t in enumerate(times):
        text = text.replace(f"__TIME_{i}__", t)
    
    return text

def process_time_string(time_str):
    if not time_str:
        return ""
        
    # Pattern: YYYY-MM-DD HH:MM UTC
    match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC', time_str)
    if match:
        try:
            dt_str = match.group(1)
            dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
            dt = dt.replace(tzinfo=timezone.utc)
            beijing_tz = timezone(timedelta(hours=8))
            beijing_dt = dt.astimezone(beijing_tz)
            return beijing_dt.strftime('%Y-%m-%d %H:%M 北京时间')
        except Exception as e:
            print(f"Time conversion error: {e}")
            return time_str

    return time_str

KNOWN_PERSONS = {
    "Andrej Karpathy": "OpenAI前创始团队",
    "Elon Musk": "X CEO",
    "Sam Altman": "OpenAI CEO",
    "Dario Amodei": "Anthropic CEO",
    "Demis Hassabis": "Google DeepMind CEO",
    "Yann LeCun": "Meta Chief AI Scientist",
    "Greg Brockman": "OpenAI President",
    "Ilya Sutskever": "Safe Superintelligence Inc. Founder",
    "Fei-Fei Li": "Stanford HAI Co-Director",
    "Andrew Ng": "DeepLearning.AI Founder",
    "Jensen Huang": "NVIDIA CEO",
    "Mark Zuckerberg": "Meta CEO",
    "Satya Nadella": "Microsoft CEO",
    "Sundar Pichai": "Google CEO",
    "Tim Cook": "Apple CEO",
    "Michael Truell": "Cursor AI CEO",
}

def process_publisher(text):
    # Remove @handle
    text = re.sub(r'\s*\(@[a-zA-Z0-9_]+\)', '', text).strip()
    
    if text in KNOWN_PERSONS:
        return f"{text} ({KNOWN_PERSONS[text]})"
    
    if ' / ' in text:
        parts = text.split(' / ')
        processed_parts = []
        for p in parts:
            p = p.strip()
            if p in KNOWN_PERSONS:
                processed_parts.append(f"{p} ({KNOWN_PERSONS[p]})")
            else:
                processed_parts.append(p)
        return ' / '.join(processed_parts)
    
    # Check for personal names with comma title
    if ',' in text:
        name, title = [x.strip() for x in text.split(',', 1)]
        return f"{name} ({title})"
    
    return text

def parse_markdown(md_content):
    data = {}
    title_match = re.search(r'^# (.*)', md_content, re.M)
    data['title'] = title_match.group(1).strip() if title_match else "AI Today"
    
    overview_match = re.search(r'## 📊 总览\s*\n\s*(.*?)\n\s*\|', md_content, re.DOTALL)
    if overview_match:
        data['overview_text'] = overview_match.group(1).strip().replace('**', '')
    else:
        overview_match = re.search(r'## 📊 总览\s*\n\s*(.*?)\n', md_content, re.DOTALL)
        if overview_match:
            data['overview_text'] = overview_match.group(1).strip().replace('**', '')
            
    table_match = re.search(r'\| 主题 \| 关键事件 \|\s*\n\| :--- \| :--- \|\s*\n(.*?)\n\s*---', md_content, re.DOTALL)
    data['overview_rows'] = []
    if table_match:
        rows_text = table_match.group(1).strip().split('\n')
        for row in rows_text:
            cols = [c.strip() for c in row.split('|') if c.strip()]
            if len(cols) >= 2:
                theme = cols[0].replace('**', '')
                event = cols[1].replace('**', '')
                data['overview_rows'].append({'theme': theme, 'event': event})

    data['items'] = []
    sections = re.split(r'#### \d+\. ', md_content)
    for i in range(1, len(sections)):
        section_text = sections[i]
        item = {'id': i}
        lines = section_text.split('\n')
        full_title = lines[0].strip()
        if ' - ' in full_title:
            entity, title = full_title.split(' - ', 1)
            item['entity'] = entity.strip()
            item['title'] = title.strip()
        else:
            item['entity'] = ""
            item['title'] = full_title
        if item['title'].startswith('[') and item['title'].endswith(']'):
             item['title'] = item['title'][1:-1]
            
        pub_match = re.search(r'\*\*发布者\*\*: (.*)', section_text)
        item['publisher'] = process_publisher(pub_match.group(1).strip()) if pub_match else "Unknown"
        
        time_match = re.search(r'\*\*时间\*\*: (.*)', section_text)
        item['time'] = time_match.group(1).strip() if time_match else ""
            
        content_block_match = re.search(r'\*\*核心内容\*\*:\s*\n(.*?)(?=\n\s*\*\*链接\*\*|\n\s*!\[|\Z)', section_text, re.DOTALL)
        if content_block_match:
            content_text = content_block_match.group(1)
            single_group = {'subtitle': '核心内容', 'items': []}
            for line in content_text.split('\n'):
                line = line.strip()
                if line.startswith('- '):
                    single_group['items'].append(line[2:].strip())
            item['content_groups'] = [single_group]
            
        images = re.findall(r'!\[.*?\]\((.*?)\)', section_text)
        item['images'] = images
        data['items'].append(item)
        
    return data

def generate_html(data, template_path, output_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    html = html.replace('{{TITLE}}', data.get('title', 'AI Today'))
    html = html.replace('{{DATE_TITLE}}', data.get('title', 'AI Today'))
    
    rows_html = ""
    for row in data.get('overview_rows', []):
        theme = clean_punctuation(row['theme'])
        event = clean_punctuation(row['event'])
        rows_html += f"<tr><td><span class='topic-tag'>{theme}</span></td><td>{event}</td></tr>\n"
    html = html.replace('<!-- OVERVIEW_ROWS_PLACEHOLDER -->', rows_html)
    
    ov_text = clean_punctuation(data.get('overview_text', ''))
    html = re.sub(r'<p class="overview-text">.*?</p>', f'<p class="overview-text">{ov_text}</p>', html, flags=re.DOTALL)
    
    cards_html = ""
    for item in data.get('items', []):
        id_num = item['id']
        entity = clean_punctuation(item['entity'])
        title = clean_punctuation(item['title'])
        full_title = f"{entity} - {title}" if entity else title
        publisher = clean_punctuation(item['publisher'])
        time_str = clean_punctuation(process_time_string(item.get('time', '')))
        
        card = f"""
        <section class="detail-card">
            <div class="detail-header">
                <div class="detail-number">{id_num}</div>
                <div class="detail-title-group">
                    <h3 class="detail-title">{full_title}</h3>
                </div>
            </div>
            <div class="detail-meta">
                <span><strong>发布者</strong>：{publisher}</span>
                <span><strong>时间</strong>：{time_str}</span>
            </div>
            <div class="detail-content">
        """
        for group in item.get('content_groups', []):
            subtitle = clean_punctuation(group['subtitle'])
            card += f"""
                <div class="content-section">
                    <h4>🚀 {subtitle}</h4>
                    <ul class="content-list">
            """
            for list_item in group['items']:
                li_text = clean_punctuation(list_item)
                li_text = re.sub(r'\*\*(.*?)\*\*', lambda m: f'<strong>{m.group(1)[1:-1] if m.group(1).startswith("[") and m.group(1).endswith("]") else m.group(1)}</strong>', li_text)
                card += f"<li>{li_text}</li>"
            card += "</ul></div>"
            
        images = item.get('images', [])
        if images:
            card += '<div class="content-section"><h4>📸 原帖截图</h4>'
            count = len(images)
            if count == 1:
                 card += f'<div class="screenshots"><div class="screenshot-item"><img src="{images[0]}" alt="Screenshot"></div></div>'
            else:
                grid_class = f"screenshots-grid-{min(count, 4)}" 
                card += f'<div class="{grid_class}">'
                for img in images:
                    card += f'<div class="screenshot-item"><img src="{img}" alt="Screenshot"></div>'
                card += '</div>'
            card += "</div>"
        card += "</div></section>"
        cards_html += card
    html = html.replace('<!-- DETAIL_CARDS_PLACEHOLDER -->', cards_html)
    
    # Redesign Footer
    footer_html = """
        <footer class="footer">
            <div class="qr-section">
                <h3>✨ 加入「小禾AI交流群」</h3>
                <p class="qr-subtitle">不错过 <硅谷AI圈动态> 每日更新</p>
                <p class="qr-subtitle">长按或扫码上方二维码 · 备注「入群」</p>
                <div class="qr-grid">
                    <div class="qr-item">
                        <div class="qr-image">
                            <img src="../assets/0116_1.JPG" alt="扫码加群">
                        </div>
                    </div>
                </div>
            </div>
            <p class="copyright">© 2026 小禾说AI · AI Today Daily · All Rights Reserved</p>
        </footer>
    """
    html = re.sub(r'<footer class="footer">.*?</footer>', footer_html, html, flags=re.DOTALL)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated HTML at {output_path}")

def main():
    if not os.path.exists(INPUT_MD): return
    with open(INPUT_MD, 'r', encoding='utf-8') as f:
        data = parse_markdown(f.read())
    generate_html(data, TEMPLATE_HTML, OUTPUT_HTML)
    shutil.copy(STYLE_CSS_SRC, STYLE_CSS_DEST)

if __name__ == "__main__":
    main()


import re
import os
import shutil

# Paths
BASE_DIR = r"c:\Users\98554\Downloads\ai-today-wenhe"
INPUT_MD = os.path.join(BASE_DIR, "archives-260127", "ai_posts_summary_2026-01-27.md")
OUTPUT_HTML = os.path.join(BASE_DIR, "archives-260127", "ai_posts_summary_2026-01-27.html")
TEMPLATE_HTML = os.path.join(BASE_DIR, ".agent", "skills", "md-2-html", "templates", "layout.html")
STYLE_CSS_SRC = os.path.join(BASE_DIR, ".agent", "skills", "md-2-html", "scripts", "style.css")
STYLE_CSS_DEST = os.path.join(BASE_DIR, "archives-260127", "style.css")

def clean_punctuation(text):
    if not text:
        return ""
    # Full-width replacement (except in parentheses or specific patterns if complex, but simple global replace is requested)
    # The rule says: , -> ，, : -> ：, etc.
    # We should be careful not to replace inside HTML tags if we had them, but inputs are raw text.
    # Strategy: Replace text, but preserve time format like 12:34
    # First, placeholders for times
    times = re.findall(r'\d{1,2}:\d{2}(?::\d{2})?', text)
    for i, t in enumerate(times):
        text = text.replace(t, f"__TIME_{i}__")

    text = text.replace(",", "，")
    text = text.replace(":", "：")
    text = text.replace(";", "；")
    text = text.replace("?", "？")
    text = text.replace("!", "！")
    
    # Restore times
    for i, t in enumerate(times):
        text = text.replace(f"__TIME_{i}__", t)
    
    return text


# Known figures mapping (Name -> Title)
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
}

def process_publisher(text):
    # Remove @handle
    text = re.sub(r'\s*\(@[a-zA-Z0-9_]+\)', '', text).strip()
    
    # Check known persons
    if text in KNOWN_PERSONS:
        return f"{text} ({KNOWN_PERSONS[text]})"
    
    # Hardcoded rules for known figures if title missing (backup for partial matches if needed)
    if "Elon Musk" in text and "CEO" not in text:
        return "Elon Musk (X CEO)"
    
    # If it was "Name (@handle), Title" -> "Name, Title" -> "Name，Title" (punctuation processed later)
    # The rule: Personal publisher needs title in brackets.
    # text is now "Name" or "Name, Title"
    
    parts = text.split(',', 1)
    if len(parts) > 1:
        name = parts[0].strip()
        title = parts[1].strip()
        return f"{name} ({title})"
        
    return text

def parse_markdown(md_content):
    data = {}
    
    # 1. Title/Date
    title_match = re.search(r'^# (.*)', md_content, re.M)
    if title_match:
        data['title'] = title_match.group(1).strip()
    
    # 2. Overview
    overview_match = re.search(r'## 📊 总览\s*\n\s*(.*?)\n\s*\|', md_content, re.DOTALL)
    if overview_match:
        raw_ov = overview_match.group(1).strip()
        # Remove markdown bolding
        data['overview_text'] = raw_ov.replace('**', '')
    else:
        # Fallback if table doesn't follow immediately
        overview_match = re.search(r'## 📊 总览\s*\n\s*(.*?)\n', md_content, re.DOTALL)
        if overview_match:
            raw_ov = overview_match.group(1).strip()
            data['overview_text'] = raw_ov.replace('**', '')
            
    # 3. Table Rows
    table_match = re.search(r'\| 主题 \| 关键事件 \|\s*\n\| :--- \| :--- \|\s*\n(.*?)\n\s*---', md_content, re.DOTALL)
    data['overview_rows'] = []
    if table_match:
        rows_text = table_match.group(1).strip().split('\n')
        for row in rows_text:
            cols = [c.strip() for c in row.split('|') if c.strip()]
            if len(cols) >= 2:
                # Remove bold markers for HTML
                theme = cols[0].replace('**', '')
                event = cols[1].replace('**', '')
                data['overview_rows'].append({'theme': theme, 'event': event})

    # 4. Details
    data['items'] = []
    # Split by #### Number
    sections = re.split(r'#### \d+\. ', md_content)
    # First section is before the first item
    for i in range(1, len(sections)):
        section_text = sections[i]
        item = {}
        item['id'] = i
        
        # Title (First line)
        lines = section_text.split('\n')
        full_title = lines[0].strip()
        # Parse Entity/Title if possible "Entity - Title"
        if ' - ' in full_title:
            entity, title = full_title.split(' - ', 1)
            item['entity'] = entity.strip()
            item['title'] = title.strip()
        else:
            item['entity'] = ""
            item['title'] = full_title
            
        # Publisher
        pub_match = re.search(r'\*\*发布者\*\*: (.*)', section_text)
        if pub_match:
            raw_pub = pub_match.group(1).strip()
            item['publisher'] = process_publisher(raw_pub)
        
        # Time
        time_match = re.search(r'\*\*时间\*\*: (.*)', section_text)
        if time_match:
            item['time'] = time_match.group(1).strip()
            
        # Content Sections: "核心内容"
        # Find lines that are list items
        # Structure:
        # - **Subtitle**: Text
        # OR
        # - Text
        content_lines = []
        is_in_content = False
        
        # Extract content block: From "**核心内容**:" to "**链接**" or end
        content_block_match = re.search(r'\*\*核心内容\*\*:\s*\n(.*?)(?=\n\s*\*\*链接\*\*|\n\s*!\[)', section_text, re.DOTALL)
        if content_block_match:
            content_text = content_block_match.group(1)
            # NEW LOGIC: Single group "核心内容"
            # Instead of splitting by bold keys into subsections, we keep them as a single list.
            # The keys will be rendered as bold text within the li item.
            
            single_group = {'subtitle': '核心内容', 'items': []}
            
            for line in content_text.split('\n'):
                line = line.strip()
                if not line: continue
                
                if line.startswith('- '):
                    text = line[2:].strip()
                    single_group['items'].append(text)
            
            item['content_groups'] = [single_group]
            
        # Images
        # Find all ![.*](path)
        images = re.findall(r'!\[.*?\]\((.*?)\)', section_text)
        item['images'] = images
        
        data['items'].append(item)
        
    return data

def generate_html(data, template_path, output_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Replace metadata
    html = html.replace('{{TITLE}}', data.get('title', 'AI Today'))
    html = html.replace('{{DATE_TITLE}}', data.get('title', 'AI Today'))
    
    # Overview Rows
    rows_html = ""
    if 'overview_rows' in data:
        for row in data['overview_rows']:
            theme = clean_punctuation(row['theme'])
            event = clean_punctuation(row['event'])
            rows_html += f"<tr><td><span class='topic-tag'>{theme}</span></td><td>{event}</td></tr>\n"
    html = html.replace('<!-- OVERVIEW_ROWS_PLACEHOLDER -->', rows_html)
    
    # Overview Text
    ov_text = clean_punctuation(data.get('overview_text', ''))
    # Replace existing text content in template?
    # Template: <p class="overview-text">...</p>
    # We should Replace the content.
    # Regex replace to be safe
    html = re.sub(r'<p class="overview-text">.*?</p>', f'<p class="overview-text">{ov_text}</p>', html, flags=re.DOTALL)
    
    # Detail Cards
    cards_html = ""
    for item in data.get('items', []):
        id_num = item['id']
        entity = clean_punctuation(item['entity'])
        title = clean_punctuation(item['title'])
        full_title = f"{entity} - {title}" if entity else title
        publisher = clean_punctuation(item['publisher'])
        time_str = clean_punctuation(item['time'])
        if time_str:
            time_str += " 北京时间"
        
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
        
        # Content Groups
        for group in item.get('content_groups', []):
            subtitle = clean_punctuation(group['subtitle'])
            card += f"""
                <div class="content-section">
                    <h4>🚀 {subtitle}</h4>
                    <ul class="content-list">
            """
            for list_item in group['items']:
                # Clean markdown bolding from content if needed or keep it?
                # Template CSS has .highlight for strong.
                # So we should convert **Text** to <span class="highlight">Text</span> or <strong>Text</strong>
                # The util clean_punctuation might mess up <strong> tags if applied after.
                # Let's clean punctuation first then markdown?.
                # Actually clean_punctuation operates on text.
                # Let's do markdown conversion.
                
                li_text = clean_punctuation(list_item)
                # Convert **Text** to <strong>Text</strong>
                li_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', li_text)
                
                card += f"<li>{li_text}</li>"
            card += """
                    </ul>
                </div>
            """
            
        # Images
        images = item.get('images', [])
        if images:
            card += """
                <div class="content-section">
                    <h4>📸 原帖截图</h4>
            """
            # Logic for grid
            count = len(images)
            if count == 1:
                 card += '<div class="screenshots"><div class="screenshot-item">'
                 card += f'<img src="{images[0]}" alt="Screenshot">'
                 card += '</div></div>'
            elif count >= 2:
                # Use grid
                grid_class = f"screenshots-grid-{min(count, 4)}" # Max grid-4 defined in css?
                # CSS has grid-2, grid-3, grid-4.
                if count > 4: grid_class = "screenshots-grid-4" # Fallback
                
                card += f'<div class="{grid_class}">'
                for img in images:
                    card += '<div class="screenshot-item">'
                    card += f'<img src="{img}" alt="Screenshot">'
                    card += '</div>'
                card += '</div>'
                
            card += "</div>" # Close content-section
            
        card += """
            </div>
        </section>
        """
        cards_html += card
        
    html = html.replace('<!-- DETAIL_CARDS_PLACEHOLDER -->', cards_html)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated HTML at {output_path}")

def main():
    with open(INPUT_MD, 'r', encoding='utf-8') as f:
        content = f.read()
        
    data = parse_markdown(content)
    generate_html(data, TEMPLATE_HTML, OUTPUT_HTML)
    
    # Copy CSS
    shutil.copy(STYLE_CSS_SRC, STYLE_CSS_DEST)
    print(f"Copied CSS to {STYLE_CSS_DEST}")

if __name__ == "__main__":
    main()

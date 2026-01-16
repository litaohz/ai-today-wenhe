import re
import sys
import os
import markdown

def generate_html(md_file_path, output_html_path, assets_dir):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # --- Configuration & Assets ---
    logo_path = os.path.join(assets_dir, "小禾说AI logo.png")
    qr_gzh = os.path.join(assets_dir, "【小禾说AI】公众号二维码.jpg")
    qr_sph = os.path.join(assets_dir, "【清华小禾说AI】视频号二维码.jpg")

    # --- Parsing ---
    
    # 1. Extract Title (First H1)
    title_match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else "硅谷AI圈动态"
    
    # 2. Extract Table
    table_match = re.search(r'(\|.+?\|\n\|[-:|]+\|\n(?:\|.+?\|\n)+)', md_content, re.DOTALL)
    table_md = table_match.group(1) if table_match else ""
    table_html = markdown.markdown(table_md, extensions=['tables'])

    # 3. Extract Sections (### ...)
    sections = []
    section_pattern = re.compile(r'^###\s+(.+?)\n(.*?)(?=^###|\Z)', re.MULTILINE | re.DOTALL)
    
    # Icon Mapping (Minimalist "3D" feel using Emojis/Unicode)
    icon_map = {
        "xAI": "🚀",
        "Grok": "🌌",
        "Google": "🧠",
        "DeepMind": "🧬",
        "OpenAI": "🔮",
        "ChatGPT": "💬",
        "Anthropic": "🌿",
        "Claude": "📜",
        "NVIDIA": "🔋",
        "Meta": "♾️",
        "Llama": "🦙",
        "Agent": "🤖",
        "LangChain": "🔗",
        "Apple": "🍎",
        "Microsoft": "💻",
    }

    def get_icon(text):
        for key, icon in icon_map.items():
            if key.lower() in text.lower():
                return icon
        return "✨" # Default sparkle

    for match in section_pattern.finditer(md_content):
        sec_title = match.group(1).strip()
        sec_body_md = match.group(2).strip()
        
        # Determine strict ID
        num_match = re.match(r'^(\d+)\.', sec_title)
        sec_id = f"section-{num_match.group(1)}" if num_match else f"section-{len(sections)+1}"
        
        # Clean title for display (remove numbering if desired, or keep it)
        display_title = sec_title
        
        # Find icon
        icon = get_icon(sec_title)

        sec_body_html = markdown.markdown(sec_body_md)
        sections.append({
            'id': sec_id,
            'title': display_title,
            'icon': icon,
            'body': sec_body_html
        })

    # --- HTML Template Construction ---
    
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

        :root {
            --bg-gradient: linear-gradient(135deg, #120424 0%, #290a4d 50%, #4a148c 100%);
            --glass-bg: rgba(255, 255, 255, 0.08);
            --glass-border: rgba(255, 255, 255, 0.15);
            --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            
            --text-primary: #f0e6fc; /* Lavender mist */
            --text-secondary: #b39ddb; /* Deep lavender */
            --accent-glow: #d500f9; /* Neon Purple */
            --accent-soft: #9c27b0;
            
            --font-main: 'Outfit', 'Noto Sans SC', sans-serif;
            --radius-lg: 24px;
            --radius-md: 16px;
        }

        body {
            background: var(--bg-gradient);
            background-attachment: fixed; /* Fluid feel */
            font-family: var(--font-main);
            color: var(--text-primary);
            margin: 0;
            padding: 40px 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            line-height: 1.6;
        }

        .container {
            max-width: 800px;
            width: 100%;
            position: relative;
        }

        /* Decorative Background Orbs */
        .orb {
            position: fixed;
            border-radius: 50%;
            filter: blur(80px);
            z-index: -1;
            opacity: 0.5;
        }
        .orb-1 { top: -100px; left: -100px; width: 400px; height: 400px; background: #6200ea; }
        .orb-2 { bottom: -100px; right: -100px; width: 500px; height: 500px; background: #aa00ff; }

        /* Glassmorphism Card Utils */
        .glass-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            box-shadow: var(--glass-shadow);
            padding: 30px;
            margin-bottom: 30px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .glass-panel:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(124, 77, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.3);
        }

        /* Typography & Glow */
        h1, h2, h3 {
            font-weight: 700;
            margin-top: 0;
            letter-spacing: -0.02em;
        }

        h1.main-title {
            font-size: 2.8em;
            background: linear-gradient(to right, #ffffff, #e1bee7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(225, 190, 231, 0.3);
            margin-bottom: 0.2em;
        }

        .subtitle {
            font-size: 1.1em;
            color: var(--text-secondary);
            font-weight: 400;
            margin-bottom: 20px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
        
        /* Elite Identity Badge */
        .elite-badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: rgba(0,0,0,0.2);
            padding: 8px 16px;
            border-radius: 50px;
            border: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 20px;
        }
        .elite-badge span {
            font-size: 0.85em;
            color: #d1c4e9;
            font-weight: 600;
        }
        .university-icon {
            font-size: 1.2em;
        }

        /* Header Layout */
        .header-card {
            text-align: center;
            position: relative;
            overflow: hidden;
            border-top: 1px solid rgba(255,255,255,0.2);
        }
        .header-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 4px;
            background: linear-gradient(90deg, #7c4dff, #d500f9, #7c4dff);
            box-shadow: 0 0 10px #d500f9;
        }

        /* Overview Table */
        table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0 8px; /* Spacing between rows */
            margin-top: 10px;
        }
        th {
            color: var(--text-secondary);
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0 15px 10px 15px;
            text-align: left;
        }
        td {
            background: rgba(255, 255, 255, 0.03);
            padding: 15px;
            vertical-align: middle;
        }
        td:first-child {
            border-top-left-radius: 12px;
            border-bottom-left-radius: 12px;
            color: #fff;
            font-weight: 600;
            width: 30%;
        }
        td:last-child {
            border-top-right-radius: 12px;
            border-bottom-right-radius: 12px;
            color: var(--text-secondary);
        }
        tr:hover td {
            background: rgba(255, 255, 255, 0.08);
        }

        /* Section Cards */
        .section-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            padding-bottom: 15px;
        }
        .section-icon {
            font-size: 2.5em;
            filter: drop-shadow(0 0 10px rgba(213, 0, 249, 0.4));
            animation: float 6s ease-in-out infinite;
        }
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-6px); }
            100% { transform: translateY(0px); }
        }
        .section-card h3 {
            font-size: 1.5em;
            margin: 0;
            color: #fff;
        }
        
        .section-content {
            color: var(--text-secondary);
            font-weight: 300;
        }
        .section-content strong {
            color: #e1bee7;
            font-weight: 600;
        }
        .section-content li {
            margin-bottom: 10px;
        }
        .section-content a {
            color: #d1c4e9; /* Light purple links */
            text-decoration: none;
            border-bottom: 1px dotted #d1c4e9;
        }

        /* Footer / Author Block */
        .footer-identity {
            margin-top: 40px;
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.9em;
            border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 30px;
            width: 100%;
        }
        .slogan {
            font-style: italic;
            opacity: 0.8;
            margin-bottom: 30px;
        }

        .author-card-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        .author-card {
            background: rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 15px 25px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
        }
        .author-card:hover {
            background: rgba(255,255,255,0.05);
            border-color: var(--accent-soft);
        }
        .author-logo {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: 2px solid var(--accent-glow);
            object-fit: cover;
        }
        .author-qr {
            width: 80px;
            height: 80px;
            border-radius: 8px;
            opacity: 0.9;
        }
        .author-info {
            text-align: left;
        }
        .author-name {
            display: block;
            font-weight: 700;
            color: #fff;
            margin-bottom: 4px;
        }
        .author-desc {
            font-size: 0.8em;
            color: var(--text-secondary);
        }

        /* Screenshot Helper */
        .screenshot-target {
            /* No specific changes needed, just layout */
        }
    </style>
    """

    html_parts = []
    html_parts.append(f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        {css}
    </head>
    <body>
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
    
        <div class="container">
            
            <div id="screenshot-header" class="screenshot-target">
                <!-- Header Card -->
                <div class="glass-panel header-card">
                    <div class="elite-badge">
                         <span class="university-icon">🏛️</span>
                         <span>THU & WHU Alumni AI Research</span>
                    </div>
                    
                    <h1 class="main-title">{title}</h1>
                    <div class="subtitle">硅谷 AI 前沿动态日报</div>
                    
                     <div class="overview-section">
                        {table_html}
                    </div>
                </div>
            </div>

            <!-- Detail Sections -->
            """)
            
    for sec in sections:
        html_parts.append(f"""
            <div id="{sec['id']}" class="glass-panel section-card screenshot-target">
                <div class="section-header">
                    <div class="section-icon">{sec['icon']}</div>
                    <h3>{sec['title']}</h3>
                </div>
                <div class="section-content">
                    {sec['body']}
                </div>
            </div>
        """)

    # Footer
    html_parts.append(f"""
            <div id="screenshot-footer" class="screenshot-target footer-identity">
                <div class="slogan">“由一名深耕 AI 领域的 THU & WHU 研究员主理，探索有温度的科技审美”</div>
                
                <div class="author-card-container">
                    <!-- GZH -->
                    <div class="author-card">
                        <img src="file:///{logo_path.replace(os.sep, '/')}" class="author-logo">
                        <div class="author-info">
                            <span class="author-name">小禾说AI</span>
                            <span class="author-desc">公众号</span>
                        </div>
                        <img src="file:///{qr_gzh.replace(os.sep, '/')}" class="author-qr">
                    </div>
                    
                    <!-- Video Account -->
                    <div class="author-card">
                         <img src="file:///{logo_path.replace(os.sep, '/')}" class="author-logo">
                        <div class="author-info">
                            <span class="author-name">清华小禾说AI</span>
                            <span class="author-desc">视频号</span>
                        </div>
                        <img src="file:///{qr_sph.replace(os.sep, '/')}" class="author-qr">
                    </div>
                </div>
            </div>
            
        </div> <!-- End Container -->
    </body>
    </html>
    """)

    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write("".join(html_parts))

    print(f"HTML generated at: {output_html_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        # Default behavior for manual testing or simplified calling
        # If args not provided, try to find the latest md file in current or archive dirs?
        # For now, stick to required args to be safe, or allow defaults.
        print("Usage: python md_to_html.py <input_md> <output_html> <assets_dir>")
        sys.exit(1)
    
    input_md = sys.argv[1]
    output_html = sys.argv[2]
    assets_dir = sys.argv[3]
    
    generate_html(input_md, output_html, assets_dir)

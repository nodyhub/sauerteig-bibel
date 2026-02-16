import re
import os
from datetime import datetime
import markdown

SOURCE_FILE = 'content_dump.txt'
OUTPUT_HTML = 'sauerteig_bibel.html'

# Reihenfolge der Dateien im Buch
ORDER = [
    '_index.md', 'sauerteig/_index.md', 'basis-ablauf.md', 
    'rezepte/_index.md', 'rezepte/landbrot.md', 'rezepte/graubrot.md', 
    'rezepte/vollkorn.md', 'rezepte/hanseat.md', 'rezepte/dinkel-seele.md', 
    'rezepte/dinkel-saftkorn.md', 'rezepte/reformer.md', 
    'rezepte/no-knead.md', 'rezepte/pizza-hybrid.md', 'rezepte/pancakes.md', 
    'rezepte/cracker.md', 'rezepte/schokokuchen.md', 'rezepte/zitronenkuchen.md', 
    'rezepte/apfelkuchen.md', 
    'wissen/_index.md', 'wissen/grundlagen.md', 'wissen/teigbearbeitung.md', 
    'wissen/werkzeuge.md', 'wissen/backmethoden.md', 'wissen/baby-spezial.md', 
    'impressum.md'
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Montserrat:wght@400;700&display=swap');
        
        :root {{ 
            --main-color: #5D4037; 
            --accent-color: #8D6E63;
        }}

        * {{ box-sizing: border-box; }}
        body {{ 
            font-family: 'Libre Baskerville', serif; 
            line-height: 1.7; 
            color: #2c2c2c; 
            margin: 0; 
            background: white; 
        }}
        
        /* Cover Page */
        .cover {{ 
            height: 100vh; 
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
            align-items: center; 
            background-color: var(--main-color); 
            color: #f3e5f5; 
            text-align: center;
            padding: 2rem;
            page-break-after: always;
            -webkit-print-color-adjust: exact;
        }}
        .cover h1 {{ 
            font-size: 4rem; 
            margin: 0; 
            line-height: 1.1;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .cover .divider {{
            width: 150px;
            height: 3px;
            background: white;
            margin: 2.5rem 0;
        }}
        .cover p {{ font-family: 'Montserrat', sans-serif; font-size: 1.2rem; margin: 0.5rem 0; text-transform: uppercase; letter-spacing: 3px; }}

        /* Inhaltsverzeichnis */
        .toc-page {{ page-break-after: always; padding: 2.5cm; }}
        .toc-page h2 {{ border: none; padding: 0; margin-bottom: 2rem; }}
        .toc-list {{ list-style: none; padding: 0; font-family: 'Montserrat', sans-serif; }}
        .toc-item {{ margin-bottom: 0.5rem; display: flex; justify-content: space-between; border-bottom: 1px dotted #ccc; }}
        .toc-item a {{ text-decoration: none; color: inherit; }}

        /* Main Layout */
        .content {{ padding: 2.5cm; max-width: 21cm; margin: auto; }}
        
        h1 {{ 
            font-size: 2.5rem; 
            color: var(--main-color); 
            margin-top: 4rem; 
            border-bottom: 2px solid var(--main-color);
            padding-bottom: 0.5rem;
            page-break-before: always; 
        }}
        
        h2 {{ font-size: 1.8rem; color: var(--accent-color); margin-top: 2.5rem; border-left: 5px solid var(--main-color); padding-left: 1rem; }}
        
        table {{ 
            width: 100%; 
            border-collapse: collapse; 
            margin: 2rem 0; 
            font-family: 'Montserrat', sans-serif;
            font-size: 0.85rem;
        }}
        th {{ background-color: var(--main-color); color: white; text-transform: uppercase; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #eee; }}
        tr:nth-child(even) {{ background-color: #f9f6f5; }}
        
        blockquote {{ 
            border-left: 8px solid var(--accent-color); 
            margin: 2rem 0; 
            padding: 1rem 1.5rem; 
            background: #fdf8f7; 
            font-style: italic;
        }}

        @page {{ size: A4; margin: 0; }}
    </style>
</head>
<body>
    <div class="cover">
        <p>Jan Harrie präsentiert</p>
        <div class="divider"></div>
        <h1>Die Hamburger<br>Sauerteig-Bibel</h1>
        <div class="divider"></div>
        <p>Version {version} &middot; {date}</p>
    </div>

    <div class="toc-page">
        <h2>Inhalt</h2>
        <ul class="toc-list">{toc_html}</ul>
    </div>

    <div class="content">
        {main_content}
    </div>
</body>
</html>
"""

def build_book():
    if not os.path.exists(SOURCE_FILE):
        return

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        raw_data = f.read()

    version_match = re.search(r'Version (\d+\.\d+)', raw_data)
    version = version_match.group(1) if version_match else "1.0"
    
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as gh_out:
            gh_out.write(f"VERSION={version}\n")

    files = {}
    parts = re.split(r'===== START FILE: (.*?) =====\n', raw_data)
    for i in range(1, len(parts), 2):
        files[parts[i].strip()] = parts[i+1]

    md_engine = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'])
    
    combined_md = ""
    toc_entries = []

    for filename in ORDER:
        if filename in files:
            content = re.sub(r'^---\n(.*?)\n---\n', '', files[filename], flags=re.DOTALL)
            # Titel für TOC extrahieren (Erste Zeile mit #)
            title_match = re.search(r'^# (.*)', content, re.MULTILINE)
            if title_match:
                toc_entries.append(title_match.group(1))
            combined_md += "\n\n" + content

    main_content_html = md_engine.convert(combined_md)
    toc_html = "".join([f"<li class='toc-item'>{entry}</li>" for entry in toc_entries])
    
    final_html = HTML_TEMPLATE.format(
        version=version, 
        date=datetime.now().strftime("%d.%m.%Y"),
        toc_html=toc_html,
        main_content=main_content_html
    )

    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == "__main__":
    build_book()
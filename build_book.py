import re
import os
from datetime import datetime

SOURCE_FILE = 'content_dump.txt'
OUTPUT_HTML = 'sauerteig_bibel.html'

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
        @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=Inter:wght@400;700&display=swap');
        
        :root {{ --main-color: #5D4037; --bg-color: #fdfaf7; }}
        body {{ font-family: 'Inter', sans-serif; line-height: 1.6; color: #333; margin: 0; background: var(--bg-color); }}
        
        /* Cover Page */
        .cover {{ 
            height: 100vh; display: flex; flex-direction: column; justify-content: center; 
            align-items: center; background: var(--main-color); color: white; text-align: center;
            page-break-after: always;
        }}
        .cover h1 {{ font-family: 'Libre+Baskerville', serif; font-size: 4rem; margin: 0; }}
        .cover p {{ font-size: 1.5rem; opacity: 0.8; }}

        /* Typography */
        .content {{ padding: 2cm; max-width: 21cm; margin: auto; }}
        h1, h2, h3 {{ font-family: 'Libre+Baskerville', serif; color: var(--main-color); page-break-after: avoid; }}
        h1 {{ border-bottom: 2px solid var(--main-color); padding-bottom: 0.5rem; margin-top: 3rem; }}
        h2 {{ margin-top: 2rem; }}
        
        /* Page Breaks & Printing */
        .page-break {{ page-break-before: always; }}
        table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #eee; }}
        blockquote {{ border-left: 5px solid var(--main-color); margin: 1.5rem 0; padding: 0.5rem 1rem; background: #f9f2f0; font-style: italic; }}
        img {{ max-width: 100%; height: auto; }}
        
        @media print {{
            body {{ background: white; }}
            .content {{ padding: 0; }}
        }}
    </style>
</head>
<body>
    <div class="cover">
        <h1>Die Hamburger Sauerteig-Bibel</h1>
        <p>Version {version}</p>
        <p>{date}</p>
        <p>Jan Harrie</p>
    </div>
    <div class="content">
        {main_content}
    </div>
</body>
</html>
"""

def build_html():
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        raw_data = f.read()

    # Version finden
    version_match = re.search(r'Version (\d+\.\d+)', raw_data)
    version = version_match.group(1) if version_match else "1.0"
    
    # GitHub Output
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as gh_out:
            gh_out.write(f"VERSION={version}\n")

    files = {}
    parts = re.split(r'===== START FILE: (.*?) =====\n', raw_data)
    for i in range(1, len(parts), 2):
        files[parts[i].strip()] = parts[i+1]

    # Markdown zu einfachem HTML (sehr basic Ersatz für Pandoc im Script)
    import markdown
    md = markdown.Markdown(extensions=['tables', 'fenced_code'])
    
    combined_md = ""
    for filename in ORDER:
        if filename in files:
            content = re.sub(r'^---\n(.*?)\n---\n', '', files[filename], flags=re.DOTALL)
            combined_md += f"\n\n<div class='page-break'></div>\n\n" + content

    html_content = md.convert(combined_md)
    
    final_html = HTML_TEMPLATE.format(
        version=version, 
        date=datetime.now().strftime("%d.%m.%Y"),
        main_content=html_content
    )

    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(final_html)

if __name__ == "__main__":
    build_html()
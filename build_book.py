import os
import re
import markdown

# 1. Die logische Reihenfolge exakt nach der Struktur deiner Markdown-Dateien
ORDER = [
    "_index.md",
    "wissen/philosophie.md",
    "sauerteig/_index.md",
    "technik/_index.md",
    "technik/standard.md",
    "technik/lazy.md",
    "rezepte/_index.md",
    "rezepte/anfaenger.md",
    "rezepte/anfaenger-mix.md",
    "rezepte/landbrot.md",
    "rezepte/graubrot.md",
    "rezepte/vollkorn.md",
    "rezepte/hanseat.md",
    "rezepte/dinkel-seele.md",
    "rezepte/dinkel-saftkorn.md",
    "rezepte/kartoffel-walnuss.md",
    "rezepte/reformer.md",
    "rezepte/no-knead.md",
    "rezepte/ciabatta-style.md",
    "rezepte/zupfbrot.md",
    "rezepte/pizza-hybrid.md",
    "rezepte/hanse-brioche.md",
    "rezepte/pancakes.md",
    "rezepte/cracker.md",
    "rezepte/schoko-cracker.md",
    "rezepte/zitronenkuchen.md",
    "rezepte/apfelkuchen.md",
    "rezepte/schokokuchen.md",
    "wissen/_index.md",
    "wissen/teigbearbeitung.md",
    "wissen/grundlagen.md",
    "wissen/werkzeuge.md",
    "wissen/backmethoden.md",
    "wissen/optik-finish.md",
    "wissen/baby-spezial.md",
    "wissen/empfehlungen.md",
    "wissen/erste-hilfe.md",
    "wissen/zeitplan.md",
    "impressum.md"
]

# 2. Das Kochbuch-CSS (Echte Buch-Optik für das PDF)
CSS = """
<style>
    /* Basis-Buch-Design (Serifen für den Fließtext!) */
    body { 
        font-family: 'Georgia', 'Times New Roman', serif; 
        font-size: 10pt; /* Echte Buchgröße, nicht mehr riesig */
        line-height: 1.5; 
        color: #111; 
        text-align: justify; /* Blocksatz für den Buch-Look */
        hyphens: auto; /* Automatische Silbentrennung */
    }
    
    /* Überschriften modern und sans-serif als knackiger Kontrast */
    h1, h2, h3 { 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
        font-weight: bold;
        color: #2c3e50;
    }
    
    h1 { 
        font-size: 16pt; 
        border-bottom: 2px solid #b35900; 
        padding-bottom: 5px; 
        margin-top: 0;
        page-break-before: always; /* Jedes Rezept/Kapitel startet auf einer neuen Seite */
    }
    
    h2 { 
        font-size: 13pt; 
        color: #b35900; 
        margin-top: 2em;
        margin-bottom: 0.5em;
        page-break-after: avoid; /* Keine Überschrift ganz unten auf der Seite! */
    }
    
    h3 { 
        font-size: 11pt; 
        page-break-after: avoid;
    }

    /* Cleane, platzsparende Zutaten-Tabellen */
    table { 
        border-collapse: collapse; 
        width: 100%; 
        margin-top: 15px;
        margin-bottom: 20px; 
        font-size: 9.5pt; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; /* Tabellen der Lesbarkeit halber serifenlos */
    }
    th, td { 
        border: none;
        border-bottom: 1px solid #ecf0f1; 
        padding: 6px 8px; 
        text-align: left; 
    }
    th { 
        font-weight: bold;
        color: #7f8c8d;
        text-transform: uppercase;
        font-size: 8pt;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #bdc3c7;
    }
    td:first-child { 
        font-weight: bold; 
        color: #2c3e50; 
    }

    /* Zitate und Tipps */
    blockquote { 
        border-left: 3px solid #b35900; 
        margin: 1.5em 0; 
        padding: 8px 15px; 
        font-style: italic; 
        background-color: #fdfbf7; 
        font-size: 9.5pt;
    }

    ol, ul { 
        padding-left: 20px; 
        margin-bottom: 15px; 
    }
    li { 
        margin-bottom: 6px; 
    }

    /* Halbierte Seitenränder für mehr Platz (A4) */
    @page {
        size: A4;
        /* Ränder: Oben 12.5mm, Rechts 10mm, Unten 12.5mm, Links 12.5mm */
        margin: 12.5mm 10mm 12.5mm 12.5mm; 
    }
    
    @media print {
        body { background: transparent; }
        /* Bilder (falls du mal welche einbaust) nicht zerschneiden */
        img, table, tr, td, li, blockquote { page-break-inside: avoid; }
        a { text-decoration: none; color: inherit; }
    }
</style>
"""

def build():
    # 1. Den content_dump.txt einlesen und zerteilen
    dump_file = 'content_dump.txt'
    if not os.path.exists(dump_file):
        print(f"Fehler: {dump_file} nicht gefunden!")
        return

    with open(dump_file, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    # Dictionary bauen { "dateiname.md" : "Inhalt..." }
    files_data = {}
    parts = raw_text.split('===== START FILE: ')
    for part in parts:
        if not part.strip():
            continue
        lines = part.split('\n', 1)
        if len(lines) >= 2:
            filename = lines[0].strip().replace('=====', '').strip()
            content = lines[1]
            files_data[filename] = content

    combined_md = ""
    version = "1.0" # Fallback

    # 2. Dateien in der richtigen Reihenfolge zusammenbauen
    for file_path in ORDER:
        if file_path not in files_data:
            print(f"WARNUNG: {file_path} fehlt im Dump!")
            continue
            
        content = files_data[file_path]
        
        # Version aus _index.md auslesen (sucht nach "Version X.Y")
        if file_path == "_index.md":
            match = re.search(r'Version (\d+\.\d+)', content)
            if match:
                version = match.group(1)
                print(f"Gefundene Version: {version}")

        # Frontmatter (--- ... ---) entfernen
        content = re.sub(r'^---[\s\S]*?^---\n', '', content, flags=re.MULTILINE)
        
        # Inhalt aneinanderreihen (CSS regelt den Seitenumbruch bei h1)
        combined_md += content + "\n\n"

    # 3. HTML generieren
    html_content = markdown.markdown(combined_md, extensions=['tables'])
    
    # 4. Finales HTML-Dokument zusammenbauen
    final_html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Die Hamburger Sauerteig-Bibel</title>
    {CSS}
</head>
<body>
    {html_content}
</body>
</html>
"""

    # 5. Als sauerteig_bibel.html speichern (damit der Workflow es findet)
    with open('sauerteig_bibel.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
        print("Erfolgreich gespeichert: sauerteig_bibel.html")

    # 6. Version an GitHub Actions übergeben (für den Release-Tag)
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as env_file:
            env_file.write(f"VERSION={version}\n")
            print(f"GitHub Output gesetzt: VERSION={version}")

if __name__ == "__main__":
    build()
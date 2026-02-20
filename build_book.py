import os
import re
import markdown

# 1. Die logische Reihenfolge
ORDER = [
    "_index.md",
    "wissen/philosophie.md",
    "sauerteig/_index.md",
    "basis-ablauf.md",
    "rezepte/_index.md",
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
    "impressum.md"
]

# 2. Das CSS (inkl. @page Margins für Playwright!)
# 2. Das Kochbuch-CSS (Kompakt & Edel)
CSS = """
<style>
    /* Basis-Schriftart: Kompakter für den Druck */
    body { 
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; 
        font-size: 11pt; 
        line-height: 1.4; 
        color: #2c3e50; 
    }
    
    /* Kochbuch-Optik: Edle Überschriften (Serifen) */
    h1, h2, h3 { 
        font-family: Georgia, "Times New Roman", serif; 
        font-weight: normal;
        color: #1a252f;
        margin-top: 1.2em;
        margin-bottom: 0.4em;
    }
    
    h1 { 
        font-size: 18pt; 
        border-bottom: 1px solid #eee; 
        padding-bottom: 5px; 
    }
    
    /* Eine dezente "Rost/Krusten"-Farbe für die Zwischenüberschriften */
    h2 { 
        font-size: 14pt; 
        color: #b35900; 
    }
    h3 { 
        font-size: 12pt; 
    }

    /* Kursiver Text (die kleinen Einleitungen) etwas dezenter */
    em { 
        color: #555; 
        font-size: 10.5pt; 
    }

    /* Cleane, platzsparende Zutaten-Tabellen */
    table { 
        border-collapse: collapse; 
        width: 100%; 
        margin-top: 10px;
        margin-bottom: 15px; 
        font-size: 10pt; /* Tabellen-Text noch einen Tick kleiner */
    }
    th, td { 
        border: none;
        border-bottom: 1px solid #ecf0f1; 
        padding: 5px 8px; /* Weniger Padding = mehr Platz */
        text-align: left; 
    }
    th { 
        background-color: transparent; 
        font-weight: bold;
        color: #7f8c8d;
        text-transform: uppercase;
        font-size: 8.5pt;
        letter-spacing: 0.5px;
        border-bottom: 2px solid #bdc3c7;
    }
    /* Die erste Spalte (Zutaten-Namen) leicht hervorheben */
    td:first-child { 
        font-weight: bold; 
        color: #2c3e50; 
    }

    /* Wichtige Tipps und Zitate (Blockquotes) */
    blockquote { 
        border-left: 3px solid #b35900; 
        margin: 1.2em 0; 
        padding: 6px 12px; 
        font-style: italic; 
        background-color: #fdfbf7; /* Sehr sanfter Papierton */
        font-size: 10pt;
    }

    /* Kompaktere Listen für den Ablauf */
    ol, ul { 
        padding-left: 20px; 
        margin-bottom: 15px; 
    }
    li { 
        margin-bottom: 4px; /* Spart extrem viel Platz in der Höhe */
    }

    /* Druck-Einstellungen für Playwright */
    @page {
        margin: 15mm 20mm; /* Etwas weniger Rand oben/unten gibt dem Rezept mehr Platz */
    }
    
    @media print {
        body { background: transparent; }
        
        /* Regel 1: Jedes Rezept fängt auf einer NEUEN Seite an */
        h1 { page-break-before: always; margin-top: 0; }
        
        /* Schutz davor, dass Dinge am Seitenende zerschnitten werden */
        h1, h2, h3 { page-break-after: avoid; }
        table, tr, td, li, blockquote { page-break-inside: avoid; }
        
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
        
        # Inhalt + Manueller Seitenumbruch
        combined_md += content + "\n\n<div style='page-break-after: always;'></div>\n\n"

    # 3. HTML generieren
    html_content = markdown.markdown(combined_md, extensions=['tables'])
    
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

    # 4. Als sauerteig_bibel.html speichern (damit der Workflow es findet)
    with open('sauerteig_bibel.html', 'w', encoding='utf-8') as f:
        f.write(final_html)
        print("Erfolgreich gespeichert: sauerteig_bibel.html")

    # 5. Version an GitHub Actions übergeben (für den Release-Tag)
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as env_file:
            env_file.write(f"VERSION={version}\n")
            print(f"GitHub Output gesetzt: VERSION={version}")

if __name__ == "__main__":
    build()
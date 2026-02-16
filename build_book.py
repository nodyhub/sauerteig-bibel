import re
import os
import sys
from datetime import datetime

SOURCE_FILE = 'content_dump.txt'
OUTPUT_FILE = 'sauerteig_book.md'

# Farben & Style (Brot-Theme)
# primary: Ein warmes Dunkelgrau für Texte
# accent: Ein schönes "Krusten-Orange/Braun" für Überschriften/Cover
# Farben & Style (Brot-Theme)
HEADER_TEMPLATE = """---
title: "Die Hamburger Sauerteig-Bibel"
author: "Jan Harrie"
date: "Version {version} ({date})"
lang: "de"
titlepage: true
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "FFFFFF"
titlepage-rule-height: 2
titlepage-background: "#5D4037"
toc: true
toc-own-page: true
book: true
classoption: [oneside]
---
"""

# Info: titlepage-background: "5D4037" ist ein schönes Altrosa/Braun. 
# Du kannst auch "8B4513" (SaddleBrown) nehmen.

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

def clean_content(text):
    # Entfernt Hugo Frontmatter und repariert Bildpfade falls nötig
    text = re.sub(r'^---\n(.*?)\n---\n', '', text, flags=re.DOTALL)
    # Entfernt Hugo Shortcodes falls vorhanden, z.B. {{< ... >}}
    text = re.sub(r'\{\{<.*?>\}\}', '', text)
    return text.strip()

def build_book():
    if not os.path.exists(SOURCE_FILE):
        print(f"Error: {SOURCE_FILE} not found.")
        return

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        raw_data = f.read()

    # Version finden
    version_match = re.search(r'Version (\d+\.\d+)', raw_data)
    version = version_match.group(1) if version_match else "1.0"
    current_date = datetime.now().strftime("%d.%m.%Y")
    
    # Output für GitHub Actions setzen
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as gh_out:
            gh_out.write(f"VERSION={version}\n")
    
    print(f"Building PDF Source for Version: {version}")

    files = {}
    parts = re.split(r'===== START FILE: (.*?) =====\n', raw_data)
    for i in range(1, len(parts), 2):
        files[parts[i].strip()] = parts[i+1]

    # Header zuerst schreiben
    full_book = HEADER_TEMPLATE.format(version=version, date=current_date)

    for filename in ORDER:
        if filename in files:
            content = clean_content(files[filename])
            # Seitenumbruch einfügen (Pandoc/LaTeX command)
            full_book += f"\n\n\\newpage\n\n{content}"

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_book)

if __name__ == "__main__":
    build_book()
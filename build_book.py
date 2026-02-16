import re
import os
import sys

SOURCE_FILE = 'content_dump.txt'
OUTPUT_FILE = 'sauerteig_book.md'

# Die Reihenfolge im Buch
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
    # Entfernt Hugo Frontmatter
    text = re.sub(r'^---\n(.*?)\n---\n', '', text, flags=re.DOTALL)
    return text.strip()

def build_book():
    if not os.path.exists(SOURCE_FILE):
        print(f"Error: {SOURCE_FILE} not found.")
        return

    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        raw_data = f.read()

    # 1. Version extrahieren (sucht nach "Version X.X")
    version_match = re.search(r'Version (\d+\.\d+)', raw_data)
    version = version_match.group(1) if version_match else "1.0"
    
    # Version für GitHub Actions bereitstellen
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as gh_out:
            gh_out.write(f"VERSION={version}\n")
    
    print(f"Detected Version: {version}")

    # 2. Buch bauen
    files = {}
    parts = re.split(r'===== START FILE: (.*?) =====\n', raw_data)
    for i in range(1, len(parts), 2):
        files[parts[i].strip()] = parts[i+1]

    full_book = ""
    for filename in ORDER:
        if filename in files:
            content = clean_content(files[filename])
            full_book += f"{content}\n\n\\newpage\n\n"

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_book)

if __name__ == "__main__":
    build_book()
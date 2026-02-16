import os
import re
import shutil

# --- KONFIGURATION ---
SOURCE_FILE = 'content_dump.txt'  # Name deiner Textdatei mit dem Inhalt
TARGET_DIR = 'content'            # Zielordner für Hugo
CLEAN_TARGET = True               # True = Löscht den Ordner vorher (Empfohlen)
# ---------------------

def split_files():
    # 1. Prüfen, ob Quelldatei existiert
    if not os.path.exists(SOURCE_FILE):
        print(f"❌ FEHLER: Datei '{SOURCE_FILE}' nicht gefunden.")
        print("   Bitte speichere den gesamten Textblock in diese Datei.")
        return

    # 2. Zielordner bereinigen (Optional)
    if CLEAN_TARGET and os.path.exists(TARGET_DIR):
        print(f"🧹 Lösche alten Ordner: {TARGET_DIR}/ ...")
        shutil.rmtree(TARGET_DIR)
    
    # Zielordner neu erstellen, falls nicht da
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)

    # 3. Datei einlesen
    print(f"📖 Lese {SOURCE_FILE} ...")
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 4. Regex Split
    # Sucht nach: ===== START FILE: pfad/datei.md =====
    pattern = re.compile(r'===== START FILE: (.*?) =====\n')
    parts = pattern.split(content)

    # Der erste Teil vor dem ersten Marker ist meist leer oder Müll
    if len(parts) > 0 and parts[0].strip() == "":
        parts = parts[1:]

    count = 0

    # 5. Dateien schreiben
    # Die Liste 'parts' ist jetzt immer abwechselnd: [Dateiname, Inhalt, Dateiname, Inhalt...]
    for i in range(0, len(parts), 2):
        if i+1 >= len(parts): 
            break # Sicherheitscheck
            
        rel_path = parts[i].strip()   # z.B. "rezepte/landbrot.md"
        file_content = parts[i+1].strip()
        
        # Falls im Pfad schon "content/" steht, entfernen wir es, um Dopplung zu vermeiden
        if rel_path.startswith("content/"):
            rel_path = rel_path.replace("content/", "", 1)
            
        # Vollen Pfad bauen: content/rezepte/landbrot.md
        full_path = os.path.join(TARGET_DIR, rel_path)
        
        # Unterordner erstellen (z.B. content/rezepte/)
        directory = os.path.dirname(full_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Schreiben
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(file_content + '\n')
        
        print(f"✅ Erstellt: {full_path}")
        count += 1

    print(f"\n🎉 Fertig! {count} Dateien wurden in '{TARGET_DIR}/' erstellt.")

if __name__ == "__main__":
    split_files()
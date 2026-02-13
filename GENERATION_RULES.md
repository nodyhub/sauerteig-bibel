# 📋 Content Generation Rules für Sauerteig-Bibel

Diese Datei dokumentiert die Regeln und Standards, nach denen neuer Content für diese Hugo-Website generiert wird.

## Grundprinzipien

### 1. **Dateistruktur & Organisation**
- **Hauptseiten:** `content/*.md` (auf Root-Level)
- **Unterkapitel:** `content/kapitel/*.md` (Ordnerstruktur)
- **Frontmatter:** Immer `title`, `weight` enthalten
- **Weight:** Bestimmt die Navigationsreihenfolge (aufsteigend)

### 2. **Frontmatter Standard**
```yaml
---
title: Seitentitel
weight: 10  # Sortierposition
---
```

### 3. **Markdown Standards**

#### Überschriftenstruktur
- `#` = Haupttitel (1x pro Seite)
- `##` = Hauptkapitel / Unterseiten
- `###` = Subkapitel / Unterpunkte
- `####` = Details / Erklärungen

#### Formatierung
- **Fett** für Betonung und wichtige Begriffe
- `code` für technische Begriffe/Befehle
- `[Link](../link/)` für interne Links (relative Pfade!)
- `>` für Hinweise/Tipps

#### Listen
- `-` für Bullet Points
- `1.` für nummerierte Listen
- Verschachtelung mit 2er-Einzug

### 4. **Interne Links**
```markdown
[Master-Prozess](../master-prozess/)  # Mit trailing slash
[Sauerteig-Pflege](../methoden/sauerteig-pflege/)  # Unterkapitel
```

### 5. **Spezielle Hugo-Book Shortcodes**

#### Steps (für Prozessschritte)
```markdown
{{< steps >}}

1. ## Erster Schritt

   Beschreibung des Schritts

2. ## Zweiter Schritt

   Weitere Details

{{< /steps >}}
```
**Wichtig:** 
- Nutze den `{{< >}}` Syntax (HTML-ähnlich), nicht `{{% %}}`
- Texte unter den Überschriften MÜSSEN mit 3 Leerzeichen eingerückt sein

#### Hints (für Tipps/Warnungen)
```markdown
> **Tipp:** Dies ist wichtig!
```

### 6. **Sprachstil**
- **Du-Form** durchgehend verwenden
- **Persönliche Anmerkungen:** "Ich backe...", "Meine Erfahrung..."
- **Praktisch & konkret:** Keine theoretischen Ausschweifungen
- **Emoji sparsam einsetzen** (nur in Titeln oder als Liste-Marker)
- **Deutsche Umlaute:** Vollständig ausschreiben (Äpfel, nicht Aepfel)

### 7. **Content-Typen**

#### Rezepte
- Zutaten in Tabelle (Standard/XL)
- Prozent-Angaben (Bäcker*innenprozente)
- Ablauf als nummerierte Liste
- Charakteristik am Ende

#### Anleitungen (wie Master-Prozess)
- **{{% steps %}}** Shortcode für 6-Phasen
- Detaillierte Erklärungen unter jedem Schritt
- Inline-Links zu verwandten Inhalten

#### Methoden/Werkzeuge
- Problem-Lösung Format
- Konkrete Tipps & Tricks
- Optionen mit Pro/Contra auflisten

### 8. **Gewichtung (Weight)**

```
Hauptnavigation (content/):
- philosophie.md        → weight: 10
- master-prozess.md     → weight: 20
- rezepte/              → weight: 30
- baby-spezial.md       → weight: 40
- methoden/             → weight: 50
- impressum.md          → weight: 100

Unterkapitel (z.B. rezepte/):
- landbrot.md           → weight: 10
- graubrot.md           → weight: 20
- vollkorn.md           → weight: 25
- dinkel-saftkorn.md    → weight: 30
- specials/             → weight: 40

Unter-Unterkapitel (z.B. methoden/):
- sauerteig-pflege.md   → weight: 10
- starter-ansetzen.md   → weight: 20
- schnitt-technik.md    → weight: 30
- tipps-tricks.md       → weight: 40
- backmethoden.md       → weight: 50
```

### 9. **Tabellen Standard**
```markdown
| Spalte 1 | Spalte 2 | Spalte 3 |
| :--- | :--- | :--- |
| Linksbündig | Standard | Default |
```

### 10. **Zeitangaben**
- **Vollständig:** "Minuten", "Stunden" (nie "min", "Std")
- **Beispiel:** "45 Minuten", nicht "45 Min"

### 11. **Beispiel-Workflow für neuen Content**

1. **context.md** schreiben mit:
   - Zielseitentitel & Struktur
   - Zielordner
   - Weight & Frontmatter

2. **content.md** oder **template.txt** erstellen mit Plain Text Content

3. **Konvertierung** durch Hugo-Markdown-Generierung:
   - Frontmatter hinzufügen
   - Markdown-Formatierung anwenden
   - Links relativieren
   - Shortcodes integrieren

4. **In content-Verzeichnis** kopieren mit korrektem Namen

---

**Zuletzt aktualisiert:** Februar 2026

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

### 8. **Gewichtung (Weight) - Aktualisierte Struktur**

```
Hauptnavigation (content/):
- philosophie.md        → weight: 10
- master-prozess.md     → weight: 20
- rezepte/              → weight: 30
- methoden/             → weight: 50  (Der Sauerteig)
- werkzeuge/            → weight: 60  (Werkzeuge, Tricks & Hacks)
- baby-spezial/         → weight: 70  (Baby-Spezial)
- impressum.md          → weight: 100

Unterkapitel Rezepte (rezepte/):
- landbrot.md           → weight: 10
- graubrot.md           → weight: 20
- vollkorn.md           → weight: 25
- dinkel-saftkorn.md    → weight: 30
- hanseat.md            → weight: 25
- dinkel-seele.md       → weight: 26
- reformer.md           → weight: 27

Unterkapitel Methoden (methoden/):
- ansaetzen-und-pflegen.md  → weight: 10
- schnitt-technik.md        → weight: 20
- tipps-tricks.md           → weight: 30
- backmethoden.md           → weight: 40
``` - Rezepte**

```markdown
| Zutat | Bäckerprozente | Standard (1 Kasten) | XL (Großer Kasten) |
| :--- | :--- | :--- | :--- |
| **Gesamtmehl** | **100 %** | **500 g** | **750 g** |
| *davon Weizen 550* | *54 %* | *270 g* | *400 g* |
| **Wasser** | **68 %** | **340 ml** | **510 ml** |
| **Sauerteig (aktiv)** | **20 %** | **100 g** | **150 g** |
| **Salz**Formatierungsstandards**

- **Zahlenbereiche:** "5 bis 10 Minuten" (nicht "5-10")
- **Temperaturangaben:** "250 °C" (Leerzeichen vor °C)
- **Prozentzeichen:** "1,8 %" (Leerzeichen vor %)
- **Bindestriche bei Adjektiven:** "550er-Weizen", "150er-Form" (Bindestrich, nicht minus)
- **Substantivlisten:** Kleinbuchstaben ("altes Anstellgut", nicht "Altes Anstellgut")
- **Hervorhebung:** `**Text**` für wichtige Wörter/Zahlen
- **Kursiv:** `*Text*` nur für Titel/Anmerkungen, nicht für Betonung
- **Links:** Relative Pfade mit trailing slash: `[Link](../kapitel/)`

### 11. **Überschriftenstruktur - KEINE Nummerierungen**

```markdown
# Haupttitel (nur einmal pro Datei)

## Hauptkapitel
Text...

## Nächstes Kapitel
Text...

### Unterpunkt
Text...
```

**WICHTIG:** 
- KEINE Nummerierungen vor Überschriften (## 1., ## 2. etc.)
- Nur bei Listen werden Nummern verwendet: `1. Punkt`, `2. Punkt`
- Gilt überall im content/ Verzeichnis (methoden/, werkzeuge/, baby-spezial/, etc.)

### 12. **Honig & Baby-Sicherheit**

- **Standard-Süßungsmittel:** Honig (in allen Rezepten)
- **Warnung:** Honig ist für Säuglinge unter 1 Jahr tabu (Botulismus-Risiko)
- **Alternative:** Apfelmark (ungesüßt), Reissirup, Agavendicksaft, Zucker
- **In recipes:** Immer auflisten als "1 EL Honig" in Extras-Zeile

### 13. **Zeitangaben - Standards**

**Wichtig für Rezepte:**
- Spalte 1: "Bäckerprozente" (nicht "%")
- Dezimaltrennzeichen: Komma (1,8 nicht 1.8)
- Einheiten: Leerzeichen vor Einheit (1 EL, nicht 1EL; 100 g, nicht 100g)
- Mengen-Dezimalzeichen: Komma (1,5 EL nicht 1.5 EL)
- Gesamtmehl IMMER zuerst auflisten, dann "davon" Anteile eingerückt
- "Honig" verwenden, nicht "Apfelmark"--- | :--- | :--- |
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

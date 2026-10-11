<p align="center">
  <img src="assets/icon-256.png" width="112" height="112" alt="GR4-GF2Unlock-Symbol: ein GF-2-Blitz, dessen Lichtstrahl in sechs Bändern zu je einer Blendenstufe schwächer wird">
</p>

<h1 align="center">GR4-GF2Unlock</h1>

<p align="center">
  <strong>Der GF-2-Blitzmodus der GR III, auf Ihrer RICOH GR IV.<br>Fokussieren Sie auf Ihr Motiv; die Kamera stellt die Blitzbelichtung ein.</strong>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.ko.md">한국어</a> |
  <strong>Deutsch</strong> |
  <a href="README.fr.md">Français</a> |
  <a href="README.es.md">Español</a>
</p>

Mit Firmware 2.10 hat RICOH der GR III den **GF-2-Blitzmodus** gegeben: Mit dem
aufgesteckten kleinen Blitz RICOH GF-2 löst die Kamera den Blitz mit fester
Leistung aus und ermittelt Blende, ISO und Verschlusszeit aus der
**Fokusentfernung**. Die GR IV hat diesen Modus nie bekommen.

GR4-GF2Unlock fügt ihn der GR IV als **fünfte Option im Blitzmodus** hinzu,
neben Blitz Ein, Blitz Ein+Anti Rote Augen, Langz.-Sync und
Langz.Sync+AntiRoteAug. Alles andere an Ihrer Kamera bleibt genau so, wie es
war, und Sie können jederzeit zur offiziellen Firmware zurückkehren.

Dieses Repository enthält keine RICOH-Firmware. Sie laden die offizielle
Firmware selbst von RICOH herunter, und das enthaltene Werkzeug macht daraus auf
Ihrem eigenen Computer die Version mit GF-2-Blitzmodus.

> [!WARNING]
> **Inoffiziell, auf eigenes Risiko.** Nicht von RICOH IMAGING erstellt oder
> unterstützt. Die Installation veränderter Firmware kann Ihre Garantie
> ungültig machen. Bitte lesen Sie zuerst [Bevor Sie beginnen](#bevor-sie-beginnen)
> und [Risiken](#risiken).

| Sie möchten | Weiter zu |
| --- | --- |
| Sehen, was die Kamera bei jeder Entfernung einstellt | [Was Sie erwarten können](#was-sie-erwarten-können) |
| Die Firmware erstellen (macOS, Windows, Linux) | [Die Firmware erstellen](#die-firmware-erstellen) |
| Sie installieren | [Auf die Kamera bringen](#auf-die-kamera-bringen) |
| Herausfinden, was eine Firmware-Datei enthält | [Firmware-Datei prüfen](#firmware-datei-prüfen) |
| Zur Firmware von RICOH zurückkehren | [Zurück zur offiziellen Firmware](#zurück-zur-offiziellen-firmware) |

**Inhalt:**
[So funktioniert es](#so-funktioniert-es) |
[Was Sie bekommen](#was-sie-bekommen) |
[Bevor Sie beginnen](#bevor-sie-beginnen) |
[Die Firmware erstellen](#die-firmware-erstellen) |
[Auf die Kamera bringen](#auf-die-kamera-bringen) |
[Gut zu wissen](#gut-zu-wissen) |
[Risiken](#risiken) |
[Teststand](#teststand) |
[Für Entwickler](#für-entwickler)

## So funktioniert es

Ist der GF-2-Blitzmodus gewählt, löst die Kamera den GF-2 wie bei Blitz Ein aus,
aber mit **fester Leistung**. Dann plant sie die Belichtung so, wie es der
GF-2-Blitzmodus der GR III tut: aus der Leitzahl des Blitzes und der
**Fokusentfernung** (Autofokus oder manueller Fokus), innerhalb der eigenen
Grenzen der GR IV für Blende, ISO und Blitzsynchronisation.

- **Die Leistung** wird über die **Blitzleistung** eingestellt: **Auto oder 1/1**
  ist volle Leistung, **1/4** ist Viertelleistung.
- **Mit ISO-Automatik** lässt die Kamera die Blende offen und erhöht die ISO, je
  weiter das Motiv entfernt ist.
- **Mit fester ISO** wählt die Kamera die Blende, die zur Entfernung passt.
- **Die Verschlusszeit** richtet sich nach dem Licht um das Motiv herum. Sie
  bleibt innerhalb der Blitzsynchronzeit, sodass der Blitz immer im Bild ist.
  Die längste ist 1/32 s, oder bis zu 32 s mit Langzeitsynchronisation an einem
  dunklen Ort.
- **In Tv, Av und M** werden die von Ihnen eingestellten Werte übergangen, wie
  bei der GR III.

Die Belichtungsberechnung stammt von RICOH selbst, übernommen aus der Firmware
2.10 der GR III. Alles andere ist die offizielle Firmware der GR IV,
unverändert.

### Was Sie erwarten können

Typische Werte in einem schwach beleuchteten Raum, Blitzleistung Auto oder 1/1,
Neutralfilter aus (EXIF kann sie leicht runden):

| Entfernung | ISO-Automatik | Feste ISO 400 |
| ---: | --- | --- |
| 0,5 m | f/4.8, ISO 100 | f/11.8 |
| 1 m | f/2.8, ISO 100 | f/5.9 |
| 2 m | f/2.8, ISO 367 | f/3.0 |
| 3 m | f/2.8, ISO 800 | f/2.8 |
| 5 m | f/2.8, ISO 2263 | f/2.8 (Motiv dunkler: außerhalb der Blitzreichweite) |

Mit Blitzleistung **1/4** liegt die ISO etwa zwei Stufen höher oder die Blende
etwa zwei Stufen weiter offen.

> [!TIP]
> **Prüfen Sie, ob der Modus aktiv ist.** Wählen Sie den GF-2-Blitzmodus, und
> stellen Sie den Modus **M**, **ISO 400** und eine Verschlusszeit von 1/2000 s
> oder länger ein. Fotografieren Sie etwas in etwa 1 m Entfernung, dann etwas in
> etwa 3 m Entfernung. Die Blende ändert sich von selbst, auf etwa f/5.9 und
> f/2.8, ganz gleich, was Sie eingestellt haben.

## Was Sie bekommen

Nach der Installation bietet der **Blitzmodus** (im Menü, am ADJ-Hebel und über
die Fn-Taste) Folgendes an:

| Angezeigt als | Was der Blitz tut |
| --- | --- |
| Blitz Ein | löst bei jeder Aufnahme aus, wie bisher |
| Blitz Ein+Anti Rote Augen | wie bisher |
| Langz.-Sync | wie bisher |
| Langz.Sync+AntiRoteAug. | wie bisher |
| **GF-2-Blitzmodus** | **feste Leistung; Blende, ISO und Verschlusszeit aus der Fokusentfernung** |

- Der neue Eintrag hat in jeder Menüsprache einen eigenen Namen, auf Deutsch zum
  Beispiel „GF-2-Blitzmodus“. Wenn keine Langzeitsynchronisation verfügbar ist,
  stehen Blitz Ein, Blitz Ein+Anti Rote Augen und GF-2-Blitzmodus zur Auswahl.
- Er funktioniert mit **aufgestecktem und eingeschaltetem GF-2**, in **P, Tv, Av
  oder M**. Wird kein GF-2 auf dem Blitzschuh erkannt, funktioniert er wie Blitz
  Ein.
- Die Einstellung bleibt beim Ausschalten der Kamera erhalten, wie jede
  Einstellung des Blitzmodus.
- Der Aufnahmebildschirm zeigt das Symbol für **Blitz Ein**, und die Bilder
  vermerken den Blitz als ausgelöst, wie bei Blitz Ein.
- **Alle anderen Blitzmodi funktionieren genau wie bisher**, einschließlich
  Blitzleistung Auto, 1/1 und 1/4.

### Besser als das Original der GR III

Rund um die Belichtungsberechnung von RICOH nutzt die Version für die GR IV
Hardware, die die GR III nicht hat, und behebt einige Schwachstellen:

| | GR III 2.10 | GR4-GF2Unlock |
| --- | --- | --- |
| Blitzleistung | Nur volle Leistung: Die GR III kann den GF-2 nicht steuern | Volle oder Viertelleistung (Blitzleistung 1/1 oder 1/4), mit jeweils eigens berechneter Belichtung |
| Welcher Blitz | Geht davon aus, dass ein GF-2 auslöst, sobald der Modus eingeschaltet ist | Greift nur, wenn die Kamera einen GF-2 auf dem Blitzschuh erkennt; sonst wie Blitz Ein |
| ISO-Automatik mit eingeschaltetem Neutralfilter | Der Hintergrund wird zwei Stufen zu dunkel | Die Verschlusszeit berücksichtigt den Neutralfilter, sodass der Hintergrund richtig belichtet wird |
| Sehr nahe Motive bei hellem Licht | Kann f/19 verlangen, jenseits von f/16 des Objektivs | Bleibt innerhalb von f/2.8–f/16 |
| Blitzsynchronisation | Kann eine kürzere Verschlusszeit als die Blitzsynchronzeit verlangen | Immer innerhalb der Blitzsynchronzeit, die bei der GR IV von der Blende abhängt |
| Alles andere | Das Einschalten des Modus ersetzt das normale Blitzverhalten | Eine von fünf Auswahlmöglichkeiten im Blitzmodus: Wechseln Sie jederzeit zurück zu Blitz Ein und zur automatischen Blitzleistung der GR IV |

Mehr als 48.000 Kombinationen aus Entfernung, ISO, Neutralfilter, Blitzmodus und
Licht wurden geprüft. Keine davon verlangt eine Blende außerhalb von f/2.8–f/16
oder eine Verschlusszeit, mit der der Blitz nicht synchronisieren kann.

## Bevor Sie beginnen

- **Kamera:** RICOH GR IV (das normale Farbmodell). Andere Modelle werden nicht
  unterstützt.
- **Blitz:** RICOH GF-2. Der Modus ist auf seine feste Leistung ausgelegt. Andere
  Blitzgeräte funktionieren in den anderen Blitzmodi weiterhin wie bisher.
- **Ihre Kamera muss bereits Firmware 1.11 haben.** Prüfen Sie die Version im
  Setup-Menü der Kamera.
  - Ältere Version: Aktualisieren Sie zuerst auf dem üblichen Weg mit der
    offiziellen Datei von RICOH auf 1.11.
  - Neuere Version: **Verwenden Sie dieses Werkzeug nicht.** Es unterstützt nur 1.11.
- **Die offizielle Firmware-Datei.** Laden Sie auf der offiziellen
  GR-IV-Supportseite von RICOH IMAGING die **Firmware-Version 1.11** herunter.
  Entpacken Sie sie bei Bedarf, bis Sie die Datei **`fwdc248b.bin`** haben.
- **Ein voll geladener Akku.** Während eines Firmware-Updates darf der Strom
  niemals ausfallen.
- **Eine SD-Karte**, die Sie formatieren können.
- **Ein Computer mit Python 3.8 oder neuer.** macOS und die meisten
  Linux-Systeme haben es bereits; unter Windows installieren Sie es von
  python.org. Mehr wird nicht benötigt.
- Notieren Sie sich eigene Einstellungen (C1, C2, …), die Sie nicht noch einmal
  einrichten möchten.

## Die Firmware erstellen

Öffnen Sie ein Terminal in diesem Ordner und führen Sie aus (verwenden Sie den
Pfad, unter dem Sie die offizielle Datei gespeichert haben):

```sh
python3 gr4_gf2unlock.py patch ~/Downloads/fwdc248b.bin
```

Unter Windows:

```bat
py gr4_gf2unlock.py patch C:\Users\you\Downloads\fwdc248b.bin
```

Das Werkzeug stellt zuerst sicher, dass Sie ihm die echte offizielle Datei 1.11
gegeben haben. Dann erstellt es die Firmware mit GF-2-Blitzmodus und prüft sie.
Das dauert etwa eine Minute. Wenn alles stimmt, endet es mit:

```
wrote output/fwdc248b.bin  (SHA-256 45a2edd33a0e0783458b1052ad8b67514f48b45a5db7b47013543eb46d247f0c)
```

Wenn etwas nicht stimmt, gibt es `refused: …` aus und schreibt **nichts**: zum
Beispiel bei einer anderen Firmware-Version, einer bereits veränderten Datei
oder einem beschädigten Download.

## Auf die Kamera bringen

### 1. Auf die SD-Karte kopieren

1. **Formatieren Sie die SD-Karte in der Kamera.**
2. Kopieren Sie **`output/fwdc248b.bin`** in die **oberste Ebene** der Karte:
   nicht in einen Ordner, und der Name muss genau `fwdc248b.bin` bleiben.

### 2. Kamera aktualisieren

1. Setzen Sie den voll geladenen Akku und die SD-Karte ein.
2. Starten Sie das Firmware-Update im Setup-Menü der Kamera, wie in der
   offiziellen Anleitung von RICOH zum Firmware-Update der GR IV beschrieben.
3. **Die Kamera zeigt ein Update von Version 1.11 auf Version 1.11.** Das ist
   so gewollt: Die Firmware mit GF-2-Blitzmodus behält die Versionsnummer.
   Bestätigen Sie das Update.

> [!CAUTION]
> **Schalten Sie die Kamera nicht aus, öffnen Sie weder Akku- noch
> Kartenfach, und nehmen Sie die Karte nicht heraus**, bis das Update
> abgeschlossen ist und die Kamera neu gestartet hat.

### 3. Fotografieren

1. Schieben Sie den GF-2, während Kamera und GF-2 beide **ausgeschaltet** sind,
   vollständig in den Blitzschuh, und schalten Sie dann beide ein.
2. Aufnahmemenü → **Blitzmodus** → **GF-2-Blitzmodus**.
3. Stellen Sie die **Blitzleistung** auf **Auto** oder **1/1** für volle
   Leistung oder auf **1/4**.
4. Fokussieren Sie auf Ihr Motiv und lösen Sie aus.

- Die Firmware-Version zeigt weiterhin **1.11**. Das ist normal.
- Löschen Sie `fwdc248b.bin` von der Karte (oder formatieren Sie die Karte),
  damit das Update nicht versehentlich erneut startet.

### Zurück zur offiziellen Firmware

> [!IMPORTANT]
> **Stellen Sie den Blitzmodus zuerst auf etwas anderes als GF-2-Blitzmodus**,
> zum Beispiel Blitz Ein. Tun Sie dasselbe in jeder eigenen Einstellung (C1, C2,
> …), die ihn verwendet. Die offizielle Firmware hat keine Einstellung
> GF-2-Blitzmodus.

Wiederholen Sie dann die Schritte 1–2 stattdessen mit der **offiziellen**
`fwdc248b.bin` von RICOH. Die Kamera zeigt wieder **1.11 → 1.11**; bestätigen
Sie, und Ihre Kamera ist wieder im Originalzustand.

## Gut zu wissen

- **Schalten Sie Kamera und GF-2 aus, bevor Sie den Blitz aufstecken oder
  abnehmen**, und schieben Sie den GF-2 vollständig in den Blitzschuh.
- **Die Kamera kann nicht erkennen, ob der GF-2 eingeschaltet ist.** Löst er
  nicht aus, stellt die Kamera trotzdem die Belichtung für ein Blitzfoto ein, und
  das Bild wird zu dunkel. Das ist bei der GR III genauso.
- **Sehr nahe Motive** (näher als etwa 0,7 m) werden mit ISO-Automatik etwas zu
  hell: etwa +0,6 EV bei 0,5 m. Der Modus der GR III verhält sich genauso.
- **Feste ISO und weit entfernte Motive:** Sobald die Blende ganz offen ist
  (f/2.8), wird ein weiter entferntes Motiv dunkler. Erhöhen Sie die ISO, oder
  verwenden Sie ISO-Automatik.
- **Helles Tageslicht:** Die Verschlusszeit kann nicht kürzer als die
  Blitzsynchronzeit werden (1/2500 s bei f/2.8–f/4). Ist der Neutralfilter auf
  Auto gestellt, verwendet die Kamera den Neutralfilter, wenn das Licht noch
  deutlich heller ist. Der Blitz wirkt dann als Aufhelllicht.
- **Serienaufnahmen:** Anders als bei der GR III wird nicht automatisch gewartet,
  bis der Blitz wieder geladen ist. Lassen Sie etwa zwei Sekunden zwischen
  Blitzaufnahmen.
- **Fixdistanzvorwahl, B und T sowie Videos** funktionieren wie bisher. Der
  GF-2-Blitzmodus gilt dort nicht.
- **Nicht mit GR4-MonoUnlock oder GR4-XPanUnlock kombinierbar.** Jedes Werkzeug
  geht von der offiziellen Firmware aus, und dieses Werkzeug lehnt deren Dateien
  ab.
- **Ein offizielles Update von RICOH entfernt den GF-2-Blitzmodus.** Es ersetzt
  die gesamte Firmware. Stellen Sie zuerst einen anderen Blitzmodus ein (siehe
  [Zurück zur offiziellen Firmware](#zurück-zur-offiziellen-firmware)).
- **Nur für die normale GR IV.** Installieren Sie die Datei nie auf einem
  anderen Modell.
- **Bevor Sie die Kamera zum Service schicken,** kehren Sie zur offiziellen
  Firmware zurück.

### Firmware-Datei prüfen

Bevor Sie eine Firmware-Datei auf eine Karte kopieren:

```sh
python3 gr4_gf2unlock.py check path/to/fwdc248b.bin
```

Es sagt Ihnen, ob die Datei die offizielle 1.11, die mit diesem Werkzeug
erstellte Version mit GF-2-Blitzmodus oder etwas anderes ist (es erkennt auch
Dateien von GR4-MonoUnlock und GR4-XPanUnlock).

## Risiken

- Ihre Kamera kann eine gute Firmware-Datei nicht von einer beschädigten
  unterscheiden. Kopieren Sie nur eine Datei auf Ihre Karte, die das Werkzeug
  geschrieben (oder mit `check` bestätigt) hat.
- Wenn ein Update unterbrochen wird oder eine Firmware-Datei nicht starten kann,
  erreicht die Kamera die Update-Funktion eventuell nicht mehr und müsste dann
  zum RICOH-Service. Das ist in den Tests nicht passiert, lässt sich aber nicht
  ausschließen.
- Die Rückkehr zur offiziellen Firmware, während der GF-2-Blitzmodus noch
  ausgewählt ist, wurde nicht getestet. Stellen Sie zuerst einen anderen
  Blitzmodus ein.
- Die eigenen Kalibrierungsdaten Ihrer Kamera werden nicht angetastet.

## Teststand

| Was | Stand |
| --- | --- |
| Update akzeptiert, Kamera startet | getestet auf einer GR IV 1.11 |
| GF-2-Blitzmodus im Menü Blitzmodus | getestet auf einer GR IV 1.11 |
| Belichtung aus der Fokusentfernung mit dem GF-2 | getestet auf einer GR IV 1.11 |
| Durchschalten mit ADJ-Hebel und Fn-Taste | offline geprüft; bitte melden Sie Ihre Ergebnisse |
| Blitzleistung 1/4, feste ISO, Neutralfilter, Langzeitsynchronisation | offline geprüft; bitte melden Sie Ihre Ergebnisse |
| Andere Blitzmodi unverändert | offline geprüft; bitte melden Sie Ihre Ergebnisse |
| Die Rückkehr zur offiziellen 1.11 stellt die Kamera vollständig wieder her | getestet mit früherer veränderter Firmware auf einer GR IV 1.11; mit dieser Version noch nicht |
| Das Werkzeug reproduziert die getestete Firmware exakt | getestet |

## Für Entwickler

```
GR4-GF2Unlock/
├── README.md           this guide
├── README.*.md         this guide in Japanese, Chinese, Korean, German, French and Spanish
├── gr4_gf2unlock.py    the tool (Python 3.8+, no extra packages)
└── assets/             the icon, and the script that draws it (render_icon.py)
```

| Datei | SHA-256 |
| --- | --- |
| offizielle `fwdc248b.bin` 1.11 der RICOH GR IV | `a2f664dfca034059eb0fd6e18ab08684c326b4a034d85c164dad7e1ec9b5655f` |
| `fwdc248b.bin` mit GF-2-Blitzmodus, erstellt mit diesem Werkzeug (1.0.0) | `45a2edd33a0e0783458b1052ad8b67514f48b45a5db7b47013543eb46d247f0c` |

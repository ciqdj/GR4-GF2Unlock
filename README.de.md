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
| Einen anderen Blitz als den GF-2 verwenden | [Eigenes Blitzgerät](#eigenes-blitzgerät) |
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

Ist der GF-2-Blitzmodus gewählt, löst die Kamera den Blitz wie bei Blitz Ein aus,
aber mit **fester Leistung**. Dann plant sie die Belichtung so, wie es der
GF-2-Blitzmodus der GR III tut: aus der **Leitzahl** des Blitzes und der
**Fokusentfernung** (Autofokus oder manueller Fokus), innerhalb der eigenen
Grenzen der GR IV für Blende, ISO und Blitzsynchronisation. Die Leitzahl ist die
des GF-2, 3, es sei denn, Sie geben beim Erstellen der Firmware die Ihres
eigenen Blitzes an (siehe [Eigenes Blitzgerät](#eigenes-blitzgerät)).

- **Die Leistung:** Beim GF-2 stellt die Kamera sie über die **Blitzleistung**
  ein: **Auto oder 1/1** ist volle Leistung, **1/4** ist Viertelleistung. Ein
  anderer Blitz löst mit der Leistung aus, die am Blitz selbst eingestellt ist
  (siehe [Eigenes Blitzgerät](#eigenes-blitzgerät)).
- **Mit ISO-Automatik** öffnet die Kamera die Blende und erhöht die ISO, je
  weiter das Motiv entfernt ist. Aus der Nähe bleibt sie bei der niedrigsten ISO
  und schließt die Blende so weit, wie es die Entfernung verlangt, bis f/16.
- **Mit fester ISO** wählt die Kamera die Blende, die zur Entfernung passt.
- **Die Verschlusszeit** richtet sich nach dem Licht um das Motiv herum. Sie
  bleibt innerhalb der Blitzsynchronzeit, sodass der Blitz immer im Bild ist.
  Die längste ist 1/32 s, oder bis zu 32 s mit Langzeitsynchronisation an einem
  dunklen Ort.
- **In Tv, Av und M** werden die von Ihnen eingestellten Werte übergangen, wie
  bei der GR III.
- **Mit Neutralfilter auf Auto** bleibt die Belichtung bei hellem Licht normal.
  Wenn Blende und Verschlusszeit sie nicht mehr halten können, senkt die Kamera
  die ISO (ISO-Automatik), schließt die Blende und schaltet dann den
  Neutralfilter dazu (siehe [Helles Licht](#helles-licht-neutralfilter-auto)).

Die Belichtungsberechnung stammt von RICOH selbst, übernommen aus der Firmware
2.10 der GR III. Alles andere ist die offizielle Firmware der GR IV,
unverändert.

### Was Sie erwarten können

Typische Werte in einem schwach beleuchteten Raum, Blitzleistung Auto oder 1/1,
Neutralfilter aus (EXIF kann sie leicht runden):

| Entfernung | ISO-Automatik | Feste ISO 400 |
| ---: | --- | --- |
| 0,5 m | f/5.9, ISO 100 | f/11.8 |
| 1 m | f/3.0, ISO 100 | f/5.9 |
| 2 m | f/2.8, ISO 367 | f/3.0 |
| 3 m | f/2.8, ISO 800 | f/2.8 |
| 5 m | f/2.8, ISO 2263 | f/2.8 (Motiv dunkler: außerhalb der Blitzreichweite) |

Mit Blitzleistung **1/4** liegt die ISO etwa zwei Stufen höher oder die Blende
etwa zwei Stufen weiter offen. Mit einer anderen Leitzahl skaliert die Blende
mit ihr: Blendenzahl = Leitzahl × √(ISO / 100) ÷ Entfernung, innerhalb von
f/2.8–f/16.

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
- Er funktioniert in **P, Tv, Av oder M** mit dem GF-2 und mit **jedem Blitz,
  der nicht mit der Kamera kommuniziert**, etwa einem manuellen Blitz, wie bei
  der GR III. Die Belichtung wird für die Leitzahl in der Firmware berechnet: die
  des GF-2 oder die Ihres eigenen Blitzes (siehe
  [Eigenes Blitzgerät](#eigenes-blitzgerät)).
- Mit einem **P-TTL-Blitz**, der mit der Kamera kommuniziert, etwa einem Blitz
  von RICOH oder PENTAX, funktioniert der GF-2-Blitzmodus wie Blitz Ein,
  ebenfalls wie bei der GR III.
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
| Blitzleistung | Nur volle Leistung: Die GR III kann den GF-2 nicht steuern | Mit dem GF-2 volle oder Viertelleistung (Blitzleistung 1/1 oder 1/4), mit jeweils eigens berechneter Belichtung |
| Leitzahl | Immer 3, die des GF-2 | 3 oder die Ihres eigenen Blitzes (1 bis 90) |
| Nahe Motive mit ISO-Automatik | Bis zu etwa 1 EV zu hell, näher als 0,7 m | Die Blende, die die Entfernung verlangt, bis f/16 |
| ISO-Automatik mit eingeschaltetem Neutralfilter | Der Hintergrund wird zwei Stufen zu dunkel | Die Verschlusszeit berücksichtigt den Neutralfilter, sodass der Hintergrund richtig belichtet wird |
| Sehr nahe Motive bei hellem Licht | Kann f/19 verlangen, jenseits von f/16 des Objektivs | Bleibt innerhalb von f/2.8–f/16 |
| Helles Licht, Neutralfilter Auto | Bis zu eine Stufe zu hell, und der Neutralfilter macht den Blitz dann zwei Stufen zu schwach | Niedrigere ISO, kleinere Blende, dann der Neutralfilter: Das Bild wird richtig belichtet, und der Blitz verliert nur das Licht, das wegfallen musste |
| Nahe Motive, Neutralfilter Auto | Selbst bei f/16 mit fester ISO zu hell | Der Neutralfilter, mit entsprechend weiter geöffneter Blende |
| Blitzsynchronisation | Kann eine kürzere Verschlusszeit als die Blitzsynchronzeit verlangen | Immer innerhalb der Blitzsynchronzeit, die bei der GR IV von der Blende abhängt |
| Alles andere | Das Einschalten des Modus ersetzt das normale Blitzverhalten | Eine von fünf Auswahlmöglichkeiten im Blitzmodus: Wechseln Sie jederzeit zurück zu Blitz Ein und zur automatischen Blitzleistung der GR IV |

Mehr als 250.000 Kombinationen aus Entfernung, ISO, Neutralfilter, Blitzmodus,
Licht, Blitztyp und Leitzahl (1 bis 90) wurden geprüft. Keine davon verlangt
eine Blende außerhalb von f/2.8–f/16, eine ISO außerhalb Ihrer Grenzen oder eine
Verschlusszeit, mit der der Blitz nicht synchronisieren kann.

## Bevor Sie beginnen

- **Kamera:** RICOH GR IV (das normale Farbmodell). Andere Modelle werden nicht
  unterstützt.
- **Blitz:** RICOH GF-2 oder ein manueller Blitz, dessen Leitzahl Sie kennen
  (siehe [Eigenes Blitzgerät](#eigenes-blitzgerät)). Die anderen Blitzmodi
  funktionieren mit jedem Blitz wie bisher.
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
wrote output/fwdc248b.bin  (SHA-256 ab00b2487126b4ab14e4872288970bb4a51f99ef7b56e57356a9603da6778bec)
```

Wenn etwas nicht stimmt, gibt es `refused: …` aus und schreibt **nichts**: zum
Beispiel bei einer anderen Firmware-Version, einer bereits veränderten Datei
oder einem beschädigten Download.

### Eigenes Blitzgerät

Der GF-2-Blitzmodus plant die Belichtung für die Leitzahl des GF-2, 3. Um einen
anderen Blitz zu verwenden, fügen Sie seine Leitzahl mit `--gn` hinzu:

```sh
python3 gr4_gf2unlock.py patch ~/Downloads/fwdc248b.bin --gn 12
```

- **Welche Blitzgeräte:** jeder Blitz, der nicht mit der Kamera kommuniziert
  und über den Mittenkontakt des Blitzschuhs auslöst: manuelle Blitzgeräte und
  die meisten Blitzgeräte für andere Kameramarken. Ein P-TTL-Blitz oder ein
  kompatibler Blitz im P-TTL-Modus kommuniziert mit der Kamera; der
  GF-2-Blitzmodus funktioniert dann wie Blitz Ein, wie bei der GR III.
- Geben Sie die Leitzahl **bei ISO 100, in Metern**, bei voller Leistung an, aus
  der Anleitung des Blitzes. Eine Leitzahl in Fuß: durch 3,3 teilen. Ein
  Zoom-Blitz: Verwenden Sie die Leitzahl für die Zoomstellung, mit der Sie
  fotografieren.
- Erlaubt: **1 bis 90**. Die Kamera rechnet in Schritten von 1/16 Blendenstufe,
  und das Werkzeug zeigt den Wert, den es verwendet, zum Beispiel
  `guide number: 11.81` für 12.
- **Die Kamera kann die Leistung eines solchen Blitzes nicht einstellen.**
  Stellen Sie den Blitz auf **volle manuelle Leistung** und die Blitzleistung
  auf **Auto** oder **1/1**. Stellen Sie den Blitz stattdessen auf 1/4 Leistung,
  stellen Sie auch die Blitzleistung auf **1/4**: Die Kamera plant dann zwei
  Stufen weniger ein.
- Das Werkzeug erstellt zuerst die Standard-Firmware und prüft sie wie oben,
  dann ändert es nur die Leitzahl. Die SHA-256 unterscheidet sich dann von der
  oben genannten; `check` zeigt die Leitzahl einer Datei.
- Um die Leitzahl zu ändern, erstellen Sie die Firmware erneut und installieren
  Sie sie.

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
- **Die Kamera kann nicht erkennen, ob der Blitz auslösen wird.** Ist der
  GF-2-Blitzmodus gewählt, stellt sie die Belichtung für ein Blitzfoto ein, auch
  wenn der Blitz ausgeschaltet, nicht aufgesteckt oder noch nicht wieder geladen
  ist. Dieses Bild wird zu dunkel. Das ist bei der GR III genauso.
- **Ein leistungsstarker Blitz aus der Nähe:** Ist das Motiv so nah, dass selbst
  f/16 bei der niedrigsten ISO zu viel Blitzlicht durchlässt, schaltet die
  Kamera den Neutralfilter dazu, wenn er auf Auto gestellt ist, und öffnet die
  Blende entsprechend. Bei ausgeschaltetem Neutralfilter oder einem noch näheren
  Motiv wird das Bild heller als geplant: Verwenden Sie Blitzleistung 1/4, oder
  gehen Sie weiter weg.
- **Feste ISO und weit entfernte Motive:** Sobald die Blende ganz offen ist
  (f/2.8), wird ein weiter entferntes Motiv dunkler. Erhöhen Sie die ISO, oder
  verwenden Sie ISO-Automatik.
- **Helles Tageslicht:** Die Verschlusszeit kann nicht kürzer als die
  Blitzsynchronzeit werden (1/2500 s bei f/2.8–f/4, 1/4000 s ab f/5.6). Siehe
  [Helles Licht](#helles-licht-neutralfilter-auto) unten.
- **Serienaufnahmen:** Anders als bei der GR III wird nicht automatisch gewartet,
  bis der Blitz wieder geladen ist. Lassen Sie etwa zwei Sekunden zwischen
  Blitzaufnahmen.
- **Fixdistanzvorwahl, B und T sowie Videos** funktionieren wie bisher. Der
  GF-2-Blitzmodus gilt dort nicht.
- **Nicht mit GR4-MonoUnlock oder GR4-XPanUnlock kombinierbar.** Jedes Werkzeug
  geht von der offiziellen Firmware aus, und dieses Werkzeug lehnt deren Dateien
  ab.
- **Update von einem früheren GR4-GF2Unlock:** Installieren Sie die neue Datei
  auf die gleiche Weise. Sie müssen nicht zuerst zur offiziellen Firmware
  zurückkehren. Die Versionen 1.1.0 und 1.2.0 wendeten den GF-2-Blitzmodus nur
  auf Blitzgeräte an, die die Kamera erkennt, sodass er mit einem manuellen
  Blitz keine Wirkung hatte; 1.3.0 behebt das. 1.4.0 ergänzt die Behandlung von
  hellem Licht mit Neutralfilter auf Auto.
- **Ein offizielles Update von RICOH entfernt den GF-2-Blitzmodus.** Es ersetzt
  die gesamte Firmware. Stellen Sie zuerst einen anderen Blitzmodus ein (siehe
  [Zurück zur offiziellen Firmware](#zurück-zur-offiziellen-firmware)).
- **Nur für die normale GR IV.** Installieren Sie die Datei nie auf einem
  anderen Modell.
- **Bevor Sie die Kamera zum Service schicken,** kehren Sie zur offiziellen
  Firmware zurück.

### Helles Licht (Neutralfilter Auto)

Bei hellem Licht erreicht die Verschlusszeit die Blitzsynchronzeit, und die
Blende, die der GF-2-Blitzmodus für den Blitz gewählt hat, würde zu viel
Tageslicht durchlassen. Ist der **Neutralfilter auf Auto** gestellt
(Aufnahmemenü), hält die Kamera die Belichtung normal, und zwar in dieser
Reihenfolge:

1. **ISO-Automatik:** Sie senkt die ISO, bis zu Ihrer Untergrenze. Die Blende
   bleibt.
2. Sie schließt die Blende, bis f/16.
3. Ist f/16 bei der kürzesten Blitzsynchronzeit immer noch zu hell, oder ist
   der Blitz allein selbst bei f/16 zu stark, schaltet sie den
   **Neutralfilter** (2 Stufen) dazu. Dann öffnet sie die Blende wieder so
   weit, wie es das Licht erlaubt.

Der Hintergrund wird dann richtig belichtet. Der Blitz behält seine geplante
Leistung im Verhältnis zur Belichtung, abzüglich nur dessen, was das Tageslicht
erzwungen hat: Bei Sonnenschein wirkt er als Aufhelllicht. Typische Werte bei
Sonnenschein (etwa EV 15), Blitzleistung Auto oder 1/1, Neutralfilter Auto, in
Klammern mit Neutralfilter aus, wo es abweicht:

| Entfernung | ISO-Automatik | Feste ISO 400 | Feste ISO 3200 |
| ---: | --- | --- | --- |
| 0,3 m | f/11.8, ISO 100 | f/9.9 mit Neutralfilter (f/16, Blitz zu hell) | f/16 mit Neutralfilter, noch immer zu hell (f/16, Blitz viel zu hell) |
| 1 m | f/3.7, ISO 100 (f/3.5, zu hell) | f/5.9 | f/8.4 mit Neutralfilter (f/16, Blitz zu hell) |
| 3 m | f/3.7, ISO 100 (f/3.4, ISO 141, zu hell) | f/5.7 (f/2.8, zu hell) | f/16 (f/5.7, zu hell) |

- Mit Neutralfilter **Ein** oder **Aus** funktioniert der GF-2-Blitzmodus wie
  in 1.3.0: Die Kamera ändert ISO und Blende nicht wegen des Tageslichts, und
  ein sonniger Hintergrund kann zu hell werden.
- Dafür ist der Neutralfilter nötig, daher gilt dies für die normale GR IV. Die
  GR IV HDF hat keinen Neutralfilter: Ihre Firmware behandelt den Neutralfilter
  immer als ausgeschaltet, sodass sich dort nichts ändert.

### Firmware-Datei prüfen

Bevor Sie eine Firmware-Datei auf eine Karte kopieren:

```sh
python3 gr4_gf2unlock.py check path/to/fwdc248b.bin
```

Es sagt Ihnen, ob die Datei die offizielle 1.11, die mit diesem Werkzeug
erstellte Version mit GF-2-Blitzmodus (mit ihrer Leitzahl) oder etwas anderes
ist (es erkennt auch Dateien von GR4-GF2Unlock 1.0.0 bis 1.3.0,
GR4-MonoUnlock und GR4-XPanUnlock).

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
| GF-2-Blitzmodus mit einem manuellen Blitz (1.3.0) | offline geprüft; bitte melden Sie Ihre Ergebnisse |
| P-TTL-Blitzgeräte funktionieren wie Blitz Ein (1.3.0) | offline geprüft; bitte melden Sie Ihre Ergebnisse |
| Eigene Leitzahl (`--gn`) | offline geprüft; bitte melden Sie Ihre Ergebnisse |
| Nahe Motive mit ISO-Automatik (exakte Blende) | offline geprüft; bitte melden Sie Ihre Ergebnisse |
| Durchschalten mit ADJ-Hebel und Fn-Taste | offline geprüft; bitte melden Sie Ihre Ergebnisse |
| Blitzleistung 1/4, feste ISO, Neutralfilter, Langzeitsynchronisation | offline geprüft; bitte melden Sie Ihre Ergebnisse |
| Helles Licht mit Neutralfilter auf Auto (1.4.0) | offline geprüft; bitte melden Sie Ihre Ergebnisse |
| Andere Blitzmodi unverändert | offline geprüft; bitte melden Sie Ihre Ergebnisse |
| Die Rückkehr zur offiziellen 1.11 stellt die Kamera vollständig wieder her | getestet mit früherer veränderter Firmware auf einer GR IV 1.11; mit dieser Version noch nicht |
| Das Werkzeug reproduziert die Referenz-Firmware exakt | getestet |

Die Kameratests wurden mit Version 1.0.0 durchgeführt. Seitdem lässt sich die
Leitzahl einstellen, und nahe Motive mit ISO-Automatik erhalten die exakte
Blende (1.2.0); außerdem gilt der GF-2-Blitzmodus, wie bei der GR III, für
Blitzgeräte, die die Kamera nicht erkennt (1.3.0), und mit Neutralfilter auf
Auto bleibt die Belichtung bei hellem Licht normal (1.4.0).

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
| `fwdc248b.bin` mit GF-2-Blitzmodus, erstellt mit diesem Werkzeug (1.4.0, Leitzahl 3) | `ab00b2487126b4ab14e4872288970bb4a51f99ef7b56e57356a9603da6778bec` |
| `fwdc248b.bin` mit GF-2-Blitzmodus, Version 1.3.0 | `86abac009d3664ede49ef912073d00b8fb15ac7e9867265aecda581c932db41a` |
| `fwdc248b.bin` mit GF-2-Blitzmodus, Version 1.2.0 | `225258d201217bac3416de79de94aea4d05c6aab74d4f026c30280ac8a624c22` |
| `fwdc248b.bin` mit GF-2-Blitzmodus, Version 1.1.0 | `660df9de1e611325fc41df2e42499028c7296c037201b7fd7be828b813ec1c75` |
| `fwdc248b.bin` mit GF-2-Blitzmodus, Version 1.0.0 (nur GF-2) | `45a2edd33a0e0783458b1052ad8b67514f48b45a5db7b47013543eb46d247f0c` |

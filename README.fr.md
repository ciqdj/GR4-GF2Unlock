<p align="center">
  <img src="assets/icon-256.png" width="112" height="112" alt="Icône de GR4-GF2Unlock : un flash GF-2 dont le faisceau s'atténue en six bandes d'un IL chacune">
</p>

<h1 align="center">GR4-GF2Unlock</h1>

<p align="center">
  <strong>Le Mode flash GF-2 du GR III, sur votre RICOH GR IV.<br>Faites la mise au point sur votre sujet ; l'appareil règle l'exposition au flash.</strong>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.de.md">Deutsch</a> |
  <strong>Français</strong> |
  <a href="README.es.md">Español</a>
</p>

Avec le firmware 2.10, RICOH a doté le GR III du **Mode flash GF-2** : avec le
petit flash RICOH GF-2 fixé, l'appareil déclenche le flash à une puissance fixe
et détermine l'ouverture, la sensibilité ISO et la vitesse d'obturation à partir
de la **distance de mise au point**. Le GR IV n'a jamais reçu ce mode.

GR4-GF2Unlock l'ajoute au GR IV comme **cinquième option du Mode flash**, à côté
de Flash forcé, Flash forcé+yeux rouges, Synchro lente et Synchro lente+yx
rouges. Tout le reste de votre appareil reste exactement comme avant, et vous
pouvez revenir au firmware officiel à tout moment.

Ce dépôt ne contient aucun firmware RICOH. Vous téléchargez vous-même le
firmware officiel chez RICOH, et l'outil fourni le transforme en version avec
Mode flash GF-2, sur votre propre ordinateur.

> [!WARNING]
> **Non officiel, à vos risques et périls.** Ni conçu ni approuvé par RICOH IMAGING.
> L'installation d'un firmware modifié peut annuler votre garantie. Lisez d'abord
> [Avant de commencer](#avant-de-commencer) et [Risques](#risques).

| Vous voulez | Allez à |
| --- | --- |
| Voir ce que l'appareil règle à chaque distance | [À quoi s'attendre](#à-quoi-sattendre) |
| Créer le firmware (macOS, Windows, Linux) | [Créer le firmware](#créer-le-firmware) |
| Utiliser un autre flash que le GF-2 | [Votre propre flash](#votre-propre-flash) |
| L'installer | [Installer sur l'appareil](#installer-sur-lappareil) |
| Savoir ce que contient un fichier de firmware | [Vérifier un fichier de firmware](#vérifier-un-fichier-de-firmware) |
| Revenir au firmware de RICOH | [Revenir au firmware officiel](#revenir-au-firmware-officiel) |

**Sommaire :**
[Comment ça marche](#comment-ça-marche) |
[Ce que vous obtenez](#ce-que-vous-obtenez) |
[Avant de commencer](#avant-de-commencer) |
[Créer le firmware](#créer-le-firmware) |
[Installer sur l'appareil](#installer-sur-lappareil) |
[Bon à savoir](#bon-à-savoir) |
[Risques](#risques) |
[État des tests](#état-des-tests) |
[Pour les développeurs](#pour-les-développeurs)

## Comment ça marche

Avec le Mode flash GF-2 sélectionné, l'appareil déclenche le flash comme en
Flash forcé, mais à une **puissance fixe**. Il calcule ensuite l'exposition
comme le fait le Mode flash GF-2 du GR III : à partir du **nombre guide** du
flash et de la **distance de mise au point** (autofocus ou mise au point
manuelle), dans les limites d'ouverture, de sensibilité ISO et de synchro flash
propres au GR IV. Le nombre guide est celui du GF-2, 3, sauf si vous indiquez
celui de votre propre flash en créant le firmware (voir
[Votre propre flash](#votre-propre-flash)).

- **La puissance :** l'appareil règle le GF-2 avec **Intensité du flash** :
  **Auto ou 1/1** correspond à la pleine puissance, **1/4** au quart de
  puissance. Un autre flash se déclenche à la puissance réglée sur le flash
  lui-même (voir [Votre propre flash](#votre-propre-flash)).
- **En ISO Auto,** l'appareil ouvre l'ouverture et augmente la sensibilité ISO à
  mesure que le sujet s'éloigne. De près, il reste à l'ISO le plus bas et ferme
  l'ouverture autant que la distance l'exige, jusqu'à f/16.
- **Avec un ISO fixe,** l'appareil choisit l'ouverture adaptée à la distance.
- **La vitesse d'obturation** suit la lumière autour du sujet. Elle reste dans
  la plage de synchro flash, de sorte que le flash est toujours dans l'image. La
  plus lente est 1/32 s, ou jusqu'à 32 s avec la synchro lente dans un endroit
  sombre.
- **En Tv, Av et M,** les valeurs que vous réglez sont remplacées, comme sur le
  GR III.
- **Avec Filtre ND réglé sur Auto,** l'exposition reste normale en pleine
  lumière. Lorsque l'ouverture et la vitesse d'obturation ne suffisent plus,
  l'appareil abaisse la sensibilité ISO (ISO Auto), ferme l'ouverture, puis
  ajoute le filtre ND (voir [Pleine lumière](#pleine-lumière-filtre-nd-auto)).

Le calcul de l'exposition est celui de RICOH, repris du firmware 2.10 du GR III.
Tout le reste est le firmware officiel du GR IV, inchangé.

### À quoi s'attendre

Valeurs typiques dans une pièce faiblement éclairée, Intensité du flash Auto ou
1/1, filtre ND désactivé (l'EXIF peut les arrondir légèrement) :

| Distance | ISO Auto | ISO 400 fixe |
| ---: | --- | --- |
| 0,5 m | f/5.9, ISO 100 | f/11.8 |
| 1 m | f/3.0, ISO 100 | f/5.9 |
| 2 m | f/2.8, ISO 367 | f/3.0 |
| 3 m | f/2.8, ISO 800 | f/2.8 |
| 5 m | f/2.8, ISO 2263 | f/2.8 (sujet plus sombre : hors de portée du flash) |

Avec Intensité du flash sur **1/4**, la sensibilité ISO est plus élevée
d'environ deux IL, ou l'ouverture plus grande d'environ deux IL. Avec un autre
nombre guide, l'ouverture varie en proportion : ouverture = nombre guide ×
√(ISO / 100) ÷ distance, dans la plage f/2.8–f/16.

> [!TIP]
> **Vérifiez que le mode est actif.** Sélectionnez Mode flash GF-2, passez en
> mode **M**, réglez **ISO 400** et une vitesse d'obturation de 1/2000 s ou plus
> lente. Photographiez quelque chose à environ 1 m, puis quelque chose à environ
> 3 m. L'ouverture change d'elle-même, à environ f/5.9 puis f/2.8, quelle que
> soit la valeur que vous avez réglée.

## Ce que vous obtenez

Après l'installation, **Mode flash** (dans le menu, sur le levier ADJ et sur la
touche Fn) propose :

| Affiché comme | Ce que fait le flash |
| --- | --- |
| Flash forcé | se déclenche à chaque prise de vue, comme avant |
| Flash forcé+yeux rouges | comme avant |
| Synchro lente | comme avant |
| Synchro lente+yx rouges | comme avant |
| **Mode flash GF-2** | **puissance fixe ; ouverture, sensibilité ISO et vitesse d'obturation déterminées par la distance de mise au point** |

- La nouvelle entrée a son propre nom dans chaque langue du menu, par exemple
  « Mode flash GF-2 » en français. Lorsque la synchro lente n'est pas
  disponible, les choix sont Flash forcé, Flash forcé+yeux rouges et Mode flash
  GF-2.
- Il fonctionne en **P, Tv, Av ou M** avec le GF-2 et avec **tout flash qui ne
  communique pas avec l'appareil**, par exemple un flash manuel, comme sur le
  GR III. L'exposition est calculée pour le nombre guide inscrit dans le
  firmware : celui du GF-2, ou celui de votre propre flash (voir
  [Votre propre flash](#votre-propre-flash)).
- Avec un **flash P-TTL** qui communique avec l'appareil, tel qu'un flash RICOH
  ou PENTAX, le Mode flash GF-2 fonctionne comme Flash forcé, là aussi comme sur
  le GR III.
- Le réglage est conservé lorsque l'appareil est éteint, comme tout réglage du
  Mode flash.
- L'écran de prise de vue affiche l'icône **Flash forcé**, et les photos
  enregistrent le flash comme déclenché, comme en Flash forcé.
- **Toutes les autres options du Mode flash fonctionnent exactement comme
  avant**, y compris Intensité du flash Auto, 1/1 et 1/4.

### Mieux que l'original sur le GR III

Autour du calcul d'exposition de RICOH, la version GR IV utilise du matériel que
le GR III n'a pas, et corrige quelques points faibles :

| | GR III 2.10 | GR4-GF2Unlock |
| --- | --- | --- |
| Puissance du flash | Pleine puissance uniquement : le GR III ne peut pas piloter le GF-2 | Avec le GF-2, pleine puissance ou quart de puissance (Intensité du flash 1/1 ou 1/4), avec l'exposition calculée pour chacune |
| Nombre guide | Toujours 3, celui du GF-2 | 3, ou celui de votre propre flash (1 à 90) |
| Sujets proches avec ISO Auto | Jusqu'à environ 1 IL trop clair en dessous de 0,7 m | L'ouverture qu'exige la distance, jusqu'à f/16 |
| ISO Auto avec le filtre ND activé | L'arrière-plan est sous-exposé de deux IL | La vitesse d'obturation tient compte du filtre ND, l'arrière-plan est donc correctement exposé |
| Sujets très proches en pleine lumière | Peut demander f/19, au-delà du f/16 de l'objectif | Reste dans la plage f/2.8–f/16 |
| Pleine lumière, filtre ND Auto | Jusqu'à un IL trop clair, puis le filtre ND rend le flash trop faible de deux IL | ISO plus bas, ouverture plus petite, puis filtre ND : la photo est correctement exposée, et le flash ne perd que la lumière qu'il fallait retirer |
| Sujets proches, filtre ND Auto | Trop clair même à f/16 avec un ISO fixe | Le filtre ND, avec l'ouverture agrandie en conséquence |
| Synchro flash | Peut demander une vitesse d'obturation plus rapide que la synchro flash | Toujours dans la plage de synchro flash, qui dépend de l'ouverture sur le GR IV |
| Tout le reste | Activer le mode remplace le comportement normal du flash | Une option du Mode flash parmi cinq : revenez à Flash forcé et à l'intensité du flash automatique du GR IV quand vous voulez |

Plus de 250 000 combinaisons de distance, de sensibilité ISO, de filtre ND, de
mode de flash, de lumière, de type de flash et de nombre guide (1 à 90) ont été
vérifiées. Aucune ne demande une ouverture en dehors de f/2.8–f/16, une sensibilité ISO en dehors
de vos limites ni une vitesse d'obturation avec laquelle le flash ne peut pas se
synchroniser.

## Avant de commencer

- **Appareil :** RICOH GR IV (le modèle couleur standard). Les autres modèles ne
  sont pas pris en charge.
- **Flash :** RICOH GF-2, ou un flash manuel dont vous connaissez le nombre guide
  (voir [Votre propre flash](#votre-propre-flash)). Les autres options du Mode
  flash fonctionnent avec tous les flashs comme avant.
- **Votre appareil doit déjà être en firmware 1.11.** Vérifiez la version dans
  le menu de configuration de l'appareil.
  - Version plus ancienne : mettez d'abord à jour vers la 1.11 de la manière habituelle, avec le fichier officiel de RICOH.
  - Version plus récente : **n'utilisez pas cet outil.** Il ne prend en charge que la 1.11.
- **Le fichier de firmware officiel.** Sur la page d'assistance officielle du
  GR IV de RICOH IMAGING, téléchargez la **version de firmware 1.11**.
  Décompressez-la si nécessaire jusqu'à obtenir le fichier **`fwdc248b.bin`**.
- **Une batterie complètement chargée.** Une mise à jour du firmware ne doit
  jamais être privée d'alimentation.
- **Une carte SD** que vous pouvez formater.
- **Un ordinateur avec Python 3.8 ou plus récent.** macOS et la plupart des
  systèmes Linux l'ont déjà ; sous Windows, installez-le depuis python.org. Rien
  d'autre n'est nécessaire.
- Notez les réglages personnalisés (C1, C2, …) que vous ne voudriez pas refaire.

## Créer le firmware

Ouvrez un terminal dans ce dossier et lancez (avec le chemin où vous avez
enregistré le fichier officiel) :

```sh
python3 gr4_gf2unlock.py patch ~/Downloads/fwdc248b.bin
```

Sous Windows :

```bat
py gr4_gf2unlock.py patch C:\Users\you\Downloads\fwdc248b.bin
```

L'outil vérifie d'abord que vous lui avez donné le véritable fichier officiel
1.11, puis crée le firmware avec Mode flash GF-2 et le vérifie. Cela prend
environ une minute. Si tout est correct, il se termine ainsi :

```
wrote output/fwdc248b.bin  (SHA-256 ab00b2487126b4ab14e4872288970bb4a51f99ef7b56e57356a9603da6778bec)
```

En cas de problème, il affiche `refused: …` et n'écrit **rien** : par exemple
une autre version de firmware, un fichier déjà modifié ou un téléchargement
endommagé.

### Votre propre flash

Le Mode flash GF-2 calcule l'exposition pour le nombre guide du GF-2, 3. Pour
utiliser un autre flash, ajoutez son nombre guide avec `--gn` :

```sh
python3 gr4_gf2unlock.py patch ~/Downloads/fwdc248b.bin --gn 12
```

- **Quels flashs :** tout flash qui ne communique pas avec l'appareil et se
  déclenche par le contact central de la griffe flash : les flashs manuels, et
  la plupart des flashs conçus pour d'autres marques d'appareils. Un flash
  P-TTL, ou un flash compatible en mode P-TTL, communique avec l'appareil ; le
  Mode flash GF-2 fonctionne alors comme Flash forcé, comme sur le GR III.
- Indiquez le nombre guide **à ISO 100, en mètres**, à pleine puissance, tel que
  donné dans le manuel du flash. Un nombre guide en pieds : divisez-le par 3,3.
  Un flash à zoom : prenez le nombre guide correspondant à la focale de zoom
  avec laquelle vous photographiez.
- Valeurs permises : **1 à 90**. L'appareil travaille par pas de 1/16 d'IL, et
  l'outil affiche la valeur qu'il utilise, par exemple `guide number: 11.81`
  pour 12.
- **L'appareil ne peut pas régler la puissance d'un tel flash.** Réglez le
  flash sur la **pleine puissance manuelle** et Intensité du flash sur **Auto**
  ou **1/1**. Si vous réglez plutôt le flash sur 1/4 de puissance, réglez aussi
  Intensité du flash sur **1/4** : l'appareil prévoit alors deux IL de moins.
- L'outil crée d'abord le firmware standard et le vérifie comme ci-dessus, puis
  ne modifie que le nombre guide. Le SHA-256 est alors différent de celui
  ci-dessus ; `check` affiche le nombre guide d'un fichier.
- Pour changer le nombre guide, créez à nouveau le firmware et installez-le.

## Installer sur l'appareil

### 1. Copier sur la carte SD

1. **Formatez la carte SD dans l'appareil.**
2. Copiez **`output/fwdc248b.bin`** à la **racine** de la carte : pas dans un
   dossier, et gardez exactement le nom `fwdc248b.bin`.

### 2. Mettre à jour l'appareil

1. Insérez la batterie complètement chargée et la carte SD.
2. Lancez la mise à jour du firmware depuis le menu de configuration de
   l'appareil, comme décrit dans les instructions officielles de RICOH pour la
   mise à jour du firmware du GR IV.
3. **L'appareil affiche une mise à jour de la version 1.11 vers la version 1.11.**
   C'est normal : le firmware avec Mode flash GF-2 conserve le numéro de
   version. Confirmez la mise à jour.

> [!CAUTION]
> **N'éteignez pas l'appareil, n'ouvrez pas la trappe de la batterie ou de la
> carte et ne retirez pas la carte** avant que la mise à jour soit terminée et
> que l'appareil ait redémarré.

### 3. Photographier

1. Avec l'appareil et le GF-2 tous deux **éteints**, glissez le GF-2 à fond dans
   la griffe flash, puis allumez-les tous les deux.
2. Menu de prise de vue → **Mode flash** → **Mode flash GF-2**.
3. Réglez **Intensité du flash** sur **Auto** ou **1/1** pour la pleine
   puissance, ou sur **1/4**.
4. Faites la mise au point sur votre sujet et déclenchez.

- La version du firmware affiche toujours **1.11**. C'est normal.
- Supprimez `fwdc248b.bin` de la carte (ou formatez la carte) pour que la mise à
  jour ne soit pas relancée par erreur.

### Revenir au firmware officiel

> [!IMPORTANT]
> **Réglez d'abord Mode flash sur autre chose que Mode flash GF-2**, par exemple
> Flash forcé. Faites de même dans chaque mode personnalisé (C1, C2, …) qui
> l'utilise. Le firmware officiel n'a pas de réglage Mode flash GF-2.

Répétez ensuite les étapes 1–2, cette fois avec le `fwdc248b.bin` **officiel** de
RICOH. L'appareil affiche à nouveau **1.11 → 1.11** ; confirmez, et votre
appareil retrouve son état d'origine.

## Bon à savoir

- **Éteignez l'appareil et le GF-2 avant de fixer ou de retirer le flash**, et
  enfoncez le GF-2 à fond dans la griffe flash.
- **L'appareil ne peut pas savoir si le flash va se déclencher.** Avec le Mode
  flash GF-2 sélectionné, il règle l'exposition pour une photo au flash même
  lorsque le flash est éteint, non fixé ou encore en recharge. Cette photo sera
  alors trop sombre. C'est aussi le cas sur le GR III.
- **Un flash puissant de près :** lorsque le sujet est si proche que même f/16
  à l'ISO le plus bas laisse entrer trop de lumière du flash, l'appareil ajoute
  le filtre ND si Filtre ND est réglé sur Auto, et agrandit l'ouverture en
  conséquence. Avec le filtre ND désactivé, ou un sujet plus proche encore, la
  photo est plus claire que prévu : utilisez Intensité du flash 1/4, ou reculez.
- **ISO fixe et sujets éloignés :** une fois l'ouverture au maximum (f/2.8), un
  sujet plus éloigné devient plus sombre. Augmentez la sensibilité ISO, ou
  utilisez ISO Auto.
- **Plein soleil :** la vitesse d'obturation ne peut pas être plus rapide que la
  synchro flash (1/2500 s à f/2.8–f/4, 1/4000 s à partir de f/5.6). Voir
  [Pleine lumière](#pleine-lumière-filtre-nd-auto) ci-dessous.
- **Rafale :** contrairement au GR III, il n'y a pas d'attente automatique de la
  recharge du flash. Laissez environ deux secondes entre deux photos au flash.
- **Priorité dist. inst. AE, B et T, ainsi que la vidéo** fonctionnent comme
  avant. Le Mode flash GF-2 ne s'y applique pas.
- **Non combinable avec GR4-MonoUnlock ou GR4-XPanUnlock.** Chaque outil part du
  firmware officiel, et cet outil refuse leurs fichiers.
- **Mise à jour depuis un GR4-GF2Unlock antérieur :** installez le nouveau
  fichier de la même façon. Inutile de revenir d'abord au firmware officiel.
  Les versions 1.1.0 et 1.2.0 n'appliquaient le Mode flash GF-2 qu'aux flashs
  détectés par l'appareil, si bien qu'il restait sans effet avec un flash
  manuel ; la 1.3.0 corrige ce point. La 1.4.0 ajoute la gestion de la pleine
  lumière avec Filtre ND réglé sur Auto.
- **Une mise à jour officielle de RICOH supprime le Mode flash GF-2.** Elle
  remplace l'intégralité du firmware. Réglez d'abord une autre option du Mode
  flash (voir [Revenir au firmware officiel](#revenir-au-firmware-officiel)).
- **Uniquement pour le GR IV standard.** N'installez jamais ce fichier sur un
  autre modèle.
- **Avant d'envoyer l'appareil en réparation,** revenez au firmware officiel.

### Pleine lumière (filtre ND Auto)

En pleine lumière, la vitesse d'obturation atteint la synchro flash, et
l'ouverture choisie par le Mode flash GF-2 pour le flash laisserait entrer trop
de lumière du jour. Avec **Filtre ND réglé sur Auto** (menu de prise de vue),
l'appareil maintient une exposition normale, dans cet ordre :

1. **ISO Auto :** il abaisse la sensibilité ISO, jusqu'à votre limite inférieure.
   L'ouverture ne change pas.
2. Il ferme l'ouverture, jusqu'à f/16.
3. Lorsque f/16 à la vitesse de synchro flash la plus rapide reste trop clair,
   ou que le flash seul est trop fort même à f/16, il ajoute le **filtre ND**
   (2 IL). Il agrandit ensuite à nouveau l'ouverture autant que la lumière le
   permet.

L'arrière-plan est alors correctement exposé. Le flash garde la puissance prévue
par rapport à l'exposition, moins seulement ce que la lumière du jour a obligé à
retirer : en plein soleil, il sert de lumière d'appoint. Valeurs typiques en
plein soleil (environ IL 15), Intensité du flash Auto ou 1/1, Filtre ND sur
Auto, avec entre parenthèses les valeurs avec le filtre ND désactivé
lorsqu'elles diffèrent :

| Distance | ISO Auto | ISO 400 fixe | ISO 3200 fixe |
| ---: | --- | --- | --- |
| 0,3 m | f/11.8, ISO 100 | f/9.9 avec ND (f/16, flash trop fort) | f/16 avec ND, encore trop clair (f/16, flash beaucoup trop fort) |
| 1 m | f/3.7, ISO 100 (f/3.5, trop clair) | f/5.9 | f/8.4 avec ND (f/16, flash trop fort) |
| 3 m | f/3.7, ISO 100 (f/3.4, ISO 141, trop clair) | f/5.7 (f/2.8, trop clair) | f/16 (f/5.7, trop clair) |

- Avec le filtre ND **activé** ou **désactivé**, le Mode flash GF-2 fonctionne
  comme en 1.3.0 : l'appareil ne modifie ni la sensibilité ISO ni l'ouverture
  en fonction de la lumière du jour, et un arrière-plan ensoleillé peut être
  trop clair.
- Cette fonction nécessite le filtre ND : elle concerne donc le GR IV standard.
  Le GR IV HDF n'a pas de filtre ND : son firmware considère toujours le filtre
  ND comme désactivé, si bien que rien n'y change.

### Vérifier un fichier de firmware

Avant de copier un fichier de firmware sur une carte :

```sh
python3 gr4_gf2unlock.py check path/to/fwdc248b.bin
```

Cette commande vous indique si le fichier est le 1.11 officiel, la version avec
Mode flash GF-2 créée par cet outil (avec son nombre guide) ou autre chose
(elle reconnaît aussi les fichiers GR4-GF2Unlock 1.0.0 à 1.3.0,
GR4-MonoUnlock et GR4-XPanUnlock).

## Risques

- Votre appareil ne sait pas distinguer un bon fichier de firmware d'un fichier
  endommagé. Ne copiez sur votre carte qu'un fichier écrit par l'outil (ou
  confirmé avec `check`).
- Si une mise à jour est interrompue, ou si un fichier de firmware ne peut pas
  démarrer, l'appareil risque de ne plus pouvoir accéder à la fonction de mise à
  jour, et devrait alors passer par le service après-vente de RICOH. Cela ne
  s'est pas produit lors des tests, mais on ne peut pas l'exclure.
- Revenir au firmware officiel alors que le Mode flash GF-2 est encore
  sélectionné n'a pas été testé. Réglez d'abord une autre option du Mode flash.
- Les données d'étalonnage propres à votre appareil ne sont pas modifiées.

## État des tests

| Élément | État |
| --- | --- |
| Mise à jour acceptée, l'appareil démarre | testé sur un GR IV 1.11 |
| Mode flash GF-2 dans le menu Mode flash | testé sur un GR IV 1.11 |
| Exposition déterminée par la distance de mise au point avec le GF-2 | testé sur un GR IV 1.11 |
| Mode flash GF-2 avec un flash manuel (1.3.0) | vérifié hors ligne ; merci de signaler vos résultats |
| Les flashs P-TTL fonctionnent comme Flash forcé (1.3.0) | vérifié hors ligne ; merci de signaler vos résultats |
| Votre propre nombre guide (`--gn`) | vérifié hors ligne ; merci de signaler vos résultats |
| Sujets proches avec ISO Auto (ouverture exacte) | vérifié hors ligne ; merci de signaler vos résultats |
| Cycles du levier ADJ et de la touche Fn | vérifié hors ligne ; merci de signaler vos résultats |
| Intensité du flash 1/4, ISO fixe, filtre ND, synchro lente | vérifié hors ligne ; merci de signaler vos résultats |
| Pleine lumière avec Filtre ND réglé sur Auto (1.4.0) | vérifié hors ligne ; merci de signaler vos résultats |
| Autres options du Mode flash inchangées | vérifié hors ligne ; merci de signaler vos résultats |
| Revenir au 1.11 officiel restaure entièrement l'appareil | testé avec un firmware modifié antérieur sur un GR IV 1.11 ; pas encore avec cette version |
| L'outil reproduit exactement le firmware de référence | testé |

Les tests sur l'appareil ont été faits avec la version 1.0.0. Depuis, le nombre
guide peut être réglé et les sujets proches en ISO Auto reçoivent l'ouverture
exacte (1.2.0), et le Mode flash GF-2 s'applique aux flashs que l'appareil ne
détecte pas, comme sur le GR III (1.3.0), et Filtre ND réglé sur Auto maintient
une exposition normale en pleine lumière (1.4.0).

## Pour les développeurs

```
GR4-GF2Unlock/
├── README.md           this guide
├── README.*.md         this guide in Japanese, Chinese, Korean, German, French and Spanish
├── gr4_gf2unlock.py    the tool (Python 3.8+, no extra packages)
└── assets/             the icon, and the script that draws it (render_icon.py)
```

| Fichier | SHA-256 |
| --- | --- |
| `fwdc248b.bin` officiel RICOH GR IV 1.11 | `a2f664dfca034059eb0fd6e18ab08684c326b4a034d85c164dad7e1ec9b5655f` |
| `fwdc248b.bin` avec Mode flash GF-2 créé par cet outil (1.4.0, nombre guide 3) | `ab00b2487126b4ab14e4872288970bb4a51f99ef7b56e57356a9603da6778bec` |
| `fwdc248b.bin` avec Mode flash GF-2, version 1.3.0 | `86abac009d3664ede49ef912073d00b8fb15ac7e9867265aecda581c932db41a` |
| `fwdc248b.bin` avec Mode flash GF-2, version 1.2.0 | `225258d201217bac3416de79de94aea4d05c6aab74d4f026c30280ac8a624c22` |
| `fwdc248b.bin` avec Mode flash GF-2, version 1.1.0 | `660df9de1e611325fc41df2e42499028c7296c037201b7fd7be828b813ec1c75` |
| `fwdc248b.bin` avec Mode flash GF-2, version 1.0.0 (GF-2 uniquement) | `45a2edd33a0e0783458b1052ad8b67514f48b45a5db7b47013543eb46d247f0c` |

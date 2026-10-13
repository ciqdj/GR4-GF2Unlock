<p align="center">
  <img src="assets/icon-256.png" width="112" height="112" alt="Icono de GR4-GF2Unlock: un flash GF-2 cuyo haz se atenúa en seis franjas de un paso cada una">
</p>

<h1 align="center">GR4-GF2Unlock</h1>

<p align="center">
  <strong>El GF-2 Flash Mode de la GR III, en tu RICOH GR IV.<br>Enfoca al sujeto; la cámara ajusta la exposición con flash.</strong>
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.zh-CN.md">简体中文</a> |
  <a href="README.zh-TW.md">繁體中文</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.fr.md">Français</a> |
  <strong>Español</strong>
</p>

En el firmware 2.10, RICOH dio a la GR III el **GF-2 Flash Mode**: con el
pequeño flash RICOH GF-2 montado, la cámara dispara el flash a una potencia fija
y calcula la apertura, el ISO y la velocidad de obturación a partir de la
**distancia de enfoque**. La GR IV nunca recibió este modo.

GR4-GF2Unlock lo añade a la GR IV como **quinta opción de Modo flash**, junto a
Flash On, Flash On+ojos rojos, Sinc baja velocidad y Sinc baja vel.+ojos rojos.
Todo lo demás de tu cámara queda exactamente como estaba, y puedes volver al
firmware oficial en cualquier momento.

Este repositorio no contiene ningún firmware de RICOH. Tú mismo descargas el
firmware oficial de RICOH, y la herramienta incluida lo convierte en la versión
GF-2 Flash Mode, en tu propio ordenador.

> [!WARNING]
> **No oficial, bajo tu propia responsabilidad.** No está hecho ni respaldado por RICOH IMAGING.
> Instalar un firmware modificado puede anular la garantía. Lee primero
> [Antes de empezar](#antes-de-empezar) y [Riesgos](#riesgos).

| Quieres | Ve a |
| --- | --- |
| Ver qué ajusta la cámara a cada distancia | [Qué esperar](#qué-esperar) |
| Crear el firmware (macOS, Windows, Linux) | [Crea el firmware](#crea-el-firmware) |
| Usar un flash distinto del GF-2 | [Tu propio flash](#tu-propio-flash) |
| Instalarlo | [Instálalo en la cámara](#instálalo-en-la-cámara) |
| Saber qué contiene un archivo de firmware | [Comprobar un archivo de firmware](#comprobar-un-archivo-de-firmware) |
| Volver al firmware de RICOH | [Volver al firmware oficial](#volver-al-firmware-oficial) |

**Contenido:**
[Cómo funciona](#cómo-funciona) |
[Qué obtienes](#qué-obtienes) |
[Antes de empezar](#antes-de-empezar) |
[Crea el firmware](#crea-el-firmware) |
[Instálalo en la cámara](#instálalo-en-la-cámara) |
[Conviene saber](#conviene-saber) |
[Riesgos](#riesgos) |
[Estado de las pruebas](#estado-de-las-pruebas) |
[Para desarrolladores](#para-desarrolladores)

## Cómo funciona

Con GF-2 Flash Mode seleccionado, la cámara dispara el flash como en Flash On,
pero a una **potencia fija**. Después planifica la exposición como lo hace el
GF-2 Flash Mode de la GR III: a partir del **número guía** del flash y de la
**distancia de enfoque** (con enfoque automático o manual), dentro de los
propios límites de apertura, ISO y sincronización del flash de la GR IV. El
número guía es el del GF-2, 3, salvo que indiques el de tu propio flash al crear
el firmware (consulta [Tu propio flash](#tu-propio-flash)).

- **La potencia:** la cámara ajusta el GF-2 con **Salida del flash**: **Auto o
  1/1** es potencia completa, **1/4** es un cuarto de potencia. Otro flash se
  dispara a la potencia ajustada en el propio flash (consulta
  [Tu propio flash](#tu-propio-flash)).
- **Con ISO Auto,** la cámara abre la apertura y sube el ISO a medida que el
  sujeto se aleja. De cerca, se queda en el ISO más bajo y cierra la apertura
  tanto como lo pida la distancia, hasta f/16.
- **Con un ISO fijo,** la cámara elige la apertura que corresponde a la
  distancia.
- **La velocidad de obturación** sigue la luz que rodea al sujeto. Se mantiene
  dentro de la sincronización del flash, así que el flash siempre sale en la
  foto. La más lenta es 1/32 s, o hasta 32 s con sincronización lenta en un
  lugar oscuro.
- **En Tv, Av y M,** los valores que ajustas quedan anulados, como en la GR III.
- **Con el filtro ND en Auto,** la exposición se mantiene normal con mucha luz.
  Cuando la apertura y la velocidad de obturación no bastan, la cámara baja el
  ISO (ISO Auto), cierra la apertura y después añade el filtro ND (consulta
  [Mucha luz](#mucha-luz-filtro-nd-en-auto)).

Los cálculos de exposición son de la propia RICOH, trasladados del firmware 2.10
de la GR III. Todo lo demás es el firmware oficial de la GR IV, sin cambios.

### Qué esperar

Valores típicos en una habitación con poca luz, Salida del flash en Auto o 1/1,
filtro ND desactivado (el EXIF puede redondearlos ligeramente):

| Distancia | ISO Auto | ISO 400 fijo |
| ---: | --- | --- |
| 0,5 m | f/5.9, ISO 100 | f/11.8 |
| 1 m | f/3.0, ISO 100 | f/5.9 |
| 2 m | f/2.8, ISO 367 | f/3.0 |
| 3 m | f/2.8, ISO 800 | f/2.8 |
| 5 m | f/2.8, ISO 2263 | f/2.8 (sujeto más oscuro: fuera del alcance del flash) |

Con Salida del flash en **1/4**, el ISO es unos dos pasos más alto, o la
apertura unos dos pasos más abierta. Con otro número guía, la apertura escala
con él: número f = número guía × √(ISO / 100) ÷ distancia, dentro de f/2.8–f/16.

> [!TIP]
> **Comprueba que el modo está activo.** Selecciona GF-2 Flash Mode y ajusta el
> modo **M**, **ISO 400** y una velocidad de obturación de 1/2000 s o más lenta.
> Haz una foto de algo a aproximadamente 1 m y después de algo a unos 3 m. La
> apertura cambia sola, a aproximadamente f/5.9 y f/2.8, sea cual sea el valor
> que hayas ajustado.

## Qué obtienes

Después de la instalación, **Modo flash** (en el menú, en la palanca ADJ y en el
botón Fn) ofrece:

| Se muestra como | Qué hace el flash |
| --- | --- |
| Flash On | se dispara en cada foto, como antes |
| Flash On+ojos rojos | como antes |
| Sinc baja velocidad | como antes |
| Sinc baja vel.+ojos rojos | como antes |
| **GF-2 Flash Mode** | **potencia fija; apertura, ISO y velocidad de obturación a partir de la distancia de enfoque** |

- La nueva opción tiene su propio nombre en cada idioma del menú; en español,
  como en inglés, se muestra "GF-2 Flash Mode". Cuando la sincronización lenta
  no está disponible, las opciones son Flash On, Flash On+ojos rojos y GF-2
  Flash Mode.
- Funciona en **P, Tv, Av o M** con el GF-2 y con **cualquier flash que no se
  comunique con la cámara**, por ejemplo un flash manual, como en la GR III. La
  exposición se calcula para el número guía del firmware: el del GF-2 o el de tu
  propio flash (consulta [Tu propio flash](#tu-propio-flash)).
- Con un **flash P-TTL** que se comunica con la cámara, como un flash RICOH o
  PENTAX, GF-2 Flash Mode funciona como Flash On, también como en la GR III.
- El ajuste se conserva al apagar la cámara, como cualquier ajuste de Modo
  flash.
- La pantalla de disparo muestra el icono de **Flash On**, y las fotos registran
  que el flash se ha disparado, como con Flash On.
- **Todas las demás opciones de Modo flash funcionan exactamente como antes**,
  incluida Salida del flash en Auto, 1/1 y 1/4.

### Mejor que el original de la GR III

En torno a los cálculos de exposición de RICOH, la versión para la GR IV
aprovecha hardware que la GR III no tiene y corrige algunos puntos débiles:

| | GR III 2.10 | GR4-GF2Unlock |
| --- | --- | --- |
| Potencia del flash | Solo potencia completa: la GR III no puede controlar el GF-2 | Con el GF-2, potencia completa o un cuarto de potencia (Salida del flash 1/1 o 1/4), con la exposición calculada para cada una |
| Número guía | Siempre 3, el del GF-2 | 3, o el de tu propio flash (de 1 a 90) |
| Sujetos cercanos con ISO Auto | Hasta aproximadamente 1 EV demasiado claros a menos de 0,7 m | La apertura que pide la distancia, hasta f/16 |
| ISO Auto con el filtro ND activado | El fondo sale dos pasos demasiado oscuro | La velocidad de obturación tiene en cuenta el filtro ND, así que el fondo queda bien expuesto |
| Sujetos muy cercanos con mucha luz | Puede pedir f/19, más allá del f/16 del objetivo | Se mantiene dentro de f/2.8–f/16 |
| Mucha luz, filtro ND en Auto | Hasta un paso demasiado clara, y después el filtro ND deja el flash dos pasos por debajo | ISO más bajo, apertura más cerrada y después el filtro ND: la foto queda bien expuesta, y el flash pierde solo la luz que había que quitar |
| Sujetos cercanos, filtro ND en Auto | Demasiado claros incluso a f/16 con un ISO fijo | El filtro ND, con la apertura abierta en consecuencia |
| Sincronización del flash | Puede pedir una velocidad de obturación más rápida que la sincronización del flash | Siempre dentro de la sincronización del flash, que en la GR IV depende de la apertura |
| Todo lo demás | Activar el modo sustituye el comportamiento normal del flash | Una opción de Modo flash entre cinco: vuelve a Flash On y a la salida automática del flash de la GR IV cuando quieras |

Se han comprobado más de 250 000 combinaciones de distancia, ISO, filtro ND,
modo de flash, luz, tipo de flash y número guía (de 1 a 90). Ninguna pide una
apertura fuera de f/2.8–f/16, un ISO fuera de tus límites ni una velocidad de
obturación con la que el flash no pueda sincronizar.

## Antes de empezar

- **Cámara:** RICOH GR IV (el modelo en color estándar). Otros modelos no son
  compatibles.
- **Flash:** RICOH GF-2, o un flash manual cuyo número guía conozcas (consulta
  [Tu propio flash](#tu-propio-flash)). Las demás opciones de Modo flash
  funcionan con todos los flashes como antes.
- **Tu cámara ya debe tener el firmware 1.11.** Comprueba la versión en el menú
  de configuración de la cámara.
  - Versión anterior: actualiza primero a la 1.11 de la forma normal, con el archivo oficial de RICOH.
  - Versión más reciente: **no uses esta herramienta.** Solo es compatible con la 1.11.
- **El archivo de firmware oficial.** En la página oficial de soporte de la GR IV
  de RICOH IMAGING, descarga la **versión de firmware 1.11**. Descomprímela si hace
  falta hasta tener el archivo **`fwdc248b.bin`**.
- **Una batería totalmente cargada.** Una actualización de firmware nunca debe
  quedarse sin alimentación.
- **Una tarjeta SD** que puedas formatear.
- **Un ordenador con Python 3.8 o posterior.** macOS y la mayoría de los sistemas
  Linux ya lo tienen; en Windows, instálalo desde python.org. No hace falta nada
  más.
- Apunta los ajustes personalizados (C1, C2, …) que no quieras tener que volver a configurar.

## Crea el firmware

Abre un terminal en esta carpeta y ejecuta (usa la ruta donde guardaste el
archivo oficial):

```sh
python3 gr4_gf2unlock.py patch ~/Downloads/fwdc248b.bin
```

En Windows:

```bat
py gr4_gf2unlock.py patch C:\Users\you\Downloads\fwdc248b.bin
```

La herramienta comprueba primero que le has dado el archivo oficial 1.11
auténtico. Después crea el firmware GF-2 Flash Mode y lo comprueba. Tarda
aproximadamente un minuto. Cuando todo está bien, termina así:

```
wrote output/fwdc248b.bin  (SHA-256 ab00b2487126b4ab14e4872288970bb4a51f99ef7b56e57356a9603da6778bec)
```

Si algo no está bien, muestra `refused: …` y **no escribe nada**: por ejemplo,
otra versión de firmware, un archivo ya modificado o una descarga dañada.

### Tu propio flash

GF-2 Flash Mode planifica la exposición para el número guía del GF-2, 3. Para
usar otro flash, añade su número guía con `--gn`:

```sh
python3 gr4_gf2unlock.py patch ~/Downloads/fwdc248b.bin --gn 12
```

- **Qué flashes:** cualquier flash que no se comunique con la cámara y se
  dispare desde el contacto central de la zapata: los flashes manuales y la
  mayoría de los flashes hechos para otras marcas de cámaras. Un flash P-TTL, o
  un flash compatible en modo P-TTL, se comunica con la cámara; GF-2 Flash Mode
  funciona entonces como Flash On, como en la GR III.
- Indica el número guía **a ISO 100, en metros**, a potencia completa, según el
  manual del flash. Si el número guía está en pies: divídelo entre 3,3. Con un
  flash con zoom: usa el número guía del zoom con el que disparas.
- Permitido: **de 1 a 90**. La cámara trabaja en pasos de 1/16 de paso de
  diafragma, y la herramienta muestra el valor que usa, por ejemplo
  `guide number: 11.81` para 12.
- **La cámara no puede ajustar la potencia de un flash así.** Pon el flash en
  **potencia manual completa** y Salida del flash en **Auto** o **1/1**. Si en
  cambio pones el flash a 1/4 de potencia, ajusta también Salida del flash en
  **1/4**: la cámara planifica entonces dos pasos menos.
- La herramienta crea primero el firmware estándar y lo comprueba como antes, y
  después cambia solo el número guía. El SHA-256 es entonces distinto del de
  arriba; `check` muestra el número guía de un archivo.
- Para cambiar el número guía, crea el firmware de nuevo e instálalo.

## Instálalo en la cámara

### 1. Cópialo a la tarjeta SD

1. **Formatea la tarjeta SD en la cámara.**
2. Copia **`output/fwdc248b.bin`** en la **raíz** de la tarjeta: no dentro de una
   carpeta, y con el nombre exactamente `fwdc248b.bin`.

### 2. Actualiza la cámara

1. Inserta la batería totalmente cargada y la tarjeta SD.
2. Inicia la actualización de firmware desde el menú de configuración de la cámara,
   como se describe en las instrucciones oficiales de RICOH para actualizar el firmware de la GR IV.
3. **La cámara muestra una actualización de la versión 1.11 a la versión 1.11.** Es
   lo esperado: el firmware GF-2 Flash Mode mantiene el número de versión. Confirma
   la actualización.

> [!CAUTION]
> **No apagues la cámara, no abras la tapa de la batería o de la tarjeta y no
> saques la tarjeta** hasta que la actualización haya terminado y la cámara se haya reiniciado.

### 3. A disparar

1. Con la cámara y el GF-2 **apagados**, desliza el GF-2 hasta el fondo de la
   zapata y después enciende ambos.
2. Menú Ajustes de toma → **Modo flash** → **GF-2 Flash Mode**.
3. Ajusta **Salida del flash** en **Auto** o **1/1** para potencia completa, o
   en **1/4**.
4. Enfoca al sujeto y dispara.

- La versión del firmware sigue mostrando **1.11**. Es normal.
- Borra `fwdc248b.bin` de la tarjeta (o formatéala) para que la actualización no
  se inicie de nuevo por error.

### Volver al firmware oficial

> [!IMPORTANT]
> **Primero ajusta Modo flash a cualquier opción distinta de GF-2 Flash Mode**,
> por ejemplo Flash On. Haz lo mismo en cada modo personalizado (C1, C2, …) que
> lo use. El firmware oficial no tiene el ajuste GF-2 Flash Mode.

Después repite los pasos 1–2 con el `fwdc248b.bin` **oficial** de RICOH. La
cámara vuelve a mostrar **1.11 → 1.11**; confírmalo y tu cámara vuelve a su
estado original.

## Conviene saber

- **Apaga la cámara y el GF-2 antes de montar o retirar el flash**, y empuja el
  GF-2 hasta el fondo de la zapata.
- **La cámara no puede saber si el flash se disparará.** Con GF-2 Flash Mode
  seleccionado, ajusta la exposición para una foto con flash incluso cuando el
  flash está apagado, no está montado o todavía se está cargando. Esa foto
  saldrá demasiado oscura. Lo mismo ocurre en la GR III.
- **Un flash potente de cerca:** cuando el sujeto está tan cerca que incluso
  f/16 al ISO más bajo deja entrar demasiado flash, la cámara añade el filtro ND
  si está en Auto, y abre la apertura en consecuencia. Con el filtro ND
  desactivado, o con un sujeto aún más cerca, la foto sale más clara de lo
  planificado: usa Salida del flash 1/4 o aléjate.
- **ISO fijo y sujetos lejanos:** una vez que la apertura está totalmente
  abierta (f/2.8), un sujeto más lejano sale más oscuro. Sube el ISO o usa ISO
  Auto.
- **Luz de día intensa:** la velocidad de obturación no puede ser más rápida que
  la sincronización del flash (1/2500 s a f/2.8–f/4, 1/4000 s desde f/5.6).
  Consulta [Mucha luz](#mucha-luz-filtro-nd-en-auto) más abajo.
- **Toma continua:** no hay una espera automática a que el flash se recargue, a
  diferencia de la GR III. Deja unos dos segundos entre fotos con flash.
- **AE Prior. dist. inst., B y T, y el vídeo** funcionan como antes. GF-2 Flash
  Mode no se aplica ahí.
- **No se puede combinar con GR4-MonoUnlock ni con GR4-XPanUnlock.** Cada
  herramienta parte del firmware oficial, y esta herramienta rechaza sus
  archivos.
- **Actualizar desde un GR4-GF2Unlock anterior:** instala el archivo nuevo de la
  misma forma. No hace falta volver antes al firmware oficial. Las versiones
  1.1.0 y 1.2.0 aplicaban GF-2 Flash Mode solo a los flashes que la cámara
  detecta, así que no tenía efecto con un flash manual; la 1.3.0 lo corrige. La
  1.4.0 añade el ajuste para mucha luz con el filtro ND en Auto.
- **Una actualización oficial de RICOH elimina GF-2 Flash Mode.** Reemplaza todo
  el firmware. Ajusta antes otra opción de Modo flash (consulta
  [Volver](#volver-al-firmware-oficial)).
- **Solo para la GR IV estándar.** Nunca instales el archivo en otro modelo.
- **Antes de enviar la cámara al servicio técnico,** vuelve al firmware oficial.

### Mucha luz (filtro ND en Auto)

Con mucha luz, la velocidad de obturación llega a la sincronización del flash, y
la apertura que GF-2 Flash Mode eligió para el flash dejaría entrar demasiada
luz de día. Con el **filtro ND en Auto** (menú Ajustes de toma), la cámara
mantiene normal la exposición, en este orden:

1. **ISO Auto:** baja el ISO, hasta tu límite inferior. La apertura no cambia.
2. Cierra la apertura, hasta f/16.
3. Cuando f/16 a la velocidad de sincronización del flash más rápida sigue
   siendo demasiado claro, o el flash por sí solo es demasiado fuerte incluso a
   f/16, añade el **filtro ND** (2 pasos). Después vuelve a abrir la apertura
   tanto como lo permite la luz.

El fondo queda entonces bien expuesto. El flash conserva la potencia
planificada respecto a la exposición, menos solo lo que la luz de día obligó a
quitar: al sol actúa como luz de relleno. Valores típicos al sol (aproximadamente
EV 15), Salida del flash en Auto o 1/1, filtro ND en Auto, con el filtro ND
desactivado entre paréntesis cuando es distinto:

| Distancia | ISO Auto | ISO 400 fijo | ISO 3200 fijo |
| ---: | --- | --- | --- |
| 0,3 m | f/11.8, ISO 100 | f/9.9 con ND (f/16, flash demasiado claro) | f/16 con ND, aún demasiado claro (f/16, flash excesivamente claro) |
| 1 m | f/3.7, ISO 100 (f/3.5, demasiado claro) | f/5.9 | f/8.4 con ND (f/16, flash demasiado claro) |
| 3 m | f/3.7, ISO 100 (f/3.4, ISO 141, demasiado claro) | f/5.7 (f/2.8, demasiado claro) | f/16 (f/5.7, demasiado claro) |

- Con el filtro ND **activado** o **desactivado**, GF-2 Flash Mode funciona como
  en la 1.3.0: la cámara no cambia el ISO ni la apertura por la luz de día, y un
  fondo soleado puede salir demasiado claro.
- Esto necesita el filtro ND, así que se aplica a la GR IV estándar. La GR IV
  HDF no tiene filtro ND: su firmware siempre trata el filtro ND como
  desactivado, así que allí no cambia nada.

### Comprobar un archivo de firmware

Antes de copiar cualquier archivo de firmware a una tarjeta:

```sh
python3 gr4_gf2unlock.py check path/to/fwdc248b.bin
```

Te dice si el archivo es el 1.11 oficial, la versión GF-2 Flash Mode creada por
esta herramienta (con su número guía) u otra cosa (también reconoce los
archivos de GR4-GF2Unlock 1.0.0 a 1.3.0, GR4-MonoUnlock y
GR4-XPanUnlock).

## Riesgos

- Tu cámara no puede distinguir un archivo de firmware bueno de uno dañado. Copia a
  tu tarjeta solo un archivo que haya escrito la herramienta (o que hayas confirmado con `check`).
- Si una actualización se interrumpe, o un archivo de firmware no puede arrancar, puede
  que la cámara ya no llegue a la función de actualización, y entonces necesitaría el
  servicio técnico de RICOH. No ocurrió en las pruebas, pero no se puede descartar.
- Volver al firmware oficial con GF-2 Flash Mode todavía seleccionado no se ha
  probado. Ajusta antes otra opción de Modo flash.
- Los datos de calibración propios de tu cámara no se tocan.

## Estado de las pruebas

| Qué | Estado |
| --- | --- |
| Actualización aceptada, la cámara arranca | probado en una GR IV 1.11 |
| GF-2 Flash Mode en el menú Modo flash | probado en una GR IV 1.11 |
| Exposición a partir de la distancia de enfoque con el GF-2 | probado en una GR IV 1.11 |
| GF-2 Flash Mode con un flash manual (1.3.0) | comprobado sin la cámara; por favor, comunica tus resultados |
| Los flashes P-TTL funcionan como Flash On (1.3.0) | comprobado sin la cámara; por favor, comunica tus resultados |
| Tu propio número guía (`--gn`) | comprobado sin la cámara; por favor, comunica tus resultados |
| Sujetos cercanos con ISO Auto (apertura exacta) | comprobado sin la cámara; por favor, comunica tus resultados |
| Ciclos de la palanca ADJ y del botón Fn | comprobado sin la cámara; por favor, comunica tus resultados |
| Salida del flash 1/4, ISO fijo, filtro ND, sincronización lenta | comprobado sin la cámara; por favor, comunica tus resultados |
| Mucha luz con el filtro ND en Auto (1.4.0) | comprobado sin la cámara; por favor, comunica tus resultados |
| Las demás opciones de Modo flash, sin cambios | comprobado sin la cámara; por favor, comunica tus resultados |
| Volver al 1.11 oficial restablece la cámara por completo | probado con un firmware modificado anterior en una GR IV 1.11; con esta versión aún no |
| La herramienta reproduce exactamente el firmware de referencia | probado |

Las pruebas con la cámara se hicieron con la versión 1.0.0. Desde entonces, se
puede fijar el número guía y los sujetos cercanos con ISO Auto reciben la
apertura exacta (1.2.0), y GF-2 Flash Mode se aplica a los flashes que la cámara
no detecta, como en la GR III (1.3.0), y el filtro ND en Auto mantiene normal la
exposición con mucha luz (1.4.0).

## Para desarrolladores

```
GR4-GF2Unlock/
├── README.md           this guide
├── README.*.md         this guide in Japanese, Chinese, Korean, German, French and Spanish
├── gr4_gf2unlock.py    the tool (Python 3.8+, no extra packages)
└── assets/             the icon, and the script that draws it (render_icon.py)
```

| Archivo | SHA-256 |
| --- | --- |
| `fwdc248b.bin` oficial de RICOH GR IV 1.11 | `a2f664dfca034059eb0fd6e18ab08684c326b4a034d85c164dad7e1ec9b5655f` |
| `fwdc248b.bin` GF-2 Flash Mode creado por esta herramienta (1.4.0, número guía 3) | `ab00b2487126b4ab14e4872288970bb4a51f99ef7b56e57356a9603da6778bec` |
| `fwdc248b.bin` GF-2 Flash Mode, versión 1.3.0 | `86abac009d3664ede49ef912073d00b8fb15ac7e9867265aecda581c932db41a` |
| `fwdc248b.bin` GF-2 Flash Mode, versión 1.2.0 | `225258d201217bac3416de79de94aea4d05c6aab74d4f026c30280ac8a624c22` |
| `fwdc248b.bin` GF-2 Flash Mode, versión 1.1.0 | `660df9de1e611325fc41df2e42499028c7296c037201b7fd7be828b813ec1c75` |
| `fwdc248b.bin` GF-2 Flash Mode, versión 1.0.0 (solo GF-2) | `45a2edd33a0e0783458b1052ad8b67514f48b45a5db7b47013543eb46d247f0c` |

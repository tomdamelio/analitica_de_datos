---
name: slides-html
description: Arma un deck de diapositivas como un HTML/CSS/JS autocontenido y offline (un solo archivo, sin reveal.js ni frameworks), con navegacion por teclado, pie de pagina con progreso por seccion, y widgets interactivos reales (rotar una recta, un plano 3D, un biplot, comparar metodos, revelar una formula termino a termino) en vez de solo texto y figuras estaticas. Es la version HTML de la skill /slides (que arma Beamer/PDF) — misma logica colaborativa slide-por-slide, pero para cuando el usuario quiere algo que se abre en un navegador, con animaciones/interaccion real, o que va a vivir en una pagina web. Usar esta skill cuando el usuario pida "diapositivas en HTML", "slides interactivas", "una clase con un grafico que se pueda mover/rotar/explorar", "algo como reveal.js pero simple", o cuando pida agregar interaccion (arrastrar, clickear, animar) a una diapositiva ya existente de este tipo. Triggers: /slides-html, "armar diapositivas HTML", "slides interactivas", "presentacion en HTML para el navegador".
---

# Skill: slides-html

Construye, **junto con el usuario y slide por slide**, un deck de diapositivas HTML/CSS/JS
autocontenido (un solo archivo, abrible con doble-click, sin conexion a internet) a partir de:
1. un **texto fuente** (el mensaje, el temario, las conclusiones que se quieren comunicar), y
2. **datos reales** cuando la clase necesita numeros o widgets interactivos (nunca se inventan
   valores: se precomputan una vez desde el dataset real y todo — texto, figuras, widgets — lee de ahi).

El usuario marca el ritmo: armas una slide (o un bloque chico) y PARAS a que la revise; el usuario
pide ajustes puntuales; cuando esta conforme, seguis con la proxima. Esto nacio armando la Clase 10
(reduccion de dimensionalidad / PCA) de un curso de Analitica de Datos — ese deck es el ejemplo de
referencia con el que se calibraron todas las convenciones de este documento.

> **Relacion con `/slides`:** misma filosofia colaborativa y misma idea de "un color por bloque
> tematico + footer con progreso", pero la salida es HTML puro para navegador (no LaTeX/Beamer/PDF).
> Elegir esta cuando el usuario quiere algo que corra en un browser, con **interaccion real**
> (arrastrar, clickear, animar) — no solo pasar paginas.

## Ejemplo de referencia real: la Clase 10

`clases/clase-10/slides-html/` (en la raiz de este mismo repo) es el deck COMPLETO del que salio
esta skill — no un ejemplo sintetico, es una clase real ya dictada, con los 50 slides, los 5 widgets
en uso con datos reales, y todos los gotchas de este documento ya resueltos ahi mismo. Frente a
`assets/` (starter kit generico, pensado para copiar y adaptar a cualquier proyecto), esta carpeta es
el **modelo a imitar** cuando se arma una clase nueva de ESTE curso — mirar ahi primero, no solo los
templates genericos de `assets/`:

| Si necesitas... | Mirar en clase-10/slides-html/ |
|---|---|
| Como se ve una clase completa armada (30-50 slides, todos los bloques) | `contenido_apertura.py` -> `contenido_bloque1.py` ... `contenido_cierre.py`, en ese orden |
| La paleta y el chrome ya afinados para ESTE curso (UdeSA) | `comun.py` (colores, logo, `SECCIONES`) — reusar tal cual, no reinventar |
| Un widget de rotar/3D/biplot/comparador/formula-por-pasos ya andando con datos reales | `interactivos.py` + `datos.py` en `../slides-beanim/` (de donde saca los numeros) |
| Como se precomputan los datos de un curso real (nunca inventados) | `../slides-beanim/datos.py` — un JSON, todo el deck lee de ahi |
| Como quedo el resultado final, para abrir y ver antes de empezar | `clase10_estatica_completa.html` (el deck ya generado, abrible directo) |

Para otra clase de este mismo curso, el flujo mas rapido es: copiar `comun.py` de clase-10 (ya tiene
la identidad visual correcta, no hace falta re-derivarla), y usar sus `contenido_*.py` como plantilla
de ESTRUCTURA (no de contenido) — mismo patron de portada/bloques/cierre, temario distinto. Para un
proyecto FUERA de este curso (sin identidad UdeSA), usar en cambio el starter kit neutro de `assets/`.

---

## Por que HTML/JS vanilla y no reveal.js / PowerPoint online / etc.

Se probo primero generar las mismas diapositivas como video Manim (con `manim-slides`). Funcionaba,
pero cada slide "animada" exigia escribir coreografia imperativa y la unica forma de validar un
cambio era **renderizar video de nuevo** (lento, sin preview en vivo). Pasar a HTML/CSS/JS estatico
da preview instantaneo (F5) y separa dos cosas que en Manim quedaban mezcladas: el **chrome** (titulo,
logo, pie de pagina — siempre igual, sea la slide estatica o interactiva) del **contenido** (texto
estatico O un widget JS). Nunca dos motores de render dibujando el mismo elemento de chrome — eso
garantiza cero drift visual entre una slide con texto y una con un grafico interactivo al lado.

No se usa reveal.js ni ninguna libreria de slides: el motor de navegacion (mostrar/ocultar `<section
class="slide">`, flechas de teclado, pie de progreso) son ~30 lineas de JS vanilla, mas simples de
entender y de debuggear que aprender la API de un framework para un deck que en general es chico
(30-50 slides) y no necesita transiciones entre slides (los overlays/fragments de reveal.js SI hacen
falta *dentro* de una slide para revelar terminos de una formula — eso se resuelve con el patron de
`widget_formula_pasos`, ver `references/widgets.md`).

---

## Arquitectura del deck (leer `references/arquitectura.md` para el detalle completo)

Un deck se organiza en estos archivos, todos Python que **generan** el HTML final (no se edita HTML
a mano):

```
mi-clase/
├── comun.py              # chrome: paleta, CSS, JS de navegacion, helpers (slide(), caja(), ...)
├── interactivos.py       # widgets reusables (rotar, 3D, biplot, comparador, formula-por-pasos)
├── datos.py              # UNA VEZ: precomputa todos los numeros reales a un JSON (fuente de verdad)
├── contenido_bloqueN.py  # una lista SLIDES por bloque tematico; corrible solo (preview de ese bloque)
├── build_todo.py         # concatena todos los bloques en el HTML final autocontenido
├── _katex_inline.py      # KaTeX embebido offline (generado una vez con scripts/embed_libs.py)
└── _plotly_inline.py     # Plotly embebido offline (idem, solo si hay widgets 3D o de tipo biplot)
```

Puntos que **no son negociables** porque ya causaron bugs reales (ver `references/arquitectura.md`
para el porque exacto de cada uno):
- El **orden de los `<script>`** en el HTML final importa: cualquier libreria externa (Plotly) va
  **antes** del `<div id="deck">`; KaTeX va **al final** (para no demorar el primer paint) — lo que
  implica que un widget que llama `katex.render()` en su propio script inline NO puede asumir que
  `katex` ya existe; tiene que esperar a `DOMContentLoaded`.
- El **tamano del deck** se calcula con `min(96vw, 96vh*16/9)` (no solo `vw`), y el `font-size` de
  las slides con la MISMA formula escalada — si no, una ventana mas "corta" que ancha (comun: barra
  de direcciones/pestanas del navegador comiendose alto) corta el deck arriba/abajo.
- Un widget de Plotly dentro de una slide oculta (`display:none` hasta que se activa) mide ancho 0 en
  el momento en que corre su script — hace falta un `ResizeObserver` que fuerce el resize cuando la
  slide se vuelve visible, si no, Plotly cae a su tamano por defecto (700x450) en la esquina.

---

## El loop colaborativo (igual espiritu que `/slides`)

1. **Setup inicial** — preguntar (o inferir) lo que hace falta para arrancar (ver mas abajo), copiar
   `assets/comun.py`, `assets/interactivos.py`, `assets/build_todo.py` a la carpeta de salida y
   adaptar la paleta/logo/secciones. Si la clase necesita numeros reales o widgets con datos, escribir
   `datos.py` primero (ver `references/arquitectura.md#datos`).
2. **Outline** — proponer el arbol de bloques -> slides (que bloques, cuantas slides cada uno, cuales
   ameritan un widget interactivo en vez de texto/figura estatica) y confirmarlo con el usuario.
3. **Bloque por bloque** — escribir `contenido_bloqueN.py`, correrlo solo (`python contenido_bloqueN.py`
   genera un preview de ESE bloque nada mas — mucho mas rapido para iterar que regenerar los 50),
   revisar con captura (ver Testing abajo), PARAR y esperar ajustes del usuario.
4. **Widgets** — cuando una slide amerita interaccion real (ver criterio abajo), elegir el patron que
   corresponda de `references/widgets.md` en vez de escribir uno desde cero: los 5 patrones ahi ya
   resolvieron los bugs de timing/tamano/superposicion mas comunes.
5. **Ensamblar** — `build_todo.py` junta todos los bloques; correrlo despues de cada tanda de cambios
   y volver a mostrar el resultado combinado antes de dar por cerrado un bloque.
6. **Verificar de verdad** — ver la seccion Testing: una captura headless sola NO alcanza para nada
   que dependa de tiempo (animaciones, transiciones CSS, teclas) — hace falta un navegador real.

### Cuando una slide amerita un widget interactivo (y cuando NO)

Igual que en `/slides` "una idea por slide, el plot manda" — aca el equivalente es "si mover/clickear
ALGO enseña algo que una imagen fija no puede, es candidato a widget; si no, es una figura estatica
mas rapida de generar y mas liviana". Buenas señales de que SI amerita interaccion:
- Comparar la MISMA data bajo transformaciones distintas (rotar un eje, cambiar de metodo) — ver
  al usuario cambiar el parametro y observar qué se mueve es el punto pedagogico.
- Una formula con varios simbolos que se explican de a uno — revelarlos en el momento en que se
  los nombra ancla mejor que tenerlos todos juntos con una lista de bullets aparte.
- Una nube de puntos en 3D donde rotar con el mouse ayuda a ver la estructura.

Malas señales (no vale la pena la complejidad de un widget):
- La slide es solo texto/bullets sin geometria de por medio.
- El "movimiento" no cambiaria la interpretacion (decoracion, no explicacion).

---

## Setup inicial: que preguntar si no esta claro

0. **¿Es una clase de este mismo curso (Analitica de Datos, UdeSA)?** Si si, arrancar copiando
   `clases/clase-10/slides-html/comun.py` (no `assets/comun.py`) — ya tiene la identidad visual, el
   logo y la estructura de `SECCIONES` correctas para este curso, y mirar sus `contenido_*.py` como
   modelo de estructura (ver la seccion "Ejemplo de referencia real" mas arriba). Solo usar el
   starter kit generico de `assets/` para un proyecto SIN relacion con este curso.
1. **Texto/temario fuente**: que se quiere comunicar, en que orden, cuantos bloques tematicos.
2. **Datos**: si la clase usa un dataset real, donde esta y que columnas/variables importan (para
   escribir `datos.py`); si no hay datos (charla puramente conceptual), se puede saltar ese paso.
3. **Identidad visual**: si el usuario no pide otra cosa, usar de arranque la paleta/tipografia de
   `assets/comun.py` (Helvetica, paleta AZUL/NARANJA/VERDE/VIOLETA/ROJO/MARRON + NAVY/TINTA de fondo,
   un color por bloque) — es un default ya probado, no un placeholder a medio hacer. Cambiar los
   colores si el usuario tiene identidad institucional propia.
4. **Logo (si aplica)**: hay DOS variantes, no una — `LOGO_B64` (chico, esquina superior derecha de
   TODAS las slides de contenido) y `LOGO_COLOR_B64` (grande, a todo color, SOLO en la portada). Si
   el usuario da un logo, pedir/generar las dos variantes (o al menos confirmar con el usuario si
   quiere una sola). Un error facil de cometer: setear una sola y asumir que ya esta cubierto — el
   resultado es un deck con logo en la portada pero sin marca en ninguna otra slide, o viceversa.
5. **Apertura y cierre**: NO se arman con `slide()` de la misma forma que el resto — ver
   `assets/ejemplo_apertura_cierre.py` para el patron completo (portada armada a mano, sin el
   chrome generico; resto de la apertura y el cierre con `slide(..., bloque=None, ...)` para heredar
   el color NAVY institucional en vez de un color de bloque). Repasar este archivo de ejemplo ANTES
   de escribir `contenido_apertura.py`/`contenido_cierre.py` reales, y mostrarle al usuario un
   preview de la portada y de la ultima slide en particular — son las dos que mas fijan la primera
   impresion y las que mas facil quedan con un detalle fuera de lugar (logo faltante, chrome que no
   deberia estar ahi) si se generan sin mirar el ejemplo.
6. **Carpeta de salida** del deck (`slides-html/` en el cwd salvo que el usuario indique otra).
7. **¿Hace falta KaTeX y/o Plotly?** Si hay formulas -> KaTeX; si hay widgets 3D o tipo biplot ->
   Plotly. Ambos se embeben offline una sola vez con `scripts/embed_libs.py` (pide permiso antes de
   descargar, ver esa seccion).

---

## Testing: la trampa de las capturas headless

**Cualquier cosa que dependa de tiempo real** (una animacion con `requestAnimationFrame`, una
transicion CSS, una tecla que dispara un cambio) **no se puede validar confiablemente con una captura
headless en modo `--virtual-time-budget`**: ese modo no simula bien el paso de tiempo real entre
frames, y una animacion que en un navegador de verdad se ve perfecta puede aparecer "congelada" o "a
mitad de camino" en la captura — un falso negativo. Ya paso varias veces en el desarrollo de este
patron: no repetir el error de reportar "esta roto" (o "esta arreglado") solo en base a una captura
headless cuando hay timing de por medio.

Regla practica:
- **Layout/tamano/centrado estatico** -> headless Edge (`msedge --headless=new --disable-gpu
  --screenshot=... --virtual-time-budget=4000 file:///.../deck.html?slide=N`) alcanza y es rapido.
  Usar `?slide=N` para saltar directo a la slide que se esta iterando.
- **Cualquier interaccion (click, tecla, animacion, transicion)** -> levantar un server local
  (`python -m http.server`) y usar el navegador real vía la extension de Chrome (el motor headless
  no puede abrir `file://`, por eso el server), click/tecla real, esperar ~1s, RECIEN AHI capturar.
- **Medir centrado con precision** -> no confiar en el ojo. Usar PIL/numpy sobre una captura (contar
  columnas de pixeles no-blancos dentro del area conocida del deck) o, mejor, inyectar un script de
  debug que imprima `getBoundingClientRect()` de los elementos en cuestion. Un caso real de esta
  clase: un plano 3D "se veia corrido" — la causa real no era el centrado del contenedor (que ya
  estaba bien) sino que Plotly renderizaba a su tamano por defecto (700x450) porque el contenedor
  estaba oculto (`display:none`) en el momento del render; sin medir el tamano real del SVG/canvas
  generado, ese diagnostico no habria salido nunca.

Ver `references/testing.md` para los comandos exactos y mas casos resueltos.

---

## Estilo y paleta (default, ajustable)

Paleta institucional de referencia (definida en `assets/comun.py`, cambiar si el usuario tiene la suya):

| Nombre | Hex | Uso |
|---|---|---|
| NAVY | `#00529B` | apertura/cierre, links |
| AZUL | `#3182BD` | bloque 1 |
| NARANJA | `#E6550D` | bloque 2 |
| VERDE | `#31A354` | bloque 3 |
| VIOLETA | `#756BB1` | bloque 4 |
| ROJO | `#CB181D` | bloque 5, alertas |
| MARRON | `#8C6D31` | bloque 6 |
| GRIS / GRIS_CLARO | `#636363` / `#969696` | texto secundario, pie de pagina |
| TINTA | `#122535` | texto principal |

Reglas de uso que ya se decantaron con feedback real del usuario:
- **Un color por bloque tematico** (`COLOR_BLOQUE`), usado en el titulo de cada slide de ese bloque,
  en `alert()` (resaltar una palabra clave) y en las cajas (`caja()`).
- Cuando un widget necesita **varios colores distintos a la vez** (p.ej. cada simbolo de una formula,
  o cada variable de un biplot), **no reusar el color del bloque para ninguno de ellos** — el usuario
  ya lo usa en otro lado de la misma slide (titulo, `alert()`) y reusarlo para un termino especifico
  genera ambiguedad de "¿este color es el bloque o es este termino puntual?". Elegir colores de la
  paleta que el bloque actual no este usando.
- Tipografia: Helvetica Neue / Helvetica / Arial, sans-serif, sin excepciones (ni para codigo: no hay
  bloques de codigo en este tipo de deck; si hiciera falta, usar una monoespaciada consistente).
- Pie de pagina: circulos agrupados por seccion, la seccion actual en color y con los circulos hasta
  la slide actual **rellenos** (el resto de esa seccion hueco), las demas secciones en gris hueco.
  Sin numero de pagina. La apertura (antes de la primera seccion) no tiene pie.

---

## Vocabulario de pedidos por-slide (lo que el usuario tipicamente pide)

- "que se vea el grafico mas grande / no tan chico" -> revisar el tamano REAL renderizado (no el
  CSS declarado — ver el gotcha de Plotly en slide oculta), y el aspect-ratio del contenedor si es 3D.
- "que la formula se vaya revelando / explicando de a poco" -> `widget_formula_pasos` (ver
  `references/widgets.md`), con flechas de teclado, no un boton (asi lo prefirio el usuario: las
  flechas ya son la forma de avanzar de diapositiva, es consistente).
- "que se pueda comparar A vs B vs C" -> patron comparador de metodos (botones + animacion de
  posicion, mismos puntos reacomodandose) en vez de 3 imagenes separadas.
- "los nombres/etiquetas se pisan" -> el problema casi siempre es que dos puntos/vectores caen muy
  cerca; usar el patron de relajacion de etiquetas (`references/widgets.md`, dentro de `widget_biplot`)
  en vez de mover a mano cada una.
- "se corta en los bordes / arriba / costados" -> primero chequear si es el widget (outliers fuera del
  viewBox — comprimir la cola con una funcion suave, no un clip duro que apila puntos en el borde) o
  el deck entero (formula de tamano de ventana, ver arriba).
- "quiero que sea la skill de esto" -> exactamente lo que generó este documento.

---

## Referencias

- `references/arquitectura.md` — estructura de archivos en detalle, orden de scripts, formula de
  tamano del deck, patron de datos.py, CSS del chrome completo explicado.
- `references/widgets.md` — los 5 patrones de widget interactivo (rotar, 3D, biplot con
  anti-superposicion de etiquetas, comparador de metodos animado, formula-por-pasos con flechas de
  teclado) con codigo completo y cuando usar cada uno.
- `references/testing.md` — comandos exactos de testing headless vs navegador real, medicion de
  centrado por pixeles, lista de gotchas ya resueltos para no repetirlos.
- `clases/clase-10/slides-html/` (en la raiz del repo, fuera de esta skill) — el deck REAL completo
  del que salio todo este documento. Ver la seccion "Ejemplo de referencia real" mas arriba.

## Assets (starter kit, copiar y adaptar)

- `assets/comun.py` — chrome completo: paleta, CSS, JS de navegacion + hook de teclado para widgets,
  helpers de contenido (`slide`, `caja`, `bullets`, `numerada`, `nota`, `alert`, `ecuacion`, `tabla`,
  `figura`, `colab_linea`, `slide_notebook`).
- `assets/interactivos.py` — los 5 widgets, generalizados para recibir los datos por parametro (no
  atados al dataset de ninguna clase puntual).
- `assets/build_todo.py` — template para concatenar bloques en el deck final.
- `assets/ejemplo_contenido_bloque.py` — un bloque de ejemplo mostrando el uso de cada helper y widget.
- `assets/ejemplo_apertura_cierre.py` — el patron de portada (armada a mano, con `LOGO_COLOR_B64`) y
  cierre (bloque=None -> NAVY, ultima slide sin logo chico) — leer ANTES de escribir la apertura/
  cierre reales, no improvisar esa estructura desde `slide()` solo.
- `scripts/embed_libs.py` — descarga y empaqueta KaTeX/Plotly offline (con permiso explicito antes de
  bajar nada, ver el script).

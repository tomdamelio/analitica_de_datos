# Patrones de widgets interactivos

Cinco patrones ya probados, cada uno resolviendo una clase de problema pedagogico distinta. El
codigo completo de cada uno vive en `assets/interactivos.py` (generalizado para recibir datos por
parametro); este documento explica **cuando usar cada uno** y **por que esta hecho asi** — la parte
que no es obvia mirando solo el codigo.

Regla general de todos: reciben el color a usar como parametro (nunca hardcodean un color), y reciben
los datos ya precomputados (nunca llaman a pandas/sklearn ni tocan un CSV — eso lo hizo `datos.py`).

## 1. Recta girando — comparar dos definiciones equivalentes en vivo

**Cuando usarlo:** cuando dos cantidades (ej. varianza capturada / error de proyeccion) se mueven en
sentidos opuestos a medida que un parametro cambia, y el punto pedagogico es "llegan a su optimo en
el MISMO valor del parametro" — verlo pasar en vivo convence mas que dos numeros estaticos.

**Como esta hecho:** SVG + JS vanilla (nada de librerias — es solo geometria 2D). Un slider (`<input
type="range">`) mueve un angulo; un boton "▶ Girar" anima el slider solo con `requestAnimationFrame`
interpolando el angulo en el tiempo. En cada frame, se recalculan posiciones proyectadas (geometria
simple) y se leen valores de **curvas precomputadas** (`datos.angulos/varianza/error`, calculadas una
vez en `datos.py`) por interpolacion lineal — nunca se recalcula el modelo en el navegador.

```python
widget_recta_girando(color_bloque, datos, id_="recta1")
# datos = {"puntos": [[x,y],...], "target": [...], "colores": {grupo: hex},
#          "angulos": [...], "varianza": [...], "error": [...]}
```

Puntos clave del JS: la animacion usa `performance.now()` + `requestAnimationFrame`, con una
`duracion` fija y `t = min(1, (ahora-inicio)/duracion)` — el patron estandar para animar cualquier
cosa en el tiempo sin depender de la tasa de refresco del navegador.

## 2. Plano 3D — estructura que solo se aprecia rotando

**Cuando usarlo:** cuando una nube de puntos en 3D tiene una estructura (un plano, un cluster) que
se entiende mejor rotando con el mouse que con una camara que orbita sola en un video.

**Como esta hecho:** Plotly (`scatter3d` + `surface` + `lines` para los ejes/vectores destacados).

```python
widget_plano_3d(color_bloque, datos, id_="plano1")
# datos = {"puntos": [[x,y,z],...], "vector1": [vx,vy,vz], "vector2": [...], "etiquetas": [ex,ey,ez]}
```

**Gotcha critico (ya paso, no repetir):** el `<div>` del plot vive dentro de una `.slide` que tiene
`display:none` hasta que se activa. En el momento en que el script del widget corre (durante el
parseo inicial del HTML), ese div mide ancho/alto **0**, y `Plotly.newPlot()` sin `width`/`height`
explicitos cae a su tamano por defecto (700×450px) anclado en la esquina superior izquierda — **no**
al tamano real del contenedor CSS. Esto se ve como "el grafico quedo chico y corrido a la izquierda"
y es tentador (pero incorrecto) diagnosticarlo como un problema de centrado CSS. La solucion real:

```js
new ResizeObserver(() => {
    const w = contenedor.clientWidth, h = contenedor.clientHeight;
    if (w > 0 && h > 0) Plotly.relayout("plot3d-ID", {width: w, height: h});
}).observe(contenedor);
```

El `ResizeObserver` dispara cuando la slide se activa (el contenedor pasa de 0×0 a su tamano real) y
fuerza a Plotly a re-layoutear con las dimensiones correctas.

**Segundo gotcha: el aspect-ratio del contenedor tiene que matchear la camara.** Una camara 3D
(`camera.eye`) esta "calibrada" para verse bien en cierta proporcion ancho/alto del lienzo; si el
contenedor es muy panoramico (ancho pero bajo), el cubo/escena queda chico dentro de mucho espacio
vacio en vez de llenar el cuadro, sin importar cuanto se agrande el contenedor. Solucion: elegir un
tamano de contenedor con una proporcion parecida a la que tenia cuando se afino la camara (en este
caso, ~1.55:1, similar al 700×450 por defecto de Plotly) en vez de estirarlo a lo panoramico.

## 3. Biplot — scores + loadings con anti-superposicion de etiquetas

**Cuando usarlo:** el patron clasico de biplot (PCA u otro metodo de reduccion): puntos coloreados
por grupo + flechas de variables/loadings, con leyenda clickeable para aislar un grupo.

**Como esta hecho:** Plotly `scatter` (una traza por grupo, para que la leyenda sea togglable) +
anotaciones tipo flecha para los loadings.

```python
widget_biplot(color_bloque, datos, id_="biplot1")
# datos = {"grupos": {grupo: [[x,y],...]}, "orden": [...], "colores": {...}, "etiquetas_grupo": {...},
#          "loadings": [[nombre, x, y], ...], "eje_x": "PC1 (54%)", "eje_y": "PC2 (17%)"}
```

**Gotcha 1: leyenda propia, no la de Plotly.** La leyenda nativa de Plotly se posiciona en
coordenadas de "paper" que pueden caer FUERA del div declarado, tapando texto de la slide que esta
debajo. Se arma una leyenda HTML aparte (`showlegend:false` en el layout) y el toggle se hace a mano
con `Plotly.restyle(id, {visible: "legendonly"}, [indice])` al clickear cada item.

**Gotcha 2 (el mas sutil): las etiquetas de los loadings se superponen si dos variables tienen
direccion/magnitud parecida.** Poner el nombre justo en la punta de la flecha funciona hasta que dos
flechas casi coinciden (comun: dos versiones de "la misma" variable medida en momentos distintos) —
ahi los textos quedan literalmente encimados e ilegibles. La solucion NO es un clic manual por
etiqueta; es una relajacion tipo resorte, corrida una vez en Python al armar los datos (no en el
navegador):

```python
etiquetas_pos = puntas * 1.22   # arrancar un poco mas alla de la punta real
minimo = 0.62                    # distancia minima aceptable entre dos etiquetas
for _ in range(400):
    movido = False
    for i in range(len(etiquetas_pos)):
        for j in range(i + 1, len(etiquetas_pos)):
            diff = etiquetas_pos[i] - etiquetas_pos[j]
            dist = np.linalg.norm(diff)
            if 1e-6 < dist < minimo:
                empuje = diff / dist * (minimo - dist) * 0.5
                etiquetas_pos[i] += empuje
                etiquetas_pos[j] -= empuje
                movido = True
    if not movido:
        break
```

Las flechas se dibujan hasta la punta REAL (sin texto); las etiquetas van en la posicion YA separada;
y si una etiqueta termino lejos de su punta real (mas de cierto umbral), se agrega una linea guia
punteada fina entre la punta y el texto para que quede claro a que flecha corresponde. Este mismo
truco (relajar, no clipear/mover a mano) sirve para cualquier grafico con anotaciones que puedan
superponerse.

## 4. Comparador de metodos — la MISMA data bajo transformaciones distintas, animada

**Cuando usarlo:** cuando se quiere comparar 2+ metodos/vistas de los mismos datos (p.ej. PCA lineal
vs. metodos no lineales) y el punto pedagogico es "son los MISMOS puntos, solo reacomodados" —
animar la transicion entre layouts lo demuestra de forma mucho mas convincente que 3 imagenes
estaticas lado a lado, porque el ojo puede seguir a un punto individual reacomodarse.

**Como esta hecho:** SVG + JS vanilla otra vez (no Plotly — no hace falta zoom/pan real, y esto evita
el gotcha de tamano-en-slide-oculta). Botones (uno por metodo/vista); al clickear, cada punto anima
su posicion `(x,y)` desde la capa actual hacia la capa destino con easing, usando el mismo patron
`requestAnimationFrame` + `performance.now()` del widget 1.

```python
widget_comparador_metodos(color_bloque, datos, id_="comparador1")
# datos = {"target": [...], "colores": {...}, "capas": {clave: [[x,y],...]}, "metodos": [(clave,label),...]}
```

**Gotcha: outliers que se salen del cuadro.** Si cada capa se normaliza independientemente (p.ej.
por percentil, para que la nube central se vea bien distribuida), un pequeño porcentaje de puntos
puede terminar fuera del `viewBox` — invisibles, "se pierden". Un clip duro (`Math.max/min` a un
limite) los apila a todos en una linea recta exactamente sobre el borde, lo cual se ve como un bug.
La solucion es comprimir la cola de forma suave y asintotica, no cortarla:

```python
def normalizar(emb):
    e = emb - emb.mean(axis=0)
    esc = np.percentile(np.abs(e), 96)
    e = e / esc * 3.0
    umbral, limite = 3.0, 3.4
    ax = np.abs(e)
    extra = np.maximum(ax - umbral, 0)
    comprimido = umbral + (limite - umbral) * (1 - np.exp(-extra / (limite - umbral)))
    return np.sign(e) * np.minimum(ax, comprimido)
```

Todo punto queda dentro de `[-limite, limite]`, pero los que estaban muy lejos se acercan al borde de
forma continua (cada uno a una distancia ligeramente distinta) en vez de apilarse todos en el mismo
valor exacto.

## 5. Formula por pasos — revelar y explicar termino a termino

**Cuando usarlo:** una formula con 2+ grupos de simbolos que conviene explicar de a uno (en vez de
tirar la formula completa + una lista de bullets aparte, sin conexion visual entre cada bullet y la
parte de la formula que describe).

**Como esta hecho:** KaTeX con `\htmlClass{grupo-NOMBRE}{...}` envolviendo cada grupo de simbolos en
el TeX (requiere `trust: true` en las opciones de render — es contenido propio, no input de usuario,
asi que es seguro). Un click (o, en este deck, la flecha de teclado — ver el hook en
`references/arquitectura.md`) avanza un contador `paso`; en cada paso se colorea el grupo
correspondiente y se revela (fade-in) el bullet que lo explica, **acumulando** los anteriores (no
reemplazando) para que al final se vea la formula entera coloreada y todas las explicaciones juntas.

```python
widget_formula_pasos(
    formula_tex=r"\htmlClass{grupo-a}{a} + \htmlClass{grupo-b}{b} = \htmlClass{grupo-c}{c}",
    pasos=[
        ("a", "#31A354", 'aca se explica $\\textcolor{#31A354}{a}$ ...'),
        ("b", "#3182BD", 'aca se explica $\\textcolor{#3182BD}{b}$ ...'),
        ("c", "#756BB1", 'aca se explica $\\textcolor{#756BB1}{c}$ ...'),
    ],
    id_="formula1",
)
```

**Detalle clave: colores DISTINTOS por grupo (no todos el color del bloque).** Si la formula tiene 3+
grupos y todos se colorean igual al revelarse, se pierde la distincion visual que es todo el punto
del ejercicio. Elegir un color de la paleta por grupo, evitando el color del bloque actual (que ya
se usa en otro lado de la misma slide vía `alert()`/titulo, y reusarlo ahi generaria ambiguedad).

**Detalle clave 2: el texto de abajo tiene que usar el MISMO color, no solo el concepto.** No alcanza
con explicar "esto es el termino b" en texto negro — la palabra o simbolo que refiere al termino
tiene que estar coloreada igual que en la formula, para que el ojo conecte formula <-> explicacion
sin leer. Como el bullet es texto que pasa por el auto-render global de KaTeX (`$...$`), el color se
hornea directo en el TeX de ESE bullet con `\textcolor{hex}{...}` (dos argumentos — **no** `\color{
hex}` de un solo argumento, que en KaTeX afecta "el resto del grupo actual" y puede dar resultados
inesperados si hay algo despues en el mismo `$...$`).

**Por que flechas de teclado y no un boton propio:** en este deck, avanzar con la flecha derecha es
ya la forma de "pasar de pagina"; usar la misma tecla para "revelar el siguiente termino" (y solo
avanzar de verdad de diapositiva cuando ya no queda nada por revelar) es mas consistente que tener un
boton aparte, y evita que el usuario tenga que ir a buscar un elemento especifico con el mouse en
medio de dar una clase. Ver el hook de registro (`window.__fpAvanzar`) en `references/arquitectura.md`.

---

## Verificar un widget nuevo (checklist rapida)

1. **¿Depende de Plotly?** -> agregar el `ResizeObserver` de resize-on-activate (patron 2/3), sin
   excepcion, aunque "en el momento de probarlo" ya funcione (podria estar en la primera slide,
   visible desde el arranque — el bug aparece en cualquier OTRA posicion).
2. **¿Tiene animacion (rAF) o transicion CSS?** -> probarlo en un navegador real (server local +
   extension), NO solo con captura headless (ver `references/testing.md`).
3. **¿Tiene texto/anotaciones que podrian superponerse con datos reales (no solo el ejemplo de
   prueba)?** -> correr la relajacion de etiquetas con los datos reales completos, no solo un
   subconjunto chico donde la superposicion no se nota.
4. **¿Usa `katex.render()` directo (no solo `$...$` normal)?** -> usar el patron `DOMContentLoaded`,
   nunca `setTimeout(fn, 0)`.
5. **¿El color usado es distinto al del bloque de esa slide?** (si el widget tiene multiples
   elementos a diferenciar) -> confirmar contra `COLOR_BLOQUE[bloque]` antes de fijar la paleta del
   widget.
6. **¿El widget es el protagonista de la slide o quedo como un detalle chico al costado?** — misma
   filosofia que `/slides` ("el plot manda"): si la slide existe PARA ese widget, dimensionarlo
   generosamente (la mayor parte del espacio disponible en `.contenido`), no dejarlo en un tamano
   modesto por defecto y esperar que el usuario pida despues "hacelo mas grande". Cuando haya dudas,
   pecar de grande — es mas facil achicar despues que convencer de que vale la pena agrandar.

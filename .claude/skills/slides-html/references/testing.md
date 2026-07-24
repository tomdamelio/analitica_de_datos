# Testing: comandos y gotchas ya resueltos

## Regla madre: headless para layout estatico, navegador real para cualquier cosa con tiempo de por medio

Una captura headless en modo `--virtual-time-budget` **no simula bien el paso de tiempo real** entre
frames de `requestAnimationFrame`, ni necesariamente deja completar una transicion CSS antes de
capturar. Esto genera **falsos negativos** (se ve "roto"/"congelado" en la captura, pero funciona
perfecto en un navegador real) y, mas peligroso, **falsos positivos silenciosos** si uno asume que
"si no se ve mal en la captura, esta bien" sin haber probado interaccion real. Pasó varias veces en
el desarrollo de este patron: nunca declarar un widget animado/interactivo como "andando" o "roto"
en base solo a una captura headless.

## Layout/tamano/centrado estatico (headless esta bien)

```bash
msedge.exe --headless=new --disable-gpu --window-size=1600,900 --virtual-time-budget=4000 \
  --screenshot=salida.png "file:///C:/ruta/al/deck.html?slide=N"
```

- `?slide=N` salta directo a la slide N (0-indexed, en el orden en que aparecen en el archivo que se
  esta mirando — si es un preview de un solo bloque, N es el indice DENTRO de ese archivo, no el
  numero global de la clase).
- Variar `--window-size` a proporciones raras (ej. `1920,700` — ancho pero bajo) es la forma de
  reproducir el bug de "el deck se corta arriba/abajo" ANTES de que el usuario lo vea: simula una
  ventana de navegador real con poco alto disponible (barra de direcciones, pestañas).
- Para medir centrado con precision (no a ojo): PIL/numpy sobre la captura, contando que columnas de
  pixeles dentro del area conocida del deck son "no blancas":
  ```python
  from PIL import Image
  import numpy as np
  arr = np.array(Image.open("salida.png").convert("L"))
  sub = arr[y0:y1, x0:x1]  # recorte del area de interes
  cols_con_contenido = np.where((sub < 230).any(axis=0))[0]
  centro_contenido = (cols_con_contenido.min() + cols_con_contenido.max()) / 2 + x0
  ```
  Cuidado: esto mide el **centro de la TINTA** (los pixeles no blancos), que puede no coincidir con
  el centro del CONTENEDOR si el contenido interno es asimetrico (ej. un biplot cuyos datos reales se
  inclinan hacia un lado — eso es fiel a los datos, no un bug de layout). Para saber si es el
  CONTENEDOR el que esta mal centrado (y no solo su contenido), inyectar un script de debug que mida
  `getBoundingClientRect()` directamente — mas confiable que contar pixeles:
  ```python
  # insertar antes de </body> del HTML (una copia de prueba, no el archivo real):
  inject = """
  <script>
  setTimeout(function(){
    const el = document.getElementById('mi-widget');
    const r = el.getBoundingClientRect();
    const slide = el.closest('.slide').getBoundingClientRect();
    document.title = 'centro_el=' + ((r.left+r.right)/2) + ' centro_slide=' + ((slide.left+slide.right)/2);
  }, 1000);
  </script>"""
  ```
  Un caso real donde esto importo: un plano 3D "se veia corrido" — medir el contenedor con
  `getBoundingClientRect()` mostro que el DIV estaba perfectamente centrado; el problema real era que
  Plotly renderizaba a 700×450 (su default) anclado arriba-izquierda DENTRO de ese div correctamente
  centrado, porque el div media 0×0 en el momento del render (ver `references/widgets.md`, patron 2).
  Sin medir el contenedor por separado del contenido, ese diagnostico se habria confundido con "hay
  que ajustar el CSS de centrado", que no era el problema.

## Cualquier interaccion (click, tecla, animacion) — navegador real

La extension de navegador (Chrome-en-Claude) **no puede abrir `file://`** — hace falta un servidor
HTTP local:

```bash
cd /ruta/al/deck
python -m http.server 8794 &   # elegir un puerto libre
```

Luego, con la extension del navegador:
1. Crear/usar una pestaña, navegar a `http://localhost:8794/deck.html?slide=N`.
2. **Click en algun lugar de la pagina antes de mandar teclas** — si la pestaña no tiene foco (recien
   navegada, o el foco quedo en la barra de direcciones), los eventos de teclado pueden no llegar al
   `document` y parece que "no responde" cuando en realidad nunca se disparo el evento.
3. Click/tecla real -> **esperar ~1 segundo** (una transicion CSS tipica dura 300-400ms; dar margen)
   -> RECIEN AHI capturar. Capturar inmediatamente despues de la accion es la causa mas comun de ver
   un estado "a mitad de camino" y reportarlo por error como roto.
4. Repetir para cada paso de una secuencia (varios clicks/teclas seguidos): esperar entre cada uno,
   no mandar todos de una y capturar al final, para poder confirmar CADA paso intermedio.
5. Al terminar, matar el servidor: `netstat -ano | grep <puerto>` (Windows) para encontrar el PID,
   despues `Stop-Process -Id <pid> -Force` via PowerShell (o `kill` en Unix).

Si algo parece no reaccionar en el navegador real (no solo en headless), ahi si es un bug de verdad —
recien ahi vale la pena debuggear el JS (revisar la consola por errores, verificar con un script
inyectado que la funcion se registro/ejecuto, etc.) en vez de asumir que es timing.

## Debug de errores de JS silenciosos

Cuando algo no aparece y no hay pista visual de por que, inyectar un listener de errores ANTES que
cualquier otro script (justo despues de `<head>`) en una copia de prueba del HTML:

```html
<script>
window.addEventListener('error', function(e) {
  window.__jserrs = (window.__jserrs || []).concat(e.message + ' at line ' + e.lineno);
});
</script>
```

y leerlo con un script al final (`document.title = (window.__jserrs||[]).join(' || ')`, o un
`<div>` de debug visible en la captura). Esto fue lo que encontro el bug real de `katex is not
defined` (carrera de `setTimeout(fn,0)` contra el script de KaTeX, ver `references/arquitectura.md`)
que de otra forma parecia "la formula no se dibuja" sin ninguna pista de la causa.

## Dos gotchas mas del navegador real (encontrados probando esta misma skill)

- **La pestaña automatizada puede estar "viva" pero no visible/enfocada.** Si el navegador la
  considera en background (`document.hidden === true`), Chrome/Edge **pausan o throttlean
  `requestAnimationFrame`** — un boton que dispara una animacion puede parecer que "no hace nada".
  Esto es DISTINTO del problema de `--virtual-time-budget` en headless (ver arriba): puede pasar en
  un navegador real con la extension, si la pestaña de prueba no tiene foco real. Si un widget
  animado no reacciona pese a estar en un navegador real, verificar `document.hidden` antes de asumir
  un bug de JS — y si es eso, forzar el foco (click en la pestaña/ventana) antes de repetir la prueba.
  Como diagnostico alternativo sin depender del foco: disparar el mismo cambio via un evento de
  `input` sintetico o un click por referencia de accesibilidad y verificar el ESTADO final (valores
  actualizados en el DOM), en vez de depender de ver la animacion en curso.
- **La sesion de la extension del navegador puede estar compartida entre tareas concurrentes.** Si
  hay mas de un agente/proceso usando la extension al mismo tiempo, una pestaña de otra tarea puede
  aparecer, robar foco, o navegar por encima de la que se esta probando. Si el comportamiento de
  teclado/click es inconsistente sin razon aparente, revisar `tabs_context` para confirmar que se
  esta actuando sobre LA PESTAÑA PROPIA antes de seguir debuggeando el widget.

## Antes de descargar cualquier libreria externa (KaTeX, Plotly, fuentes)

Seguir el protocolo de permiso explicito: decir el nombre del archivo, la fuente (URL) y el tamano
aproximado, y esperar confirmacion del usuario antes de correr el `curl`/`wget`. Ver
`scripts/embed_libs.py`, que ya tiene este chequeo incorporado.

# Trampas conocidas

Cosas que ya costaron retrabajo en este repositorio. Leelas antes de armar la notebook de
Python (fase 5) y el par en R (fase 6).

## Contenidos

- [Python y R no calculan la varianza igual](#python-y-r-no-calculan-la-varianza-igual)
- [Ocultar una celda requiere tres mecanismos distintos](#ocultar-una-celda-requiere-tres-mecanismos-distintos)
- [Asserts fragiles](#asserts-fragiles)
- [Paridad de figuras entre Python y R](#paridad-de-figuras-entre-python-y-r)
- [Cargar datos que funcionen tambien en Colab](#cargar-datos-que-funcionen-tambien-en-colab)
- [Imagenes por URL raw](#imagenes-por-url-raw)
- [Manifiestos de dependencias](#manifiestos-de-dependencias)
- [Detalles de R](#detalles-de-r)
- [Scripts que generan notebooks](#scripts-que-generan-notebooks)
- [Sin Quarto local](#sin-quarto-local)

## Python y R no calculan la varianza igual

La que mas muerde, porque el sintoma es un `assert` que falla por un margen chiquito y parece
un error de redondeo.

`StandardScaler` de scikit-learn estandariza con la **varianza poblacional** (denominador `n`).
`scale()` de R usa la **varianza muestral** (denominador `n-1`). Consecuencia practica: sobre
datos ya estandarizados,

- en Python, `np.mean((v - v.mean())**2)` da exactamente 1;
- en R, esa misma cuenta da `(n-1)/n`, y lo que da exactamente 1 es `var(v)`.

Con n grande la diferencia es invisible a simple vista pero rompe cualquier comparacion con
tolerancia chica. Si afirmas que "con variables estandarizadas la varianza total es p", en
Python verificalo con la varianza poblacional y en R con `var()`.

Lo mismo vale para los autovalores: `prcomp(...)$sdev^2` esta en la escala muestral, asi que
suman exactamente `p` si entraste con datos escalados por `scale()`.

## Ocultar una celda requiere tres mecanismos distintos

Sirve para el andamiaje (branding, parametros, colores, helpers): el estudiante no necesita
verlo, pero tiene que ejecutarse. Cada visor entiende un mecanismo distinto y **ninguno cubre
a los otros dos**:

| Donde | Que lo oculta |
|---|---|
| Google Colab | metadata `cellView: form` + una linea `#@title Etiqueta { display-mode: "form" }` |
| JupyterLab y VS Code | metadata `jupyter.source_hidden: true` |
| El sitio (Quarto) | `#| include: false` (oculta codigo y salida) o `#| echo: false` (oculta solo el codigo) |

Quarto lee sus opciones **solo** en las primeras lineas de la celda, y deja de leerlas apenas
aparece un comentario que no empieza con `#|`. Como Colab necesita su `#@title`, el orden que
funciona para los dos es: `#|` primero, `#@title` despues, y la metadata aparte.

```python
#| include: false
#@title Configuracion de la materia (parametros, colores y funciones)  { display-mode: "form" }
import numpy as np
...
```

Si el docente dice "en mi editor no se ve oculta", casi siempre falta `jupyter.source_hidden`,
que es el unico que mira el editor local.

## Asserts fragiles

El objetivo es que un `assert` falle cuando el numero esta mal, no cuando el mundo es
levemente distinto de lo que asumiste.

- **No exijas monotonia que la matematica no garantiza.** El error global de reconstruccion
  baja siempre al sumar componentes; el error de *una celda puntual* puede subir. Verifica lo
  que es cierto (el error final es el minimo, y con todas las componentes es cero).
- **Elegi la tolerancia segun el calculo**, no por costumbre. Comparar varianzas calculadas con
  denominadores distintos con `atol=1e-8` falla por construccion.
- **Verifica contra un calculo independiente**, no contra la misma expresion escrita dos veces.
  El caso lindo: calcular un score a mano como suma de `loading x valor` y compararlo con el
  que devuelve la libreria.

## Paridad de figuras entre Python y R

Las figuras de R llevan sufijo `_r`; la de Python es la canonica del sitio y la que alimenta
las slides. La paridad es **conceptual**, no pixel a pixel: misma idea, mismos datos, misma
conclusion.

Una asimetria real: el `plotly` de R no exporta PNG estatico sin dependencias extra, mientras
que en Python `kaleido` lo hace. Los graficos interactivos quedan interactivos en las dos
notebooks, pero **el PNG estatico que usan las slides sale de la version de Python**.

## Cargar datos que funcionen tambien en Colab

Las notebooks se abren en Colab, donde no existe el repositorio en disco. Cargar con una ruta
relativa funciona al renderizar el sitio y falla para el estudiante.

Carga siempre desde una **URL publica y estable** (la fuente oficial del dataset, o el raw del
repo, que es publico) y versiona ademas una copia en `data/` para la autoria. Documenta fuente
y licencia en `data/README.md`.

Ojo con el orden: si la URL apunta al raw del repo, **no resuelve hasta que hiciste push**. Si
necesitas ejecutar la notebook antes de publicar, carga desde la fuente oficial externa.

## Imagenes por URL raw

Una imagen referenciada como `https://raw.githubusercontent.com/<owner>/<repo>/main/...`
funciona en Colab y en el sitio publicado, pero **se ve rota localmente y hasta que se pushea**.
No es un error: avisale al docente para que no lo reporte como bug.

Quarto tampoco copia al sitio las carpetas que nadie enlaza de forma relativa, asi que ese
archivo puede dar 404 en la ruta del sitio aunque este commiteado. Mientras la notebook lo
referencie por la URL raw, se ve bien igual.

## Manifiestos de dependencias

`requirements.txt` (Python) y `DESCRIPTION` (R) tienen que declarar todo lo que las notebooks
importan. Es de lo mas facil de olvidar, porque en la maquina donde se armo la clase el
paquete ya esta instalado y nada falla; el error aparece recien cuando alguien arma el entorno
desde cero.

Antes de cerrar, cruza los imports reales de las dos notebooks contra los manifiestos.
Distingue las dependencias que el material necesita para correr de las que son solo de autoria
(por ejemplo, la que exporta figuras estaticas para las slides) y dejalo anotado.

## Detalles de R

- `Rtsne` aborta si hay filas duplicadas: pasa `check_duplicates = FALSE`.
- `umap` de R se controla con un objeto de configuracion (`cfg <- umap.defaults; cfg$random_state <- SEED`),
  no con argumentos sueltos.
- El kernel de Jupyter para R se llama `ir`.
- Los widgets interactivos de Python (`ipywidgets`) no tienen equivalente directo. Resolvelo
  con el idiomatismo de R: una figura estatica que muestre lo mismo, o bloques `<details>`
  desplegables para las autoevaluaciones.

## Scripts que generan notebooks

Si armas la notebook con un script, **no mapees el contenido por indice de celda**. Insertar
una celda markdown corre todos los indices y el script queda desalineado en silencio la
proxima vez que se corre. Consumi el contenido en orden, o identifica las celdas por algo
estable.

## Sin Quarto local

Puede no haber Quarto instalado en la maquina donde se arma la clase. Como el sitio se
construye en CI y las notebooks se publican con outputs congelados, no es bloqueante, pero
significa que **el render de CI es la primera prueba real de los `.qmd`**. Decilo asi cuando
informes el estado, en vez de dar por bueno un render que no se hizo.

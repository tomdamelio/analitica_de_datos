---
name: armado-de-clase
description: Guia el armado completo de una clase de la materia Analitica de Datos (Maestria en Ciencias del Comportamiento, UdeSA), de punta a punta - notebooks en Python y R, pagina del sitio Quarto y diapositivas (HTML interactivo o Beamer/PDF, a eleccion del docente). Usala siempre que se vaya a preparar, armar, ampliar, corregir o cerrar una clase de esta materia, incluso si el docente solo dice "armemos la Clase N", "sigamos con la notebook", "ampliemos esta clase", "hagamos las slides" o menciona el programa de la materia. Define el ORDEN del proceso, los puntos donde hay que frenar a validar con el docente, y las trampas del repositorio que ya costaron retrabajo.
---

# Armado de una clase

Este repositorio publica una materia completa: un sitio Quarto con una pagina por clase,
dos notebooks por clase (Python como version de dictado y R como par validado) y un deck
Beamer. Este skill no arma el material por vos: define **en que orden** hacerlo, **donde
frenar** a validar con el docente, y **que trampas** ya nos costaron trabajo repetido.

Los docentes son Tomas D'Amelio y Nicolas Bruno. Cualquiera de los dos puede estar del otro
lado; no asumas contexto previo ni preferencias que no hayan dicho en la conversacion.

## Antes que nada: leer el contrato

`CONVENTIONS.md`, en la raiz del repo, es la fuente de verdad sobre estructura de carpetas,
nombres de archivo, anatomia de las paginas y notebooks, manejo de figuras, bilingueismo
Python/R y reglas de copyright. Leelo antes de crear nada. Este skill **no repite** esas
convenciones: si algo se contradice, gana `CONVENTIONS.md`.

Leé tambien la entrada de la clase en `programa.qmd` (objetivo, contenidos, practica y
lectura obligatoria). Es lo que la materia se comprometio a dar, y el material tiene que
cubrirlo.

## El orden importa, y esta es la razon

Cada clase existe por triplicado: notebook Python, notebook R y slides, ademas de la pagina.
Los tres derivan del mismo contenido. Si armas la version de R o el sitio antes de que la
notebook de Python este cerrada, **cada cambio posterior hay que espejarlo a mano en todos
lados**. Ya pasó, y duplicó el trabajo.

La regla que lo evita: **la notebook de Python se cierra primero, con el docente**. Recien
cuando el docente la da por terminada se toca R, el sitio y las slides. Cuesta paciencia al
principio y ahorra rehacer todo despues.

## Las nueve fases

Trabaja de a una. Las fases 4, 5 y 8 terminan en un **checkpoint**: presentas lo hecho y
esperas al docente antes de seguir. No las encadenes de corrido.

### 1. Encuadre

Identifica el numero de clase y lee su entrada en `programa.qmd`. Mira una clase ya armada
como plantilla viva (a la fecha, `clases/clase-02/` y `clases/clase-10/` son las completas).
Fijate que clases previas existen: el material se apoya en lo ya dado y no deberia depender
de clases que todavia no estan.

### 2. Bibliografia

Los libros de referencia estan en `context/refs/pdf/` (gitignoreado: son material con
copyright y **nunca** se publican). Suelen ser PDFs enteros de varios cientos de paginas.

Antes de leer, **parti el libro por capitulos** y guarda las partes en un subdirectorio
(por ejemplo `context/refs/pdf/islp_chapters/`). Un capitulo aislado se lee sin quemar
contexto, y queda disponible para las clases siguientes. Si ya estan partidos, usalos.

### 3. Validar los topicos

Contrasta tres fuentes antes de decidir el contenido:

- **el programa**, que fija el compromiso minimo;
- **el capitulo**, que fija el tratamiento y el vocabulario;
- **lo que el docente quiera sumar**, que suele ser lo que vuelve la clase propia.

Si el docente menciona que tiene **anotaciones sobre el texto** (subrayados y comentarios en
Zotero, notas sueltas, un documento de contexto), pedilas y leelas: son la guia mas directa
de que quiere enfatizar. Para leer anotaciones de Zotero hay instrucciones en
`references/zotero.md`. No vayas a buscarlas por tu cuenta si nadie las menciono.

Prestá atencion a los limites que el docente marque: material que explicitamente **no** va a
la notebook (a veces reservado para las slides), o sobre lo que no quiere detenerse.

### 4. Hilo narrativo y datos  ·  CHECKPOINT

Propone el arco de la clase: secciones en orden, que figura ancla cada una, y sobre que
datos. Discutilo antes de escribir codigo.

Sobre los datos, dos criterios que funcionaron bien:

- **Un solo dataset acompaña la explicacion.** Cambiar de dataset entre secciones rompe el
  hilo. Si hace falta un segundo, que sea para el ejercicio de cierre, y preferentemente uno
  que los estudiantes ya conozcan de clases anteriores: aplican el metodo nuevo sobre datos
  familiares.
- **Datos reales antes que sinteticos**, si existen y la licencia lo permite. Un dataset real
  donde el metodo revela algo genuino vale mas que uno fabricado. Documentalo en
  `data/README.md` con fuente, licencia y donde se usa, como pide `CONVENTIONS.md`.

Frena aca y espera el visto bueno del docente sobre el hilo y los datos.

### 5. Notebook de Python  ·  CHECKPOINT (y el mas importante)

Delega la construccion al skill **`colab-class-notebook`**, que define la anatomia
pedagogica (encabezado, indice, puente con el programa, hilo, secciones numeradas con
laboratorios intercalados, autoevaluacion y hoja de referencia). Este skill aporta lo que
ese no sabe: las convenciones de esta materia.

Lo que no es negociable en esta materia:

- **La notebook queda ejecutada**, con outputs visibles. Ejecutala de verdad (por ejemplo con
  `nbclient`) antes de darla por hecha.
- **Cada numero que afirmes en prosa sale de codigo y se verifica** con un `assert` contra un
  calculo independiente. Es lo que permite que el docente confie en la pagina sin recalcular:
  si un numero estuviera mal, la notebook no habria terminado de ejecutar.
- **Las figuras se guardan** en `clases/clase-NN/assets/figures/` con el nombre de la
  convencion. De ahi salen despues las slides, asi que no las inventes ni las reciclesde otra
  clase.
- **Los ejercicios llevan `solution` y `scaffold`** (`CONVENTIONS.md` §7), para poder generar
  despues la version sin soluciones de forma mecanica.

Presenta la notebook ejecutada y **detenete**. Espera correcciones. Aplicalas sobre Python y
volve a ejecutar. Repeti hasta que el docente la de por cerrada. **No avances a R, al sitio
ni a las slides mientras esta fase siga abierta**, por mas terminada que parezca.

### 6. Par en R

Recien ahora. El objetivo es paridad de contenido, no traduccion literal: mismo dataset,
mismos pasos, mismas conclusiones y las mismas figuras conceptuales, pero escritas con el
idiomatismo de R (`prcomp`, `kmeans`, `ggplot2`, `stopifnot`).

La forma mas segura de mantener la paridad es **espejar la notebook de Python celda a celda**:
reutiliza su prosa markdown (adaptando las referencias a funciones de Python) y reescribi solo
el codigo. Ejecutala con el kernel `ir` y verifica que no queden rastros de Python en el texto.

Las figuras de R llevan sufijo `_r`; la version de Python es la canonica del sitio.

Ojo con las diferencias reales entre lenguajes: hay una lista en `references/trampas.md`, y la
que mas muerde es que Python y R no calculan la varianza con el mismo denominador.

### 7. Sitio

Actualiza, en este orden:

1. `clases/clase-NN/index.qmd`, siguiendo la anatomia de `CONVENTIONS.md` §4. Revisa que
   **describa el material que realmente quedo**: si el hilo cambio durante la fase 5, la
   pagina escrita antes quedo desactualizada.
2. `_quarto.yml`, agregando la clase al submenu "Clases".
3. `data/README.md`, si entro un dataset nuevo.
4. **Los manifiestos de dependencias**: `requirements.txt` y `DESCRIPTION`. Es facil
   olvidarlos y el error no aparece hasta que alguien arma el entorno desde cero. Cruza los
   imports reales de las dos notebooks contra los manifiestos.

El mapa del programa se actualiza solo: `scripts/gen_mapa.py` enlaza la clase apenas existe
su `index.qmd`.

No enlaces archivos que todavia no existen (el PDF de las slides, por ejemplo): es un enlace
roto en el sitio publicado.

### 8. Slides  ·  CHECKPOINT

Antes de arrancar, **preguntale al docente que formato de slides quiere** — no lo decidas por tu
cuenta ni asumas el mismo formato de la clase anterior:

- **HTML interactivo** (skill `slides-html`) — deck autocontenido para navegador, con widgets reales
  (arrastrar una recta, rotar un plano 3D, comparar metodos, revelar una formula termino a termino) en
  vez de solo texto y figuras estaticas. **Esta es la opcion recomendada por defecto**: para esta
  materia (metodos que se entienden mejor viendolos moverse) la interaccion suele valer la pena, y
  `clases/clase-10/slides-html/` ya es un ejemplo completo y probado para calibrarse. Si el docente no
  tiene preferencia o no esta seguro, proponé esta.
- **LaTeX/Beamer -> PDF** (skill `slides-latex`) — paginas fijas, sin interaccion; mejor si el docente
  va a imprimir el material, prefiere el look institucional ya armado en Beamer, o no quiere depender
  de un navegador durante la clase.

Delega al skill que corresponda segun la respuesta. Los dos comparten la misma tematizacion por
bloque y el mismo espiritu colaborativo (armar y parar, no todo de una).

Lo propio de esta materia, para cualquiera de los dos formatos:

- Las slides usan **las figuras/datos reales que emitieron las notebooks**, no figuras nuevas ni
  numeros inventados. Si necesitas un numero que no tenes a mano, recalculalo desde los datos.
- Las slides cubren el **contenido teorico**; la practica vive en las notebooks. En cada bloque, un
  puntero a Colab marca la tarea.
- **`slides-html`**: copiar `comun.py` de `clases/clase-10/slides-html/` como base (ya tiene la
  identidad visual de la materia resuelta), no partir del starter kit generico de la skill.
- **`slides-latex`**: copiar el tema y los logos de una clase ya armada en Beamer.

Compila/genera, revisa el render y presenta el deck. Despues **iteran slide por slide** al ritmo del
docente.

### 9. Cierre

Commit, merge y push, y **verifica que quedo publicado de verdad**: que el workflow de CI
haya pasado y que las URLs respondan. Los pasos concretos estan en `references/cierre.md`.

Nada esta terminado porque el archivo exista localmente. Esta terminado cuando el sitio
publicado lo muestra.

## Los skills en los que se apoya

`colab-class-notebook` (fase 5) y, en la fase 8, **`slides-html`** (recomendada por defecto) o
`slides-latex` (segun lo que elija el docente), viven en `.claude/skills/` de este repositorio,
versionados junto con la materia. Estan ahi para que los dos docentes trabajen sobre la misma
version sin instalar nada: alcanza con clonar el repo.

Son skills genericos, asi que un docente puede tener ademas su copia personal en
`~/.claude/skills/` para usarlos en otros proyectos. Para esta materia, **la version del repo
es la que manda**: si alguna vez divergen, la del repo es la que esta acordada entre ambos y
la que corresponde usar aca.

## Archivos de referencia

- `references/trampas.md` — las diferencias Python/R, los tres mecanismos para ocultar celdas,
  paridad de figuras y otros detalles que ya costaron retrabajo. Leelo antes de las fases 5 y 6.
- `references/zotero.md` — como leer subrayados y comentarios del docente sobre un PDF. Solo
  si el docente menciona que tiene anotaciones.
- `references/cierre.md` — flujo de git, CI y verificacion de publicacion. Fase 9.

## Como trabajar con el docente

El docente marca el ritmo. Los checkpoints existen porque una clase es una decision
pedagogica suya, no una tarea a completar: presentar y esperar es mas rapido que rehacer.

Cuando una decision cambie el trabajo de forma importante (que dataset, que se cubre y que
no, cuanto se profundiza), preguntá antes en vez de elegir por tu cuenta. Cuando sea una
convencion ya escrita o un detalle menor, resolvelo y seguí.

Si algo no se pudo verificar, decilo. Es preferible "el render de CI va a ser la primera
prueba real porque no hay Quarto local" a dar por bueno algo que no se probo.

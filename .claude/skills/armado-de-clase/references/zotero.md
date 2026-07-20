# Leer las anotaciones del docente en Zotero

Solo si el docente menciona que tiene subrayados y comentarios sobre el texto. No vayas a
buscarlos por tu cuenta.

Cuando existen, son el insumo mas directo de que quiere enfatizar: los **comentarios** suelen
ser instrucciones concretas ("este ejemplo me gusta para clase", "esto no lo cubramos",
"mostrar esto de forma interactiva"), y los **subrayados sin comentario** marcan que pasajes
considera centrales.

## Conectarse

`pyzotero` en modo local lee la biblioteca sin API key, hablando con la aplicacion de escritorio.
Requiere que **Zotero este abierto** y que tenga habilitado el acceso local para otras
aplicaciones (en Zotero: Preferencias, Avanzado).

```python
from pyzotero import zotero
zot = zotero.Zotero(library_id="0", library_type="user", local=True)
```

Si falla la conexion, avisale al docente que abra Zotero en vez de intentar rodearlo.

## Encontrar el PDF y sus anotaciones

El camino es coleccion -> item del libro -> adjunto PDF -> anotaciones.

```python
# 1. la coleccion de la materia
for c in zot.collections():
    print(c["key"], c["data"]["name"])

# 2. los items de esa coleccion (el libro y sus adjuntos)
for it in zot.collection_items("<KEY_COLECCION>"):
    d = it["data"]
    print(it["key"], d.get("itemType"), d.get("title"), d.get("contentType", ""))

# 3. las anotaciones del adjunto PDF
anns = zot.children("<KEY_ADJUNTO_PDF>", itemType="annotation")
```

**El filtro `itemType="annotation"` no es opcional.** Sin el, `children()` devuelve una lista
vacia aunque el PDF tenga decenas de anotaciones, y el item hasta informa `numChildren: 0`. Es
una particularidad del modo local que hace parecer que no hay nada anotado.

## Que mirar de cada anotacion

```python
import json
for a in anns:
    d = a["data"]
    pagina = json.loads(d.get("annotationPosition", "{}")).get("pageIndex")
    print(pagina,
          d.get("annotationPageLabel"),   # numero de pagina impreso en el libro
          d.get("annotationText"),        # el texto subrayado
          d.get("annotationComment"))     # la nota del docente, si la escribio
```

Al procesarlas conviene separar las que tienen `annotationComment` no vacio: son pocas y son
las accionables. Las demas sirven para saber que partes del capitulo enfatizar.

`annotationPageLabel` es la pagina impresa y `pageIndex` la del PDF; casi nunca coinciden.
Para ubicar el capitulo, usa `pageIndex`.

## Al reportarlas

Devolvele al docente un resumen que enlace **cada comentario con el cambio concreto** que
propones hacer en el material, y confirma antes de aplicarlos si implican reestructurar. Un
comentario breve puede significar un cambio grande: "mejor empezar en dos dimensiones"
reordena media clase.

Prestá especial atencion a los comentarios que **excluyen** contenido o lo reservan para otro
entregable ("esto no va en la notebook, guardalo para las slides"). Son faciles de pasar por
alto y molesto de deshacer.

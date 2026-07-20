# Cierre: publicar y verificar

Fase 9. Una clase no esta terminada porque los archivos existan en disco: esta terminada
cuando el sitio publicado la muestra.

## Antes de commitear

Repasa que no quede material a medias:

- Las dos notebooks ejecutadas, sin errores y con las figuras emitidas.
- La pagina describiendo **el material que realmente quedo** (si el hilo cambio durante la
  iteracion, la pagina escrita antes quedo vieja).
- Sin enlaces a archivos que no existen todavia.
- Los manifiestos de dependencias al dia.
- Los artefactos de compilacion fuera (LaTeX genera `.aux`, `.log`, `.nav`, `.out`, `.snm`,
  `.toc`; el `.gitignore` los cubre).

Y sobre todo: **`context/` nunca se commitea**. Ahi viven los PDFs de los libros, que tienen
copyright. Esta gitignoreado; confirma que el `git status` no los muestre antes de agregar.

## Git

El repositorio publica desde `main`: el workflow de CI se dispara con cada push a esa rama.
Trabaja en una rama y mergeala cuando la clase este lista.

```bash
git checkout -b clase-NN-<tema>
# ... trabajo ...
git add -A && git status --short          # revisar QUE se esta agregando
git commit                                 # mensaje explicando el porque, no solo el que
```

Los mensajes de commit del repo describen que se armo y con que criterio, no solo la lista de
archivos. Ayuda al otro docente a entender decisiones sin leer el diff.

Para publicar:

```bash
git checkout main
git merge --ff-only clase-NN-<tema>
git push origin main
```

## Verificar que salio

Publicar sin verificar es la forma mas comun de creer que algo esta hecho cuando no lo esta.

**1. Que el workflow de CI haya pasado.** Es la primera prueba real del render si no hay
Quarto local.

```bash
gh run list --limit 3
gh run watch <run-id> --exit-status
```

**2. Que las URLs respondan.** Al menos la pagina de la clase, las dos notebooks renderizadas,
el PDF de las slides y el programa.

```python
import urllib.request
base = "https://tomdamelio.github.io/analitica_de_datos"
for u in ["/clases/clase-NN/index.html",
          "/clases/clase-NN/notebooks/claseNN_python.html",
          "/clases/clase-NN/notebooks/claseNN_r.html",
          "/clases/clase-NN/slides/claseNN.pdf",
          "/programa.html"]:
    try:
        r = urllib.request.urlopen(base + u, timeout=30)
        print(r.status, len(r.read()) // 1024, "KB", u)
    except Exception as e:
        print("ERR", getattr(e, "code", "?"), u)
```

Un 404 no siempre es un problema: los archivos que nadie enlaza de forma relativa no se copian
al sitio. Fijate si algo del material los necesita por esa ruta antes de salir a arreglarlo.

**3. Que la pagina muestre lo que corresponde.** Abrila y revisa que los datasets, las
secciones y los enlaces sean los de esta clase y no restos de una version anterior.

## Informar el estado

Al cerrar, decile al docente que quedo publicado, que se verifico y **que quedo pendiente**.
Si algo no se pudo probar, nombralo en vez de darlo por bueno. La lista de pendientes es tan
parte del cierre como el push.

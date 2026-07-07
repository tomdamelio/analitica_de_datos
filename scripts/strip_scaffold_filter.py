#!/usr/bin/env python
"""Filtro ipynb para Quarto (declarado en _quarto.yml como ipynb-filters).

Quarto serializa la metadata desconocida de cada celda dentro de los atributos
del div ::: {.cell ...}; un `scaffold` multilinea con indentacion rompe ese
parseo y el HTML sale con divs sin procesar. Este filtro remueve la clave
`scaffold` SOLO de la copia que Quarto usa para renderizar: el .ipynb fuente
conserva el marcado solution+scaffold intacto (CONVENTIONS.md, seccion 7).

Recibe el JSON de la notebook por stdin y lo devuelve por stdout.
"""
import json
import sys

# stdin/stdout en bytes con utf-8 explicito: en Windows la consola puede ser
# cp1252 y el JSON de la notebook es utf-8.
nb = json.loads(sys.stdin.buffer.read().decode("utf-8"))
for cell in nb.get("cells", []):
    cell.get("metadata", {}).pop("scaffold", None)
sys.stdout.buffer.write(json.dumps(nb, ensure_ascii=False).encode("utf-8"))

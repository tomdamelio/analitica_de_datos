# REPORT — Fase 1: Maquetado del curso + Clase 2 piloto

**Fecha:** 2026-07-07 · **Parámetro de la corrida:** `COLAB_BASE = tomdamelio/analitica_de_datos/main`

---

## 1. Qué se creó

**El sistema** (reutilizable por las Fases 2 y 3):

- Sitio Quarto completo: `_quarto.yml` (nav, tema, `freeze: auto`), `index.qmd`, `programa.qmd` (desde el programa final), `bibliografia.qmd` (solo enlaces).
- `_variables.yml`: **único** punto de parametrización de `<owner>/<repo>/<branch>` (`colab-root`, `site-url`).
- `theme/tokens.yml` + `theme/udesa.scss`: paleta y tema del sitio.
- `requirements.txt` (Python, versiones validadas) y `DESCRIPTION` (R).
- `.github/workflows/publish.yml`: build + deploy a GitHub Pages, **listo pero inerte** (no existe el remoto todavía).
- `scripts/strip_scaffold_filter.py`: ipynb-filter de Quarto (ver decisión 4).
- Repo git inicializado con `.gitignore` (`context/` fuera del versionado desde el arranque).
- `context/refs/`: bibliografía de autoría organizada + `bibliografia_manifest.md`.

**La demostración** (Clase 2 de punta a punta):

- `clases/clase-02/index.qmd`: página con anatomía de CONVENTIONS §4.
- `clases/clase-02/notebooks/clase02_python.ipynb` (57 celdas) y `clase02_r.ipynb` (53 celdas): **ambas ejecutadas sin errores**, mismos resultados, construidas con el skill `colab-class-notebook` (TOC clickeable, hilo, labs intercalados, quiz, machete final).
- 6 figuras en `clases/clase-02/assets/figures/` (3 canónicas Python + 3 espejo `_r`).
- `data/hr_attrition.csv` + `data/README.md` (fuente, licencia, diccionario de variables).

## 2. Decisiones tomadas (y desvíos del prompt, con motivo)

1. **URLs de bibliografía corregidas.** Las URLs de descarga directa de ISLP y ESL del prompt devuelven **404**: los autores ahora sirven los PDFs vía Google Drive. Se descargaron desde ahí (verificados: PDF válidos, 20 MB y 13 MB) y el manifest y `bibliografia.qmd` enlazan a las **home oficiales estables** en lugar de PDFs directos.
2. **Fuente del dataset: repo oficial de IBM, no Kaggle.** `IBM/employee-attrition-aif360` (GitHub, licencia del repo **Apache-2.0**) sirve el CSV público y estable; Kaggle requiere login. Las notebooks cargan desde esa URL raw. Decisión conservadora: **el CSV no se sirve desde el sitio público** hasta que la cátedra valide la licencia (pregunta abierta 1).
3. **Faltantes/duplicados simulados determinísticamente.** El dataset viene sin faltantes ni duplicados, pero la Clase 2 los enseña. La notebook ensucia una **copia** con reglas fijas por número de legajo (sin RNG): las mismas filas se ensucian en Python y en R, así los resultados son idénticos y comparables. Documentado como "nota de laboratorio" en la notebook y en `data/README.md`.
4. **Filtro de render para `scaffold`.** La metadata `scaffold` multilinea (CONVENTIONS §7) rompe la serialización de atributos de Quarto (divs `:::` sin parsear en el HTML). Solución: `ipynb-filters` que quita `scaffold` **solo de la copia que Quarto renderiza**; los `.ipynb` fuente conservan el marcado completo para el stripping futuro. Bug aislado con bisección; test mínimo reproducible.
5. **Branding placeholder alineado con el skill.** No hay `context/brand/`; se usó el azul UdeSA `#00529B` + terracota `#C0492F` (default del skill de notebooks), consistente entre sitio (`tokens.yml`/`udesa.scss`) y figuras de ambas notebooks. Señalado como `placeholder` en `tokens.yml`.
6. **Variables de la Clase 2** (criterio comportamental): `Attrition` como objetivo; `MonthlyIncome` (asimetría/outliers), `OverTime` y `BusinessTravel` (los contrastes más fuertes: 30,5% vs 10,4% y 24,9% vs 8,0%), `Department`/`JobRole` (dónde se concentra la rotación), `DistanceFromHome` y `JobSatisfaction` (imputación), y features `IngresoPorAnioExp`, `TramoEdad`, `ViajaFrecuente`.
7. **Repo público** *(decisión de cátedra 2026-07-07, posterior al checkpoint)*. La arquitectura original (repo privado + Pages) resultó inviable en el plan Free de GitHub (Pages en privados requiere plan pago). Se evaluó un espejo público de notebooks (Colab no abre repos privados), pero al hacer público el repo principal el espejo quedó obsoleto y se eliminó: los badges apuntan directo a `tomdamelio/analitica_de_datos`. Nota: el repo público expone también `data/hr_attrition.csv`; es la misma copia que IBM publica en su propio repo (Apache-2.0), registrado en la pregunta abierta 1. El repo espejo `analitica-de-datos-notebooks` puede borrarse desde la web de GitHub.
8. **Entorno instalado desde cero** (máquina sin Python/R/Quarto): Python 3.12.10 (winget), Quarto 1.9.38 **portable** en `~/apps/quarto` (el instalador winget requería admin), R 4.5.3 (ya presente en AppData) + IRkernel registrado (`ir` en Jupyter). LaTeX **no** se instaló (Fase 2).

## 3. Cómo correr / buildear

```bash
# Render local (Quarto portable de esta máquina: ~/apps/quarto/bin/quarto)
quarto render      # -> _site/
quarto preview     # servidor local

# Re-ejecutar notebooks (solo al editarlas; el sitio usa los outputs guardados)
cd clases/clase-02/notebooks
jupyter nbconvert --to notebook --execute --inplace clase02_python.ipynb
jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=ir clase02_r.ipynb
```

Deploy: crear el repo privado `tomdamelio/analitica_de_datos`, Settings → Pages → Source: *GitHub Actions*, y pushear a `main`. El workflow no ejecuta código (freeze + outputs guardados); solo renderiza y publica.

## 4. Qué se validó

- ✅ **Ambas notebooks ejecutan de punta a punta sin errores** (nbconvert `--execute`; kernels `python3` e `ir`).
- ✅ **Paridad Python/R**: asserts idénticos en ambas (1470×35; 237 bajas = 16,1%; mediana $4.919; 416 con horas extra; constantes = {EmployeeCount, Over18, StandardHours}; 5 duplicados; 77+44=121 faltantes; mediana 7 / moda 4; 114 outliers todos JobLevel ≥ 4; tasas 10,4%/30,5%, 24,9%/14,1%, 39,8% Sales Rep; mediana IngresoPorAnioExp 549,22). Todo número mostrado sale de ejecutar código.
- ✅ **Marcado para stripping**: 4 ejercicios por notebook con tag `solution` + metadata `scaffold` (con huecos `___` y `# TODO`), verificado por script.
- ✅ **Sitio renderiza sin warnings**; notebook Python legible en el sitio con figuras; badges Colab apuntan a `tomdamelio/analitica_de_datos/main`; bibliografía solo enlaza (9 links externos, 0 PDFs); `data/` y `context/` **no** se copian a `_site/`.
- ✅ Sin guiones largos (em/en dashes) en las notebooks; español en todo el material; sin deep learning; Eje IV = NLP en `programa.qmd`.
- ⚠️ **No validado aún** (requiere el repo en GitHub): que los badges resuelvan en Colab y que el runtime R de Colab tome el kernelspec `ir` automáticamente. Metadata preparada para eso (`kernelspec: ir` + `language_info: R`); verificar en el primer push (pregunta abierta 3).

## 5. Preguntas abiertas para la cátedra

1. **Licencia del dataset:** ¿alcanza el Apache-2.0 del repo oficial de IBM para servir `hr_attrition.csv` también desde GitHub Pages como respaldo? Hoy las notebooks cargan del repo de IBM; si IBM archivara ese repo, habría que mover la carga al sitio propio o a un mirror.
2. **Branding:** ¿confirman el azul `#00529B` + terracota, o proveen la guía oficial UdeSA para `context/brand/`? Si cambia la paleta, hay que regenerar las 6 figuras (un re-run de cada notebook).
3. **Primer push:** al crear el repo, verificar en Colab: badge Python, badge R (runtime R automático) y carga del CSV. Cinco minutos de chequeo manual.
4. **Nombre de la variable de curso en las notebooks:** los títulos de sección y ejercicios usan voseo ("escribí", "calculá" en consignas neutras "escribi/calcula" sin tilde por la regla anti-acentos en headings). ¿OK el registro rioplatense en todo el material?
5. **`CONVENTIONS_1.md` en la raíz** quedó como copia de descarga (gitignoreada); la canónica es `CONVENTIONS.md`. ¿La borro?

## 6. Estado del checklist de Fase 1

Todos los ítems de la definición de "listo" están cumplidos, con dos notas: el deploy quedó **configurado sin publicar** (no existe el remoto; decisión del checkpoint) y la validación en Colab queda pendiente del primer push (ver preguntas 1 y 3).

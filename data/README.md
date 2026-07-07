# data/ — datasets de la materia

> Regla (`CONVENTIONS.md` §9): solo datasets chicos, con fuente y licencia documentadas
> acá. Las notebooks cargan los datos desde una **URL pública estable** (el repo es
> privado, su raw no sirve para Colab); la copia local es para autoría/render.

## `hr_attrition.csv` — dataset espina (clases 2–7 y 9–10)

**IBM HR Analytics Employee Attrition & Performance** — dataset ficticio creado por
científicos de datos de IBM para ilustrar problemas de people analytics (predicción de
rotación de personal / *turnover*).

| Campo | Valor |
|---|---|
| Dimensiones | 1.470 filas × 35 columnas (1 fila = 1 empleado/a) |
| Variable objetivo | `Attrition` (Yes/No; 237 Yes = 16,1%) |
| Faltantes / duplicados | 0 / 0 (dataset "limpio de fábrica"; ver nota pedagógica) |
| Fuente primaria | IBM Sample Data. Publicado por IBM en su repo oficial [`IBM/employee-attrition-aif360`](https://github.com/IBM/employee-attrition-aif360) (archivo `data/emp_attrition.csv`) |
| Fuente de difusión | [Kaggle: IBM HR Analytics Attrition](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) (requiere login; NO se usa para cargar) |
| **URL de carga en notebooks** | `https://raw.githubusercontent.com/IBM/employee-attrition-aif360/master/data/emp_attrition.csv` |
| Descargado | 2026-07-07 |
| Se usa en | Clase 2 (EDA/limpieza), y previsto para 3 (viz), 4–7 (supervisado), 9–10 (no supervisado) |

### Licencia — ⚠️ punto a validar por la cátedra

- La versión difundida en Kaggle figura como *"Database: Open Database, Contents:
  Database Contents"*, pero IBM nunca publicó una licencia abierta formal específica
  para el dataset. Es de uso educativo **muy** extendido.
- El repo **oficial de IBM** que lo contiene (`IBM/employee-attrition-aif360`) está
  licenciado **Apache-2.0**, lo que cubre el repo y razonablemente sus datos de ejemplo;
  aun así, la licencia del *repo* no es una declaración explícita sobre el *dataset*.
- **Decisión adoptada en Fase 1 (conservadora):** las notebooks cargan el CSV **desde la
  URL raw del repo de IBM** (fuente pública, oficial y estable) y **no** se sirve el CSV
  desde el sitio público de la materia. Si la cátedra decide que Apache-2.0 alcanza, se
  puede pasar a servirlo desde GitHub Pages (`<site-url>/data/hr_attrition.csv`) como
  respaldo ante cambios en el repo de IBM. Registrado como pregunta abierta en `REPORT.md`.

### Nota pedagógica (Clase 2)

El dataset original **no tiene faltantes ni duplicados**. Para enseñar detección y
manejo de datos faltantes/duplicados, la notebook de la Clase 2 introduce "suciedad"
**determinística y documentada** (reglas por índice, sin aleatoriedad, idénticas en
Python y R) sobre una copia, y luego la limpia. Los descriptivos y figuras del análisis
final salen siempre de los datos reales.

### Diccionario de variables (subset usado en Clase 2)

| Variable | Tipo | Descripción |
|---|---|---|
| `Age` | int | Edad en años |
| `Attrition` | cat (Yes/No) | Si el empleado dejó la empresa |
| `Department` | cat (3) | Departamento |
| `JobRole` | cat (9) | Puesto |
| `MonthlyIncome` | int | Ingreso mensual (USD) |
| `TotalWorkingYears` | int | Años de experiencia laboral total |
| `YearsAtCompany` | int | Antigüedad en la empresa |
| `DistanceFromHome` | int | Distancia casa–trabajo (km) |
| `OverTime` | cat (Yes/No) | Hace horas extra |
| `JobSatisfaction` | ord 1–4 | Satisfacción con el trabajo |
| `WorkLifeBalance` | ord 1–4 | Balance vida–trabajo |
| `EnvironmentSatisfaction` | ord 1–4 | Satisfacción con el ambiente |
| `MaritalStatus` | cat (3) | Estado civil |
| `NumCompaniesWorked` | int | Empresas anteriores |

Columnas constantes sin información (`EmployeeCount`, `StandardHours`, `Over18`) se
usan en la clase justamente como ejemplo de columnas a descartar.

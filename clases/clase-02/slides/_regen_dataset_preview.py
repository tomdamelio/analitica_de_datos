# -*- coding: utf-8 -*-
"""Genera una imagen-preview del dataset HR Attrition (datos reales) para la slide 2."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

NAVY = "#00529B"; INK = "#122535"; RED = "#B4232E"; SURF = "#F5F7FA"

df = pd.read_csv("data/hr_attrition.csv")
cols = ["Age", "Department", "JobRole", "MonthlyIncome", "OverTime", "Attrition"]
head = ["Edad", "Departamento", "Puesto", "Ingreso", "Horas extra", "Se fue?"]
sub = df[cols].head(6).copy()
sub["MonthlyIncome"] = sub["MonthlyIncome"].map(lambda v: f"${v:,}")
sub["OverTime"] = sub["OverTime"].map({"Yes": "Si", "No": "No"})
sub["Attrition"] = sub["Attrition"].map({"Yes": "Si", "No": "No"})
# abreviar departamentos largos para que entren en la tabla
sub["Department"] = sub["Department"].replace({
    "Research & Development": "I+D", "Human Resources": "RR.HH.", "Sales": "Ventas"})

fig, ax = plt.subplots(figsize=(10.5, 2.5))
ax.axis("off")
tbl = ax.table(cellText=sub.values, colLabels=head, cellLoc="center", loc="center")
tbl.auto_set_font_size(False)
tbl.set_fontsize(11)
tbl.scale(1, 1.55)

ncols = len(head)
# anchos de columna proporcionales al contenido mas largo de cada columna
maxlen = []
for c in range(ncols):
    m = len(str(head[c]))
    for v in sub.iloc[:, c].astype(str):
        m = max(m, len(v))
    maxlen.append(m)
total = sum(maxlen)
widths = [ml / total for ml in maxlen]
for (r, c), cell in tbl.get_celld().items():
    cell.set_width(widths[c])
    cell.set_edgecolor("white")
    if r == 0:  # header
        cell.set_facecolor(NAVY)
        cell.set_text_props(color="white", fontweight="bold")
        cell.set_height(cell.get_height() * 1.05)
    else:
        cell.set_facecolor("white" if r % 2 else SURF)
        # destacar la columna objetivo (Attrition = ultima)
        if c == ncols - 1:
            val = sub.iloc[r - 1]["Attrition"]
            cell.set_facecolor("#F7DDD9" if val == "Si" else "#E3EAF0")
            cell.set_text_props(color=RED if val == "Si" else INK, fontweight="bold")
        else:
            cell.set_text_props(color=INK)

out = "clases/clase-02/../../context/_muestras_slides/_tmp_preview.png"  # placeholder
import os
dest = os.path.join(os.path.dirname(__file__), "slides_build", "clase02_dataset_preview.png")
fig.savefig(dest, dpi=200, bbox_inches="tight", facecolor="white")
print("guardado:", dest, "| filas:", len(sub))
print("Attrition en las 6 filas:", list(sub["Attrition"]))

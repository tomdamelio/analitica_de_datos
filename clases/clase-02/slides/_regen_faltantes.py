# -*- coding: utf-8 -*-
"""Figura 'faltantes por variable' (sin titulo) reproduciendo el ensuciado de la notebook."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd, numpy as np
import sys

NAVY = "#00529B"; ACCENT = "#C0492F"; INK = "#122535"
df = pd.read_csv("data/hr_attrition.csv")
const = [c for c in df.columns if df[c].nunique() == 1]
df = df.drop(columns=const)
ds = pd.concat([df, df.head(5)], ignore_index=True).drop_duplicates().reset_index(drop=True)
ds["DistanceFromHome"] = ds["DistanceFromHome"].astype("float64")
ds["JobSatisfaction"] = ds["JobSatisfaction"].astype("float64")
ds.loc[ds["EmployeeNumber"] % 20 == 0, "DistanceFromHome"] = np.nan
ds.loc[ds["EmployeeNumber"] % 31 == 0, "JobSatisfaction"] = np.nan
falt = ds.isna().sum()
falt = falt[falt > 0].sort_values(ascending=False)
print("faltantes:", dict(falt))

plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False,
                     "font.size": 12, "text.color": INK, "axes.labelcolor": INK,
                     "xtick.color": INK, "ytick.color": INK, "axes.edgecolor": INK})
fig, ax = plt.subplots(figsize=(7, 3.3))
labels = list(falt.index)
vals = [int(v) for v in falt.values]
bars = ax.bar(labels, vals, color=[NAVY, ACCENT][:len(labels)], width=0.5)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.5, str(v), ha="center",
            fontweight="bold", color=INK)
ax.set_ylabel("celdas faltantes")
ax.set_ylim(0, max(vals) * 1.18)
fig.tight_layout()
out = sys.argv[1]
fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
print("guardado:", out)

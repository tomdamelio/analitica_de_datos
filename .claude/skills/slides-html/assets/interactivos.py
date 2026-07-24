"""
Widgets interactivos reusables para el deck HTML (SVG/Plotly + JS vanilla). Cada uno recibe
los datos YA PRECOMPUTADOS por parametro (nunca tocan un CSV/dataset crudo ni llaman a
pandas/sklearn) — eso lo hace `datos.py` una sola vez y los vuelca a un JSON que se lee antes
de generar el deck. Ver references/widgets.md en la skill para el detalle de cuando usar cada
uno y los gotchas ya resueltos (no repetirlos).

Requiere Plotly embebido (widget_plano_3d, widget_biplot) y/o KaTeX embebido
(widget_formula_pasos) — generarlos con scripts/embed_libs.py y pasarlos como `extra_js`/
incluirlos en el CSS del deck (ver comun.py armar_html).
"""

import json

import numpy as np


def widget_recta_girando(color_bloque, datos, id_="recta1"):
    """
    Una recta que gira (slider + boton "Girar", animado con requestAnimationFrame): a medida
    que rota, dos cantidades que se mueven en sentidos opuestos (ej. varianza capturada / error
    de proyeccion) se leen en vivo desde curvas YA PRECOMPUTADAS (interpolacion lineal, nunca se
    recalcula el modelo en el navegador). Uso tipico: mostrar que dos definiciones equivalentes
    de un mismo optimo se alcanzan en el mismo punto.

    `datos` = {
      "puntos": [[x,y], ...], "target": ["grupoA", ...], "colores": {"grupoA": "#hex", ...},
      "angulos": [...], "varianza": [...], "error": [...],  # curvas precomputadas por angulo
    }
    """
    payload = {
        "puntos": datos["puntos"], "target": datos["target"], "colores": datos["colores"],
        "angulos": datos["angulos"], "varianza": datos["varianza"], "error": datos["error"],
    }
    grupos = sorted(set(datos["target"]))
    leyenda = "".join(
        f'<span class="leyenda-item"><i style="background:{datos["colores"][g]}"></i>{g}</span>'
        for g in grupos)

    return f"""
<div class="widget-recta" id="widget-{id_}">
  <div class="svg-col">
    <svg viewBox="-3.6 -3.6 7.2 7.2" class="svg-recta" id="svg-{id_}"></svg>
    <div class="leyenda-recta">{leyenda}</div>
  </div>
  <div class="controles-recta">
    <div class="fila-slider">
      <input type="range" min="0" max="179" step="1" value="0" id="slider-{id_}" class="slider-angulo">
      <button id="play-{id_}" class="boton-girar" style="border-color:{color_bloque};color:{color_bloque}">▶ Girar</button>
    </div>
    <div class="medidor">
      <span class="medidor-label">Varianza capturada</span>
      <div class="medidor-barra"><div class="medidor-fill" id="fillvar-{id_}" style="background:{color_bloque}"></div></div>
      <span class="medidor-valor" id="valvar-{id_}" style="color:{color_bloque}"></span>
    </div>
    <div class="medidor">
      <span class="medidor-label">Error de proyección</span>
      <div class="medidor-barra"><div class="medidor-fill error" id="fillerr-{id_}"></div></div>
      <span class="medidor-valor" id="valerr-{id_}" style="color:#CB181D"></span>
    </div>
    <p class="medidor-angulo">Ángulo: <strong id="valang-{id_}">0°</strong></p>
  </div>
</div>
<script>
(function() {{
    const datos = {json.dumps(payload, ensure_ascii=False)};
    const NS = "http://www.w3.org/2000/svg";
    const svg = document.getElementById("svg-{id_}");

    function Y(y) {{ return -y; }}

    for (const [x1, y1, x2, y2] of [[-3.5, 0, 3.5, 0], [0, -3.5, 0, 3.5]]) {{
        const l = document.createElementNS(NS, "line");
        l.setAttribute("x1", x1); l.setAttribute("y1", Y(y1));
        l.setAttribute("x2", x2); l.setAttribute("y2", Y(y2));
        l.setAttribute("stroke", "#c8c8c8"); l.setAttribute("stroke-width", "0.02");
        svg.appendChild(l);
    }}

    const segmentos = [], pies = [];
    datos.puntos.forEach((p, i) => {{
        const [x, y] = p;
        if (Math.abs(x) > 3.4 || Math.abs(y) > 3.4) {{ segmentos.push(null); pies.push(null); return; }}
        const seg = document.createElementNS(NS, "line");
        seg.setAttribute("stroke", "#CB181D"); seg.setAttribute("stroke-width", "0.014");
        seg.setAttribute("stroke-opacity", "0.55");
        svg.appendChild(seg);
        segmentos.push(seg);

        const pie = document.createElementNS(NS, "circle");
        pie.setAttribute("r", "0.03"); pie.setAttribute("fill", "#122535"); pie.setAttribute("fill-opacity", "0.6");
        svg.appendChild(pie);
        pies.push(pie);

        const dot = document.createElementNS(NS, "circle");
        dot.setAttribute("cx", x); dot.setAttribute("cy", Y(y)); dot.setAttribute("r", "0.045");
        dot.setAttribute("fill", datos.colores[datos.target[i]] || "#636363");
        dot.setAttribute("fill-opacity", "0.65");
        svg.appendChild(dot);
    }});

    const linea = document.createElementNS(NS, "line");
    linea.setAttribute("stroke", "#122535"); linea.setAttribute("stroke-width", "0.045");
    svg.appendChild(linea);

    function interpolar(arr, theta) {{
        const angs = datos.angulos;
        const n = angs.length;
        const paso = angs[1] - angs[0];
        let i = Math.floor(theta / paso);
        if (i >= n - 1) i = n - 2;
        const t = (theta - angs[i]) / paso;
        return arr[i] + (arr[i + 1] - arr[i]) * t;
    }}

    const fillVar = document.getElementById("fillvar-{id_}");
    const valVar = document.getElementById("valvar-{id_}");
    const fillErr = document.getElementById("fillerr-{id_}");
    const valErr = document.getElementById("valerr-{id_}");
    const valAng = document.getElementById("valang-{id_}");
    const slider = document.getElementById("slider-{id_}");
    const varMax = Math.max(...datos.varianza), errMax = Math.max(...datos.error);

    function actualizar(theta) {{
        const rad = theta * Math.PI / 180;
        const ux = Math.cos(rad), uy = Math.sin(rad);
        linea.setAttribute("x1", -3.2 * ux); linea.setAttribute("y1", Y(-3.2 * uy));
        linea.setAttribute("x2", 3.2 * ux); linea.setAttribute("y2", Y(3.2 * uy));

        datos.puntos.forEach((p, i) => {{
            if (!segmentos[i]) return;
            const [x, y] = p;
            const dot = x * ux + y * uy;
            const px = dot * ux, py = dot * uy;
            segmentos[i].setAttribute("x1", x); segmentos[i].setAttribute("y1", Y(y));
            segmentos[i].setAttribute("x2", px); segmentos[i].setAttribute("y2", Y(py));
            pies[i].setAttribute("cx", px); pies[i].setAttribute("cy", Y(py));
        }});

        const varPct = (interpolar(datos.varianza, theta % 180) / varMax) * 100;
        const err = interpolar(datos.error, theta % 180);
        fillVar.style.width = varPct.toFixed(1) + "%";
        valVar.textContent = varPct.toFixed(1).replace(".", ",") + " %";
        const errPct = Math.min(100, (err / errMax) * 100);
        fillErr.style.width = errPct + "%";
        valErr.textContent = err.toFixed(2).replace(".", ",");
        valAng.textContent = Math.round(theta) + "°";
    }}

    slider.addEventListener("input", () => actualizar(parseFloat(slider.value)));
    actualizar(0);

    let animando = false;
    document.getElementById("play-{id_}").addEventListener("click", () => {{
        if (animando) return;
        animando = true;
        const inicio = performance.now();
        const desde = parseFloat(slider.value);
        const duracion = 3500;
        function paso(ahora) {{
            const t = Math.min(1, (ahora - inicio) / duracion);
            const theta = desde + (179 - desde) * t;
            slider.value = theta;
            actualizar(theta);
            if (t < 1) requestAnimationFrame(paso); else animando = false;
        }}
        requestAnimationFrame(paso);
    }});
}})();
</script>
"""


def widget_comparador_metodos(color_bloque, datos, id_="comparador1"):
    """
    Botones para alternar entre 2+ "vistas"/metodos de LOS MISMOS puntos; al clickear, cada
    punto ANIMA su posicion (no cambia de imagen) desde la capa actual a la destino — asi se ve
    que es la misma nube de datos re-arreglada, no graficos distintos. Uso tipico: comparar
    metodos de reduccion de dimensionalidad, o cualquier comparacion "misma data, transformacion
    distinta".

    `datos` = {
      "target": ["grupoA", ...], "colores": {"grupoA": "#hex", ...},
      "capas": {"clave_metodo": [[x,y], ...], ...},   # coordenadas YA normalizadas y sin
                                                        # outliers fuera de [-3.6, 3.6] (ver
                                                        # references/widgets.md, patron 4, para
                                                        # la compresion suave de la cola)
      "metodos": [("clave_metodo", "Etiqueta visible"), ...],  # orden de los botones
    }
    """
    metodos = datos["metodos"]
    payload = {
        "target": datos["target"], "colores": datos["colores"],
        "capas": {clave: datos["capas"][clave] for clave, _ in metodos},
    }
    primera_clave = metodos[0][0]

    botones = "".join(
        f'<button class="boton-metodo{" activo" if clave == primera_clave else ""}" '
        f'data-metodo="{clave}" id="btn-{clave}-{id_}">{etiqueta}</button>'
        for clave, etiqueta in metodos)

    grupos = sorted(set(datos["target"]))
    leyenda = "".join(
        f'<span class="leyenda-item"><i style="background:{datos["colores"][g]}"></i>{g}</span>'
        for g in grupos)

    return f"""
<div class="widget-comparador" id="widget-{id_}" style="--color-activo:{color_bloque}">
  <div class="comparador-botones">{botones}</div>
  <svg viewBox="-3.6 -3.6 7.2 7.2" class="svg-comparador" id="svg-{id_}"></svg>
  <div class="leyenda-recta">{leyenda}</div>
</div>
<script>
(function() {{
    const datos = {json.dumps(payload, ensure_ascii=False)};
    const NS = "http://www.w3.org/2000/svg";
    const svg = document.getElementById("svg-{id_}");
    const primeraClave = "{primera_clave}";

    function Y(y) {{ return -y; }}

    const puntos = [];
    datos.capas[primeraClave].forEach((p, i) => {{
        const c = document.createElementNS(NS, "circle");
        c.setAttribute("r", "0.045");
        c.setAttribute("fill", datos.colores[datos.target[i]] || "#636363");
        c.setAttribute("fill-opacity", "0.6");
        c.setAttribute("cx", p[0]); c.setAttribute("cy", Y(p[1]));
        svg.appendChild(c);
        puntos.push(c);
    }});

    let metodoActual = primeraClave;
    let animando = false;

    function easeInOutQuad(t) {{ return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }}

    function animarA(metodo) {{
        if (metodo === metodoActual || animando) return;
        animando = true;
        const desde = datos.capas[metodoActual];
        const hasta = datos.capas[metodo];
        const inicio = performance.now();
        const duracion = 900;
        function paso(ahora) {{
            const t = Math.min(1, (ahora - inicio) / duracion);
            const te = easeInOutQuad(t);
            puntos.forEach((c, i) => {{
                const [x0, y0] = desde[i], [x1, y1] = hasta[i];
                c.setAttribute("cx", x0 + (x1 - x0) * te);
                c.setAttribute("cy", Y(y0 + (y1 - y0) * te));
            }});
            if (t < 1) {{
                requestAnimationFrame(paso);
            }} else {{
                metodoActual = metodo;
                animando = false;
            }}
        }}
        requestAnimationFrame(paso);
    }}

    document.querySelectorAll("#widget-{id_} .boton-metodo").forEach((b) => {{
        b.addEventListener("click", () => {{
            document.querySelectorAll("#widget-{id_} .boton-metodo").forEach((x) => x.classList.remove("activo"));
            b.classList.add("activo");
            animarA(b.dataset.metodo);
        }});
    }});
}})();
</script>
"""


CSS_INTERACTIVOS = """
.widget-recta { display:flex; gap:2em; align-items:center; justify-content:center; width:100%; }
.svg-col { display:flex; flex-direction:column; align-items:center; gap:.4em; }
.svg-recta { width:19vw; max-width:340px; background:white; }
.leyenda-recta { display:flex; gap:.9em; font-size:.6em; color:#636363; flex-wrap:wrap; justify-content:center; }
.leyenda-item { display:flex; align-items:center; gap:.3em; }
.leyenda-item i { width:.7em; height:.7em; border-radius:50%; display:inline-block; }

.controles-recta { display:flex; flex-direction:column; gap:.7em; width:32%; min-width:260px; }
.fila-slider { display:flex; align-items:center; gap:.6em; }
.slider-angulo { flex:1; }
.boton-girar { background:white; border:1.5px solid; border-radius:8px; padding:.25em .7em;
    font-size:.8em; font-weight:700; cursor:pointer; white-space:nowrap; }
.boton-girar:hover { opacity:.7; }

.medidor { display:flex; flex-direction:column; gap:.15em; }
.medidor-label { font-size:.68em; color:#636363; }
.medidor-barra { background:#ECECEC; border-radius:8px; height:.55em; overflow:hidden; }
.medidor-fill { height:100%; width:0%; }
.medidor-fill.error { background:#CB181D; }
.medidor-valor { font-size:.85em; font-weight:700; }
.medidor-angulo { font-size:.72em; color:#636363; margin:.2em 0 0; }

/* protagonista de la slide: bien grande, no un detalle al costado. Proporcion
   ~1.55:1 para que combine con una camara 3D tipica (ver references/widgets.md,
   patron 2) — NO estirar a lo panoramico, el cubo queda chico igual. */
.plot3d { width:780px; max-width:70%; height:500px; margin:0 auto 1em; flex-shrink:0; }
.biplot-col { display:flex; flex-direction:column; align-items:center; gap:.5em; width:100%;
    flex-shrink:0; }
/* alto FIJO (no %): dentro de un flex column, un hijo con alto en porcentaje
   no tiene una referencia estable y puede terminar comiendose todo el
   espacio, dejando 0px para sus hermanos (le paso a la leyenda una vez). */
.plot-biplot { width:82%; height:430px; margin:0 auto; flex-shrink:0; }
.leyenda-item.apagado { opacity:.35; }

.widget-comparador { display:flex; flex-direction:column; align-items:center; gap:.6em; width:100%; }
.comparador-botones { display:flex; gap:.7em; flex-wrap:wrap; justify-content:center; }
.boton-metodo { background:white; border:1.5px solid #9FB0BD; border-radius:8px;
    padding:.35em 1.15em; font-size:.85em; font-weight:700; cursor:pointer; color:#636363; }
.boton-metodo:hover { opacity:.75; }
.boton-metodo.activo { border-color:var(--color-activo); color:var(--color-activo); background:#f5f5f5; }
.svg-comparador { width:22vw; max-width:390px; background:white; }

.widget-formula { display:flex; flex-direction:column; align-items:center; gap:.55em; width:100%; }
.formula-katex { font-size:1.2em; margin:.15em 0; }
.formula-katex .katex { transition:color .3s ease; }
.formula-bullets { list-style:none; margin:0; padding:0; display:flex; flex-direction:column;
    gap:.4em; width:94%; text-align:left; }
.formula-bullets li { opacity:0; transition:opacity .4s ease; }
.formula-bullets li.fp-visible { opacity:1; }
.fp-hint { font-size:.68em; color:#969696; margin:.2em 0 0; }
"""


def widget_plano_3d(color_bloque, datos, id_="plano3d"):
    """
    Una nube de puntos + un plano/vectores destacados en 3D real (Plotly): se arrastra con el
    mouse para rotar y hacer zoom. Uso tipico: mostrar una estructura (un plano, dos direcciones
    principales) que orbitar-camara-sola no deja explorar.

    `datos` = {
      "puntos": [[x,y,z], ...], "vector1": [vx,vy,vz], "vector2": [vx,vy,vz],
      "etiquetas": ["eje x", "eje y", "eje z"],
    }

    IMPORTANTE (ver references/widgets.md, patron 2): el div vive dentro de una slide oculta al
    momento del render, asi que SIEMPRE hace falta el ResizeObserver de mas abajo — no asumir que
    "porque en esta slide en particular ya funciona sin el" alcanza para las demas.
    """
    puntos = np.array(datos["puntos"])
    v1, v2 = np.array(datos["vector1"]), np.array(datos["vector2"])
    etiquetas = datos["etiquetas"]

    extent = float(np.abs(puntos).max()) * 1.05
    gs = np.linspace(-extent, extent, 12)
    aa, bb = np.meshgrid(gs, gs)
    plano = aa[..., None] * v1 + bb[..., None] * v2

    payload = {
        "x": puntos[:, 0].tolist(), "y": puntos[:, 1].tolist(), "z": puntos[:, 2].tolist(),
        "surf_x": plano[:, :, 0].tolist(), "surf_y": plano[:, :, 1].tolist(),
        "surf_z": plano[:, :, 2].tolist(),
        "flecha1": v1.tolist(), "flecha2": v2.tolist(),
        "etiquetas": etiquetas, "color": color_bloque,
    }

    return f"""
<div id="plot3d-{id_}" class="plot3d"></div>
<script>
(function() {{
    const datos = {json.dumps(payload, ensure_ascii=False)};
    const trazas = [
        {{ type: "scatter3d", mode: "markers", x: datos.x, y: datos.y, z: datos.z,
           marker: {{ size: 3, color: "#3182BD", opacity: 0.65 }}, hoverinfo: "skip", showlegend: false }},
        {{ type: "surface", x: datos.surf_x, y: datos.surf_y, z: datos.surf_z,
           opacity: 0.35, showscale: false,
           colorscale: [[0, datos.color], [1, datos.color]], hoverinfo: "skip" }},
        {{ type: "scatter3d", mode: "lines",
           x: [0, datos.flecha1[0]], y: [0, datos.flecha1[1]], z: [0, datos.flecha1[2]],
           line: {{ color: "#122535", width: 7 }}, hoverinfo: "skip", showlegend: false }},
        {{ type: "scatter3d", mode: "lines",
           x: [0, datos.flecha2[0]], y: [0, datos.flecha2[1]], z: [0, datos.flecha2[2]],
           line: {{ color: "#CB181D", width: 7 }}, hoverinfo: "skip", showlegend: false }},
    ];
    const contenedor = document.getElementById("plot3d-{id_}");
    const layout = {{
        margin: {{ l: 20, r: 20, t: 10, b: 60 }}, paper_bgcolor: "white",
        scene: {{
            xaxis: {{ title: datos.etiquetas[0], showbackground: false }},
            yaxis: {{ title: datos.etiquetas[1], showbackground: false }},
            zaxis: {{ title: datos.etiquetas[2], showbackground: false }},
            camera: {{ eye: {{ x: 1.6, y: -1.7, z: 0.9 }} }},
        }},
    }};
    Plotly.newPlot("plot3d-{id_}", trazas, layout, {{ displayModeBar: false, responsive: true }});
    // El div esta dentro de ".slide" (display:none hasta que se activa): mide
    // 0x0 en el momento de este script, y Plotly cae al tamano por defecto
    // (700x450) anclado arriba a la izquierda si no se corrige esto.
    new ResizeObserver(() => {{
        const w = contenedor.clientWidth, h = contenedor.clientHeight;
        if (w > 0 && h > 0) Plotly.relayout("plot3d-{id_}", {{ width: w, height: h }});
    }}).observe(contenedor);
}})();
</script>
"""


def widget_biplot(color_bloque, datos, id_="biplot1"):
    """
    Scores (puntos, coloreados por grupo, leyenda togglable) + loadings (flechas con nombre) en
    2D — el patron clasico de biplot, con anti-superposicion de etiquetas cuando dos variables
    caen cerca (ver references/widgets.md, patron 3, para el detalle del algoritmo de relajacion).

    `datos` = {
      "grupos": {"grupoA": [[x,y], ...], ...}, "orden": ["grupoA", "grupoB", ...],
      "colores": {"grupoA": "#hex", ...}, "etiquetas_grupo": {"grupoA": "Etiqueta linda", ...},
      "loadings": [["nombre_variable", x, y], ...],  # x,y ya escalados para verse bien junto a los scores
      "eje_x": "PC1 (54%)", "eje_y": "PC2 (17%)",
    }
    """
    orden = datos["orden"]
    loadings = np.array([[l[1], l[2]] for l in datos["loadings"]], dtype=float)
    nombres = [l[0] for l in datos["loadings"]]

    # Relajacion tipo resorte: si dos variables tienen loadings parecidos, sus
    # nombres se separan iterativamente en vez de quedar amontonados en la punta.
    etiquetas_pos = loadings * 1.22
    minimo = float(np.abs(loadings).max()) * 0.19 if len(loadings) else 0.62
    for _ in range(400):
        movido = False
        for i in range(len(etiquetas_pos)):
            for j in range(i + 1, len(etiquetas_pos)):
                diff = etiquetas_pos[i] - etiquetas_pos[j]
                dist = np.linalg.norm(diff)
                if 1e-6 < dist < minimo:
                    empuje = diff / dist * (minimo - dist) * 0.5
                    etiquetas_pos[i] += empuje
                    etiquetas_pos[j] -= empuje
                    movido = True
        if not movido:
            break

    payload = {
        "grupos": datos["grupos"], "orden": orden, "colores": datos["colores"],
        "etiquetas_grupo": datos["etiquetas_grupo"],
        "flechas": [[nombres[i], round(float(loadings[i, 0]), 3), round(float(loadings[i, 1]), 3),
                    round(float(etiquetas_pos[i, 0]), 3), round(float(etiquetas_pos[i, 1]), 3)]
                   for i in range(len(nombres))],
        "ejex": datos["eje_x"], "ejey": datos["eje_y"],
    }

    leyenda = "".join(
        f'<span class="leyenda-item leyenda-click" data-i="{i}" style="cursor:pointer">'
        f'<i style="background:{datos["colores"][g]}"></i>{datos["etiquetas_grupo"][g]}</span>'
        for i, g in enumerate(orden))

    return f"""
<div class="biplot-col">
  <div id="biplot-{id_}" class="plot-biplot"></div>
  <div class="leyenda-recta">{leyenda}</div>
</div>
<script>
(function() {{
    const datos = {json.dumps(payload, ensure_ascii=False)};
    const trazas = datos.orden.map((g) => {{
        const pts = datos.grupos[g];
        return {{ type: "scatter", mode: "markers", name: datos.etiquetas_grupo[g],
                 x: pts.map((p) => p[0]), y: pts.map((p) => p[1]),
                 marker: {{ size: 5, color: datos.colores[g], opacity: 0.5 }} }};
    }});
    // Flechas (sin texto: solo la punta) + etiquetas en posiciones YA separadas
    // (precalculadas en Python) para que no se amontonen cuando dos variables
    // casi coinciden en direccion.
    const flechas = datos.flechas.map(([nombre, dx, dy]) => ({{
        x: dx, y: dy, ax: 0, ay: 0, xref: "x", yref: "y", axref: "x", ayref: "y",
        showarrow: true, arrowhead: 2, arrowsize: 1, arrowwidth: 1.6,
        arrowcolor: "{color_bloque}", text: "",
    }}));
    const nombres = datos.flechas.map(([nombre, dx, dy, lx, ly]) => ({{
        x: lx, y: ly, xref: "x", yref: "y", showarrow: false, text: nombre,
        font: {{ size: 11, color: "{color_bloque}" }},
        xanchor: lx >= dx ? "left" : "right",
    }}));
    // linea guia fina cuando la etiqueta se desplazo lejos de la punta real.
    const guias = datos.flechas.filter(([nombre, dx, dy, lx, ly]) =>
        Math.hypot(lx - dx, ly - dy) > 0.35
    ).map(([nombre, dx, dy, lx, ly]) => ({{
        type: "line", x0: dx, y0: dy, x1: lx, y1: ly, xref: "x", yref: "y",
        line: {{ color: "{color_bloque}", width: 0.75, dash: "dot" }},
    }}));
    const contenedorPlot = document.getElementById("biplot-{id_}");
    const layout = {{
        margin: {{ l: 45, r: 32, t: 10, b: 45 }}, paper_bgcolor: "white", plot_bgcolor: "white",
        showlegend: false,
        xaxis: {{ title: datos.ejex, zeroline: true, zerolinecolor: "#ccc", gridcolor: "#eee" }},
        yaxis: {{ title: datos.ejey, zeroline: true, zerolinecolor: "#ccc", gridcolor: "#eee" }},
        annotations: flechas.concat(nombres),
        shapes: guias,
    }};
    // Leyenda HTML propia (no la de Plotly, que puede caer fuera del div
    // declarado y tapar texto de la slide): showlegend:false + toggle a mano.
    Plotly.newPlot("biplot-{id_}", trazas, layout, {{
        responsive: true,
        displayModeBar: "hover",
        modeBarButtonsToRemove: ["lasso2d", "select2d", "autoScale2d", "toImage"],
        displaylogo: false,
    }});

    const contenedorLeyenda = contenedorPlot.closest(".biplot-col");
    contenedorLeyenda.querySelectorAll(".leyenda-click").forEach((el) => {{
        el.addEventListener("click", () => {{
            const i = parseInt(el.dataset.i, 10);
            const oculto = el.classList.toggle("apagado");
            Plotly.restyle("biplot-{id_}", {{ visible: oculto ? "legendonly" : true }}, [i]);
        }});
    }});
    // Ver widget_plano_3d: mismo gotcha de tamano-en-slide-oculta.
    new ResizeObserver(() => Plotly.Plots.resize("biplot-{id_}")).observe(contenedorPlot);
}})();
</script>
"""


def widget_formula_pasos(formula_tex, pasos, id_="formula1"):
    """
    Revela una formula grupo de simbolos por grupo, cada uno con su propio color — marcados en
    el TeX con \\htmlClass{{grupo-NOMBRE}}{{...}}. El texto de abajo va acumulando, en el MISMO
    color, la explicacion de cada grupo (el color se hornea directo en su TeX via \\textcolor,
    asi que el llamador debe envolver ahi el simbolo correspondiente — ver references/widgets.md
    patron 5 para el porque).

    Sin boton: se avanza con la flecha derecha (retrocede con la izquierda), igual que se pasa
    de diapositiva — el manejador global de teclado (ver comun.py armar_js) consulta
    window.__fpAvanzar/__fpRetroceder antes de cambiar de slide, y solo cambia de slide una vez
    que ya no queda nada por revelar.

    `pasos` es una lista de (nombre_de_grupo, color, html_de_la_explicacion), en el orden en que
    se quiere ir revelando. Elegir colores DISTINTOS entre si y distintos del color del bloque
    de esa slide (que ya se usa en otro lado — titulo, alert()).
    """
    grupos = [g for g, _, _ in pasos]
    colores = [c for _, c, _ in pasos]
    bullets_html = "".join(
        f'<li class="fp-oculto" data-grupo="{g}">{texto}</li>' for g, _, texto in pasos)

    return f"""
<div class="widget-formula" id="widget-{id_}">
  <div class="formula-katex" id="formula-{id_}"></div>
  <ol class="formula-bullets" id="bullets-{id_}">{bullets_html}</ol>
  <p class="fp-hint">Usá <strong>→</strong> para ir revelando los términos.</p>
</div>
<script>
(function() {{
    const grupos = {json.dumps(grupos)};
    const colores = {json.dumps(colores)};
    const formulaEl = document.getElementById("formula-{id_}");
    const slideEl = formulaEl.closest(".slide");
    const bullets = document.querySelectorAll("#bullets-{id_} li");
    let paso = 0;

    function aplicar() {{
        grupos.forEach((g, i) => {{
            formulaEl.querySelectorAll(".grupo-" + g).forEach((el) => {{
                el.style.color = i < paso ? colores[i] : "";
                el.style.fontWeight = i < paso ? "700" : "";
            }});
        }});
        bullets.forEach((li, i) => li.classList.toggle("fp-visible", i < paso));
    }}

    function avanzar(slideActivo) {{
        if (slideActivo !== slideEl || paso >= grupos.length) return false;
        paso++; aplicar(); return true;
    }}
    function retroceder(slideActivo) {{
        if (slideActivo !== slideEl || paso <= 0) return false;
        paso--; aplicar(); return true;
    }}
    (window.__fpAvanzar = window.__fpAvanzar || []).push(avanzar);
    (window.__fpRetroceder = window.__fpRetroceder || []).push(retroceder);

    // katex.render() debe correr DESPUES de que la libreria este cargada: el
    // script de KaTeX se inyecta al final del documento (para no demorar el
    // primer paint), asi que en el momento en que este script corre (en medio
    // del HTML de la slide) `katex` todavia no existe. DOMContentLoaded esta
    // garantizado por spec a disparar solo despues de TODOS los scripts
    // sincronicos del documento (incluido el de KaTeX) — no usar setTimeout(0),
    // es una carrera que a veces pierde (ver references/arquitectura.md).
    function renderFormula() {{
        katex.render(String.raw`{formula_tex}`, formulaEl,
            {{ throwOnError: false, trust: true, displayMode: true }});
        aplicar();
    }}
    if (window.katex) {{ renderFormula(); }}
    else {{ document.addEventListener("DOMContentLoaded", renderFormula); }}
}})();
</script>
"""

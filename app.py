import streamlit as st

# ─── Configuración de la página ──────────────────────────────────
st.set_page_config(
    page_title="Expedición Heurística",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─── Estilos ─────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 20% 0%, #1e293b 0%, #0f172a 55%, #020617 100%);
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { display: none; }

    /* ---------- HUD superior ---------- */
    .hud {
        display: grid;
        grid-template-columns: 1fr 1.4fr 1fr;
        gap: 12px;
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 14px;
        padding: 14px 18px;
        backdrop-filter: blur(10px);
        margin-bottom: 18px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35);
    }
    .hud-block { display: flex; flex-direction: column; gap: 6px; }
    .hud-label {
        font-size: 10px; font-weight: 700; letter-spacing: 1.5px;
        color: #94a3b8; text-transform: uppercase;
    }
    .hud-value {
        display: flex; align-items: center; gap: 6px;
        color: #f1f5f9; font-weight: 700; font-size: 15px;
    }
    .score-num { color: #38bdf8; font-size: 18px; font-family: monospace; }
    .racha-num { color: #fb923c; font-size: 18px; font-family: monospace; }

    /* ---------- Tarjeta de pregunta ---------- */
    .question-card {
        background: linear-gradient(145deg, #1e293b 0%, #172033 100%);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-left: 5px solid #38bdf8;
        border-radius: 14px;
        padding: 22px 24px;
        margin: 10px 0 22px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        position: relative;
        overflow: hidden;
    }
    .question-card::before {
        content: "";
        position: absolute; top: 0; right: 0;
        width: 180px; height: 180px;
        background: radial-gradient(circle, rgba(56,189,248,0.12), transparent 70%);
        pointer-events: none;
    }
    .q-header {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 14px;
    }
    .badge-topic {
        background: linear-gradient(90deg, #0284c7, #0ea5e9);
        color: white; font-size: 10px; font-weight: 700;
        padding: 5px 12px; border-radius: 999px;
        letter-spacing: 1px; text-transform: uppercase;
    }
    .q-counter {
        font-family: monospace; font-size: 12px; color: #64748b;
        letter-spacing: 1px;
    }
    .q-text {
        color: #f8fafc; font-size: 17px; font-weight: 600;
        line-height: 1.55;
    }

    /* ---------- Botones de opción ---------- */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1e293b 0%, #293548 100%);
        color: #e2e8f0;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 14px 18px;
        text-align: left;
        font-weight: 500;
        font-size: 14px;
        transition: all 0.18s ease;
        margin-bottom: 6px;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #293548 0%, #3b4a63 100%);
        border-color: #38bdf8;
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(56, 189, 248, 0.25);
        color: #ffffff;
    }
    .stButton > button:active { transform: translateX(2px); }

    /* Botón primario (Confirmar / Siguiente) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0284c7 0%, #0ea5e9 100%);
        color: white;
        border: none;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-align: center;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 100%);
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.4);
        transform: translateY(-2px);
    }

    /* ---------- Feedback ---------- */
    .feedback {
        border-radius: 12px;
        padding: 18px 22px;
        margin: 16px 0;
        border-left: 5px solid;
        animation: slideIn 0.35s ease;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .feedback.correct {
        background: linear-gradient(135deg, rgba(22,163,74,0.15), rgba(21,128,61,0.08));
        border-color: #22c55e;
    }
    .feedback.incorrect {
        background: linear-gradient(135deg, rgba(220,38,38,0.15), rgba(153,27,27,0.08));
        border-color: #ef4444;
    }
    .feedback-title {
        font-size: 13px; font-weight: 800; letter-spacing: 1.5px;
        text-transform: uppercase; margin-bottom: 6px;
    }
    .feedback.correct .feedback-title { color: #4ade80; }
    .feedback.incorrect .feedback-title { color: #f87171; }
    .feedback-points {
        font-family: monospace; font-size: 22px; font-weight: 700;
        margin-bottom: 10px;
    }
    .feedback.correct .feedback-points { color: #22c55e; }
    .feedback.incorrect .feedback-points { color: #ef4444; }
    .feedback-text {
        color: #cbd5e1; font-size: 14px; line-height: 1.6;
    }

    /* ---------- Pantalla final ---------- */
    .final-card {
        background: linear-gradient(145deg, #1e293b 0%, #172033 100%);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
        margin: 20px 0;
    }
    .final-title {
        font-size: 26px; font-weight: 800; color: #f8fafc;
        letter-spacing: 1px; margin-bottom: 8px;
    }
    .final-subtitle {
        font-size: 13px; color: #94a3b8; letter-spacing: 2px;
        text-transform: uppercase; margin-bottom: 24px;
    }
    .final-rank {
        display: inline-block;
        padding: 10px 22px; border-radius: 999px;
        background: linear-gradient(90deg, #0284c7, #38bdf8);
        color: white; font-weight: 700; font-size: 14px;
        letter-spacing: 1px; margin-bottom: 24px;
    }
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        margin-top: 20px;
    }
    .stat-cell {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 10px;
    }
    .stat-value {
        font-family: monospace; font-size: 22px; font-weight: 700;
        color: #38bdf8; margin-bottom: 4px;
    }
    .stat-label {
        font-size: 10px; color: #94a3b8; letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    /* Ocultar radio nativo, no lo usamos */
    .stRadio { display: none; }
</style>
""", unsafe_allow_html=True)


# ─── Banco de preguntas ──────────────────────────────────────────
PREGUNTAS = [
    {
        "tema": "Concepto Base",
        "pregunta": "¿Cuál es la definición formal de una 'heurística' en Inteligencia Artificial?",
        "opciones": [
            "Un algoritmo exacto y determinista que siempre halla la solución más barata.",
            "Una regla o función que estima qué tan cerca está un estado de la meta sin garantizar exactitud.",
            "Un método ciego que recorre obligatoriamente cada nodo del espacio de estados.",
            "Una técnica de compresión de memoria para reducir el tamaño de los árboles de búsqueda.",
        ],
        "correcta": 1,
        "explicacion": "Una heurística es una estimación orientadora: no garantiza exactitud matemática, pero descarta ramas poco prometedoras ahorrando tiempo computacional.",
    },
    {
        "tema": "Espacio de Estados",
        "pregunta": "¿Por qué es indispensable usar heurísticas en problemas como el Ajedrez o el Rompecabezas de 8?",
        "opciones": [
            "Porque evitan la explosión combinatoria reduciendo drásticamente el espacio a explorar.",
            "Porque los lenguajes de programación no pueden usar ciclos while en grafos grandes.",
            "Porque garantizan que el camino encontrado no tenga ninguna curva ni retroceso.",
            "Porque eliminan por completo la necesidad de almacenar nodos en la memoria RAM.",
        ],
        "correcta": 0,
        "explicacion": "En problemas con millones de estados posibles, una búsqueda ciega tardaría años en completarse. La heurística poda caminos y hace el problema tratable.",
    },
    {
        "tema": "Ejemplos de h(n)",
        "pregunta": "En el rompecabezas de 8 piezas, ¿qué mide la heurística de 'Distancia Manhattan'?",
        "opciones": [
            "El número total de piezas que ya están en su posición final correcta.",
            "La distancia euclidiana en línea diagonal directa entre el espacio vacío y el centro.",
            "La suma de las distancias horizontales y verticales de cada pieza hasta su casilla objetivo.",
            "La cantidad de movimientos legales que el jugador puede realizar en el siguiente turno.",
        ],
        "correcta": 2,
        "explicacion": "La Distancia Manhattan suma los bloques (|x1 - x2| + |y1 - y2|) que le faltan a cada pieza para llegar a su destino, asumiendo que no chocan.",
    },
    {
        "tema": "Función de Evaluación",
        "pregunta": "En la fórmula f(n) = g(n) + h(n), ¿qué representa cada componente?",
        "opciones": [
            "g(n) es el costo estimado a la meta y h(n) es el costo real acumulado.",
            "g(n) es el costo real acumulado desde el inicio y h(n) es el costo estimado a la meta.",
            "g(n) es el número de ramas generadas y h(n) es el límite de profundidad.",
            "g(n) y h(n) son valores aleatorios para evitar atascos en la búsqueda.",
        ],
        "correcta": 1,
        "explicacion": "g(n) mira al pasado (lo que ya te costó llegar hasta ahí) y h(n) mira al futuro (la estimación de lo que falta para llegar a la meta).",
    },
    {
        "tema": "Cálculo Numérico f(n)",
        "pregunta": "Si para llegar a la Ciudad B ya recorriste 25 km (g=25) y su distancia aérea a la meta es 40 km (h=40), ¿cuál es su f(B)?",
        "opciones": ["f(B) = 15 km", "f(B) = 65 km", "f(B) = 1000 km", "f(B) = 50 km"],
        "correcta": 1,
        "explicacion": "f(B) = g(B) + h(B) = 25 + 40 = 65. El algoritmo siempre expandirá primero el nodo que tenga el menor valor de f(n).",
    },
    {
        "tema": "Admisibilidad",
        "pregunta": "¿Qué condición matemática exige la 'Admisibilidad' de una heurística?",
        "opciones": [
            "h(n) jamás debe sobreestimar el costo real: h(n) <= costo_real(n, meta).",
            "h(n) debe ser siempre el doble del costo acumulado para prevenir riesgos.",
            "h(n) debe ser exactamente igual a 0 en todos los nodos del árbol.",
            "h(n) debe aumentar exponencialmente en cada nivel de profundidad.",
        ],
        "correcta": 0,
        "explicacion": "Una heurística admisible es siempre 'optimista'. Al nunca sobreestimar el costo restante, le garantiza al algoritmo A* que encontrará la solución óptima.",
    },
    {
        "tema": "No Informada vs. Informada",
        "pregunta": "¿Qué ventaja tiene una búsqueda informada frente a BFS (Amplitud) o DFS (Profundidad)?",
        "opciones": [
            "No necesita verificar si un nodo ya fue visitado anteriormente.",
            "Posee una función evaluadora que le da dirección o 'brújula' hacia la meta.",
            "Utiliza menos memoria RAM que una sola variable entera.",
            "Funciona únicamente en árboles binarios perfectamente balanceados.",
        ],
        "correcta": 1,
        "explicacion": "BFS y DFS exploran a ciegas por estructura. La búsqueda informada aprovecha el conocimiento del dominio (h) para priorizar los caminos más prometedores.",
    },
    {
        "tema": "Búsqueda Voraz",
        "pregunta": "¿Por qué la Búsqueda Voraz (Greedy Best-First Search) NO siempre es óptima?",
        "opciones": [
            "Porque suma el costo g(n) demasiadas veces provocando desbordamiento.",
            "Porque solo evalúa h(n), dejándose llevar por la cercanía aparente sin importar el costo real acumulado.",
            "Porque solo puede retroceder y nunca avanza hacia adelante.",
            "Porque descarta la meta en cuanto la encuentra en la frontera.",
        ],
        "correcta": 1,
        "explicacion": "La búsqueda voraz es miope: elige lo que parece más cercano ahora (menor h), pero puede meterte en un desvío larguísimo o en un callejón sin salida.",
    },
    {
        "tema": "Ascenso de Colinas",
        "pregunta": "¿Cuál es el principal peligro del algoritmo de Ascenso de Colinas (Hill Climbing)?",
        "opciones": [
            "Quedar atrapado en un óptimo local (un pico que es más alto que sus vecinos, pero no el más alto del mapa).",
            "Gastar toda la memoria RAM almacenando los nodos anteriores.",
            "Calcular integrales dobles en cada paso del proceso.",
            "Confundir la lista abierta con la lista cerrada en cada iteración.",
        ],
        "correcta": 0,
        "explicacion": "Como solo avanza si el vecino inmediato mejora la puntuación, si llega a una colina secundaria donde todos los pasos bajan, se detiene creyendo que triunfó.",
    },
    {
        "tema": "Búsqueda en Haz (Beam Search)",
        "pregunta": "¿En qué consiste la técnica de Búsqueda en Haz y cuál es su parámetro 'k'?",
        "opciones": [
            "Conserva solo los 'k' mejores nodos en cada nivel, sacrificando optimalidad a cambio de ahorrar memoria.",
            "Multiplica la heurística por 'k' veces para acelerar el procesamiento gráfico.",
            "Divide el grafo en 'k' dimensiones espaciales paralelas e independientes.",
            "Repite la búsqueda 'k' veces desde el nodo inicial de forma aleatoria.",
        ],
        "correcta": 0,
        "explicacion": "Beam Search poda radicalmente la frontera: solo retiene los k estados más prometedores por nivel, evitando que la memoria colapse en grafos gigantes.",
    },
]

PUNTOS_BASE = 100
BONO_RACHA = 20
MAX_PUNTOS = len(PREGUNTAS) * PUNTOS_BASE + BONO_RACHA * (len(PREGUNTAS) - 1)


# ─── Estado inicial ──────────────────────────────────────────────
DEFAULTS = {
    "indice": 0,
    "puntos": 0,
    "vidas": 3,
    "racha": 0,
    "max_racha": 0,
    "respondido": False,
    "feedback": None,
    "terminado": False,
    "seleccion": None,
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reset_juego():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v


# ─── Componentes gráficos (SVG) ──────────────────────────────────
def svg_corazon(lleno: bool) -> str:
    fill = "#ef4444" if lleno else "#1e293b"
    stroke = "#7f1d1d" if lleno else "#475569"
    return (
        f'<svg width="20" height="20" viewBox="0 0 24 24" style="display:inline-block;">'
        f'<path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3'
        f'c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5'
        f'c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        f'</svg>'
    )


def render_vidas(vidas: int) -> str:
    return " ".join(svg_corazon(i < vidas) for i in range(3))


def render_barra_puntos(puntos: int, max_puntos: int) -> str:
    pct = min(100.0, (puntos / max_puntos) * 100) if max_puntos else 0
    return (
        '<div style="background:#0f172a;border:1px solid #334155;border-radius:999px;'
        'height:8px;overflow:hidden;margin-top:4px;">'
        f'<div style="background:linear-gradient(90deg,#0284c7,#38bdf8);height:100%;'
        f'width:{pct:.1f}%;transition:width 0.6s ease;"></div></div>'
    )


def render_mapa(actual: int, total: int) -> str:
    """Mapa SVG animado del camino de nodos."""
    W, H = 720, 120
    margin = 45
    y = 60
    step = (W - 2 * margin) / (total - 1)
    traveled_x = margin + step * actual

    parts = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
             f'style="width:100%;height:auto;display:block;">']

    # Definiciones (gradientes y filtros)
    parts.append(f'''<defs>
        <linearGradient id="progGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#22c55e"/>
            <stop offset="100%" stop-color="#38bdf8"/>
        </linearGradient>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="3" result="blur"/>
            <feMerge>
                <feMergeNode in="blur"/>
                <feMergeNode in="SourceGraphic"/>
            </feMerge>
        </filter>
    </defs>''')

    # Línea base (futura)
    parts.append(
        f'<line x1="{margin}" y1="{y}" x2="{W - margin}" y2="{y}" '
        f'stroke="#1e293b" stroke-width="6" stroke-linecap="round"/>'
    )
    parts.append(
        f'<line x1="{margin}" y1="{y}" x2="{W - margin}" y2="{y}" '
        f'stroke="#334155" stroke-width="6" stroke-linecap="round" '
        f'stroke-dasharray="2 10"/>'
    )

    # Línea recorrida
    if actual > 0:
        parts.append(
            f'<line x1="{margin}" y1="{y}" x2="{traveled_x}" y2="{y}" '
            f'stroke="url(#progGrad)" stroke-width="6" stroke-linecap="round" '
            f'filter="url(#glow)"/>'
        )

    # Nodos
    for i in range(total):
        cx = margin + step * i
        if i < actual:
            parts.append(f'<circle cx="{cx}" cy="{y}" r="17" fill="#22c55e" '
                         f'stroke="#14532d" stroke-width="2"/>')
            parts.append(f'<path d="M{cx-6} {y} l4 4 l8 -8" fill="none" '
                         f'stroke="#052e16" stroke-width="2.5" stroke-linecap="round" '
                         f'stroke-linejoin="round"/>')
        elif i == actual:
            # Anillo pulsante
            parts.append(
                f'<circle cx="{cx}" cy="{y}" r="17" fill="none" '
                f'stroke="#38bdf8" stroke-width="2">'
                f'<animate attributeName="r" values="17;30" dur="1.6s" '
                f'repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0.9;0" dur="1.6s" '
                f'repeatCount="indefinite"/>'
                f'</circle>'
            )
            parts.append(f'<circle cx="{cx}" cy="{y}" r="17" fill="#0284c7" '
                         f'stroke="#38bdf8" stroke-width="3" filter="url(#glow)"/>')
            parts.append(f'<text x="{cx}" y="{y+5}" font-family="monospace" '
                         f'font-size="13" font-weight="700" fill="white" '
                         f'text-anchor="middle">{i+1}</text>')
        else:
            parts.append(f'<circle cx="{cx}" cy="{y}" r="17" fill="#0f172a" '
                         f'stroke="#475569" stroke-width="2"/>')
            parts.append(f'<text x="{cx}" y="{y+5}" font-family="monospace" '
                         f'font-size="13" font-weight="700" fill="#64748b" '
                         f'text-anchor="middle">{i+1}</text>')

    # Etiquetas Inicio / Meta
    parts.append(
        f'<text x="{margin}" y="{y-32}" font-family="monospace" font-size="10" '
        f'fill="#64748b" text-anchor="middle" letter-spacing="1">INICIO</text>'
    )
    parts.append(
        f'<text x="{W - margin}" y="{y-32}" font-family="monospace" font-size="10" '
        f'fill="#64748b" text-anchor="middle" letter-spacing="1">META</text>'
    )

    parts.append('</svg>')
    return ''.join(parts)


# ─── Renderizado: pantalla final ─────────────────────────────────
if st.session_state.terminado:
    gano = st.session_state.vidas > 0
    pct = st.session_state.puntos / MAX_PUNTOS

    if gano:
        if pct >= 0.9:
            rango = "MAESTRO DE LA BUSQUEDA OPTIMA (A*)"
        elif pct >= 0.6:
            rango = "EXPLORADOR HEURISTICO CALIFICADO"
        else:
            rango = "APRENDIZ DE BUSQUEDA INFORMADA"
        titulo = "MISION COMPLETADA"
        color_titulo = "#22c55e"
    else:
        rango = "SIN RUTA DISPONIBLE"
        titulo = "MISION FALLIDA"
        color_titulo = "#ef4444"

    st.markdown(f"""
    <div class="final-card">
        <div class="final-title" style="color:{color_titulo};">{titulo}</div>
        <div class="final-subtitle">Expedicion Heuristica</div>
        <div class="final-rank">{rango}</div>
        <div class="stat-grid">
            <div class="stat-cell">
                <div class="stat-value">{st.session_state.puntos}</div>
                <div class="stat-label">Puntos / {MAX_PUNTOS}</div>
            </div>
            <div class="stat-cell">
                <div class="stat-value">{st.session_state.max_racha}</div>
                <div class="stat-label">Racha Maxima</div>
            </div>
            <div class="stat-cell">
                <div class="stat-value">{max(0, st.session_state.vidas)} / 3</div>
                <div class="stat-label">Vidas Restantes</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Barra de progreso de puntuación final
    st.markdown(render_barra_puntos(st.session_state.puntos, MAX_PUNTOS),
                unsafe_allow_html=True)

    st.write("")
    if st.button("VOLVER A JUGAR", type="primary", use_container_width=True):
        reset_juego()
        st.rerun()

# ─── Renderizado: pantalla de juego ──────────────────────────────
else:
    idx = st.session_state.indice
    q = PREGUNTAS[idx]
    total = len(PREGUNTAS)

    # HUD superior
    st.markdown(f"""
    <div class="hud">
        <div class="hud-block">
            <div class="hud-label">Vidas</div>
            <div class="hud-value">{render_vidas(st.session_state.vidas)}</div>
        </div>
        <div class="hud-block">
            <div class="hud-label">Puntuacion</div>
            <div class="hud-value"><span class="score-num">{st.session_state.puntos:04d}</span>
                <span style="color:#64748b;font-size:12px;">/ {MAX_PUNTOS}</span></div>
            {render_barra_puntos(st.session_state.puntos, MAX_PUNTOS)}
        </div>
        <div class="hud-block">
            <div class="hud-label">Racha</div>
            <div class="hud-value"><span class="racha-num">{st.session_state.racha:02d}</span>
                <span style="color:#64748b;font-size:12px;">seguidas</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mapa SVG animado
    st.markdown(render_mapa(idx, total), unsafe_allow_html=True)

    # Tarjeta de la pregunta
    st.markdown(f"""
    <div class="question-card">
        <div class="q-header">
            <span class="badge-topic">{q['tema']}</span>
            <span class="q-counter">NODO {idx + 1:02d} / {total:02d}</span>
        </div>
        <div class="q-text">{q['pregunta']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── FASE 1: responder ────────────────────────────────────────
    if not st.session_state.respondido:
        letras = ["A", "B", "C", "D"]
        for i, op in enumerate(q["opciones"]):
            if st.button(f"{letras[i]}   |   {op}",
                         key=f"opt_{idx}_{i}",
                         use_container_width=True):
                es_correcta = (i == q["correcta"])

                if es_correcta:
                    st.session_state.racha += 1
                    bono = BONO_RACHA if st.session_state.racha > 1 else 0
                    ganados = PUNTOS_BASE + bono
                    st.session_state.puntos += ganados
                    st.session_state.max_racha = max(
                        st.session_state.max_racha, st.session_state.racha
                    )
                else:
                    st.session_state.vidas -= 1
                    st.session_state.racha = 0
                    ganados = 0

                st.session_state.feedback = {
                    "correcto": es_correcta,
                    "ganados": ganados,
                    "explicacion": q["explicacion"],
                }
                st.session_state.respondido = True
                st.rerun()

    # ── FASE 2: feedback + siguiente ─────────────────────────────
    else:
        fb = st.session_state.feedback
        if fb["correcto"]:
            st.markdown(f"""
            <div class="feedback correct">
                <div class="feedback-title">Movimiento Optimo</div>
                <div class="feedback-points">+{fb['ganados']} puntos</div>
                <div class="feedback-text">{fb['explicacion']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="feedback incorrect">
                <div class="feedback-title">Ruta Suboptima Detectada</div>
                <div class="feedback-points">-1 vida</div>
                <div class="feedback-text">{fb['explicacion']}</div>
            </div>
            """, unsafe_allow_html=True)

        sin_vidas = st.session_state.vidas <= 0
        ultimo_nodo = st.session_state.indice >= total - 1
        texto_btn = "VER RESULTADOS" if (sin_vidas or ultimo_nodo) else "SIGUIENTE NODO"

        if st.button(texto_btn, type="primary", use_container_width=True):
            if sin_vidas or ultimo_nodo:
                st.session_state.terminado = True
            else:
                st.session_state.indice += 1
            st.session_state.respondido = False
            st.session_state.feedback = None
            st.rerun()
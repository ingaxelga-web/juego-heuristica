import streamlit as st

# ─── Configuración ───────────────────────────────────────────────
st.set_page_config(
    page_title="Expedición Heurística: En Busca del Óptimo",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Estilos (selectores actualizados para Streamlit moderno) ────
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stHeader"] { background: transparent; }

    .hud-box {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 12px 18px;
        backdrop-filter: blur(8px);
        margin-bottom: 15px;
    }
    .question-card {
        background: #1e293b;
        border-left: 5px solid #3b82f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .badge-topic {
        background: #3b82f6;
        color: white;
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 999px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        display: inline-block;
        margin-bottom: 8px;
    }
    .stRadio > div {
        background: rgba(15, 23, 42, 0.5);
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Banco de preguntas (idéntico) ───────────────────────────────
PREGUNTAS = [
    {
        "tema": "Concepto Base",
        "pregunta": "¿Cuál es la definición formal de una 'heurística' en Inteligencia Artificial?",
        "opciones": [
            "Un algoritmo exacto y determinista que siempre halla la solución más barata.",
            "Una regla o función que estima qué tan cerca está un estado de la meta sin garantizar exactitud.",
            "Un método ciego que recorre obligatoriamente cada nodo del espacio de estados.",
            "Una técnica de compresión de memoria para reducir el tamaño de los árboles de búsqueda."
        ],
        "correcta": 1,
        "explicacion": "Una heurística es una estimación orientadora: no garantiza exactitud matemática, pero descarta ramas poco prometedoras ahorrando tiempo computacional."
    },
    {
        "tema": "Espacio de Estados",
        "pregunta": "¿Por qué es indispensable usar heurísticas en problemas como el Ajedrez o el Rompecabezas de 8?",
        "opciones": [
            "Porque evitan la explosión combinatoria reduciendo drásticamente el espacio a explorar.",
            "Porque los lenguajes de programación no pueden usar ciclos `while` en grafos grandes.",
            "Porque garantizan que el camino encontrado no tenga ninguna curva ni retroceso.",
            "Porque eliminan por completo la necesidad de almacenar nodos en la memoria RAM."
        ],
        "correcta": 0,
        "explicacion": "En problemas con millones de estados posibles, una búsqueda ciega tardaría años en completarse. La heurística poda caminos y hace el problema tratable."
    },
    {
        "tema": "Ejemplos de h(n)",
        "pregunta": "En el rompecabezas de 8 piezas, ¿qué mide la heurística de 'Distancia Manhattan'?",
        "opciones": [
            "El número total de piezas que ya están en su posición final correcta.",
            "La distancia euclidiana en línea diagonal directa entre el espacio vacío y el centro.",
            "La suma de las distancias horizontales y verticales de cada pieza hasta su casilla objetivo.",
            "La cantidad de movimientos legales que el jugador puede realizar en el siguiente turno."
        ],
        "correcta": 2,
        "explicacion": "La Distancia Manhattan suma los bloques (|x1 - x2| + |y1 - y2|) que le faltan a cada pieza para llegar a su destino, asumiendo que no chocan."
    },
    {
        "tema": "Función de Evaluación",
        "pregunta": "En la fórmula f(n) = g(n) + h(n), ¿qué representa cada componente?",
        "opciones": [
            "g(n) es el costo estimado a la meta y h(n) es el costo real acumulado.",
            "g(n) es el costo real acumulado desde el inicio y h(n) es el costo estimado a la meta.",
            "g(n) es el número de ramas generadas y h(n) es el límite de profundidad.",
            "g(n) y h(n) son valores aleatorios para evitar atascos en la búsqueda."
        ],
        "correcta": 1,
        "explicacion": "g(n) mira al pasado (lo que ya te costó llegar hasta ahí) y h(n) mira al futuro (la estimación de lo que falta para llegar a la meta)."
    },
    {
        "tema": "Cálculo Numérico f(n)",
        "pregunta": "Si para llegar a la Ciudad B ya recorriste 25 km (g=25) y su distancia aérea a la meta es 40 km (h=40), ¿cuál es su f(B)?",
        "opciones": ["f(B) = 15 km", "f(B) = 65 km", "f(B) = 1000 km", "f(B) = 50 km"],
        "correcta": 1,
        "explicacion": "f(B) = g(B) + h(B) = 25 + 40 = 65. El algoritmo siempre expandirá primero el nodo que tenga el menor valor de f(n)."
    },
    {
        "tema": "Admisibilidad",
        "pregunta": "¿Qué condición matemática exige la 'Admisibilidad' de una heurística?",
        "opciones": [
            "h(n) jamás debe sobreestimar el costo real: h(n) ≤ costo_real(n, meta).",
            "h(n) debe ser siempre el doble del costo acumulado para prevenir riesgos.",
            "h(n) debe ser exactamente igual a 0 en todos los nodos del árbol.",
            "h(n) debe aumentar exponencialmente en cada nivel de profundidad."
        ],
        "correcta": 0,
        "explicacion": "Una heurística admisible es siempre 'optimista'. Al nunca sobreestimar el costo restante, le garantiza al algoritmo A* que encontrará la solución óptima."
    },
    {
        "tema": "No Informada vs. Informada",
        "pregunta": "¿Qué ventaja tiene una búsqueda informada frente a BFS (Amplitud) o DFS (Profundidad)?",
        "opciones": [
            "No necesita verificar si un nodo ya fue visitado anteriormente.",
            "Posee una función evaluadora que le da dirección o 'brújula' hacia la meta.",
            "Utiliza menos memoria RAM que una sola variable entera.",
            "Funciona únicamente en árboles binarios perfectamente balanceados."
        ],
        "correcta": 1,
        "explicacion": "BFS y DFS exploran a ciegas por estructura. La búsqueda informada aprovecha el conocimiento del dominio (h) para priorizar los caminos más prometedores."
    },
    {
        "tema": "Búsqueda Voraz",
        "pregunta": "¿Por qué la Búsqueda Voraz (Greedy Best-First Search) NO siempre es óptima?",
        "opciones": [
            "Porque suma el costo g(n) demasiadas veces provocando desbordamiento.",
            "Porque solo evalúa h(n), dejándose llevar por la cercanía aparente sin importar el costo real acumulado.",
            "Porque solo puede retroceder y nunca avanza hacia adelante.",
            "Porque descarta la meta en cuanto la encuentra en la frontera."
        ],
        "correcta": 1,
        "explicacion": "La búsqueda voraz es miope: elige lo que parece más cercano ahora (menor h), pero puede meterte en un desvío larguísimo o en un callejón sin salida."
    },
    {
        "tema": "Ascenso de Colinas",
        "pregunta": "¿Cuál es el principal peligro del algoritmo de Ascenso de Colinas (Hill Climbing)?",
        "opciones": [
            "Quedar atrapado en un óptimo local (un pico que es más alto que sus vecinos, pero no el más alto del mapa).",
            "Gastar toda la memoria RAM almacenando los nodos anteriores.",
            "Calcular integrales dobles en cada paso del proceso.",
            "Confundir la lista abierta con la lista cerrada en cada iteración."
        ],
        "correcta": 0,
        "explicacion": "Como solo avanza si el vecino inmediato mejora la puntuación, si llega a una colina secundaria donde todos los pasos bajan, se detiene creyendo que triunfó."
    },
    {
        "tema": "Búsqueda en Haz (Beam Search)",
        "pregunta": "¿En qué consiste la técnica de Búsqueda en Haz y cuál es su parámetro 'k'?",
        "opciones": [
            "Conserva solo los 'k' mejores nodos en cada nivel, sacrificando optimalidad a cambio de ahorrar memoria.",
            "Multiplica la heurística por 'k' veces para acelerar el procesamiento gráfico.",
            "Divide el grafo en 'k' dimensiones espaciales paralelas e independientes.",
            "Repite la búsqueda 'k' veces desde el nodo inicial de forma aleatoria."
        ],
        "correcta": 0,
        "explicacion": "Beam Search poda radicalmente la frontera: solo retiene los k estados más prometedores por nivel, evitando que la memoria colapse en grafos gigantes."
    }
]

# ─── Constantes de puntaje (evitan el error del "/1000") ─────────
PUNTOS_BASE = 100
BONO_RACHA  = 20
MAX_PUNTOS  = len(PREGUNTAS) * PUNTOS_BASE + BONO_RACHA * (len(PREGUNTAS) - 1)
# = 1000 + 180 = 1180

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
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v


def reset_juego():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v


# ─── Mapa SVG de progreso ────────────────────────────────────────
def render_mapa_progreso(actual, total):
    ancho_total = 600
    lineas = (
        f'<line x1="30" y1="35" x2="{ancho_total - 30}" y2="35" '
        f'stroke="#475569" stroke-width="4" stroke-dasharray="6"/>'
    )
    circulos = []
    for i in range(total):
        cx = 35 + i * (ancho_total - 70) / (total - 1)
        cy = 35
        if i < actual:
            color, fill, texto = "#22c55e", "#22c55e", "✓"
        elif i == actual:
            color, fill, texto = "#38bdf8", "#0284c7", str(i + 1)
        else:
            color, fill, texto = "#64748b", "#1e293b", str(i + 1)
        circulos.append(
            f'<circle cx="{cx}" cy="{cy}" r="14" stroke="{color}" '
            f'stroke-width="3" fill="{fill}" />'
            f'<text x="{cx}" y="{cy + 4}" font-size="11" font-weight="bold" '
            f'fill="white" text-anchor="middle">{texto}</text>'
        )
    return f'''
    <div style="display:flex; justify-content:center; margin-bottom:15px; overflow-x:auto;">
        <svg width="{ancho_total}" height="70" viewBox="0 0 {ancho_total} 70">
            {lineas}{"".join(circulos)}
        </svg>
    </div>
    '''


# ─── ¿Partida terminada? ─────────────────────────────────────────
if st.session_state.terminado:
    st.markdown("<h2 style='text-align:center;'>🏁 Misión Heurística Finalizada</h2>",
                unsafe_allow_html=True)

    if st.session_state.vidas > 0:
        st.balloons()
        pct = st.session_state.puntos / MAX_PUNTOS
        if pct >= 0.9:
            rango = "🥇 Maestro de la Búsqueda Óptima (A*)"
        elif pct >= 0.6:
            rango = "🥈 Explorador Heurístico Calificado"
        else:
            rango = "🥉 Aprendiz de Búsqueda Informada"
        st.success(f"🏆 ¡Has completado el recorrido con éxito!\n\n**Rango obtenido:** {rango}")
    else:
        st.error("💀 ¡Has caído en un Óptimo Local sin salida! Te has quedado sin vidas.")

    st.markdown(f"""
    <div class="hud-box" style="text-align:center;">
        <h3>Estadísticas Finales</h3>
        <p style="font-size:20px;">⭐ <b>Puntuación total:</b> {st.session_state.puntos} / {MAX_PUNTOS} pts</p>
        <p style="font-size:18px;">🔥 <b>Mayor racha:</b> {st.session_state.max_racha} respuestas seguidas</p>
        <p style="font-size:18px;">❤️ <b>Vidas conservadas:</b> {max(0, st.session_state.vidas)} / 3</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Volver a Jugar", use_container_width=True):
        reset_juego()
        st.rerun()

# ─── Pantalla activa ─────────────────────────────────────────────
else:
    # HUD superior
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"**Vidas:** {'❤️ ' * st.session_state.vidas}{'🖤 ' * (3 - st.session_state.vidas)}")
    col2.markdown(f"**Puntos:** ⭐ `{st.session_state.puntos} pts`")
    col3.markdown(f"**Racha:** 🔥 `{st.session_state.racha}`")

    st.markdown(render_mapa_progreso(st.session_state.indice, len(PREGUNTAS)),
                unsafe_allow_html=True)

    q = PREGUNTAS[st.session_state.indice]

    st.markdown(f"""
    <div class="question-card">
        <span class="badge-topic">{q['tema']} • Nodo {st.session_state.indice + 1} de {len(PREGUNTAS)}</span>
        <h4 style="margin-top:5px; color:#f8fafc;">{q['pregunta']}</h4>
    </div>
    """, unsafe_allow_html=True)

    # ── FASE 1: responder ────────────────────────────────────────
    if not st.session_state.respondido:
        opcion_elegida = st.radio(
            "Selecciona la decisión óptima:",
            q["opciones"],
            key=f"pregunta_{st.session_state.indice}",
            label_visibility="collapsed"
        )
        if st.button("🚀 Confirmar Movimiento", use_container_width=True):
            idx_sel = next(i for i, o in enumerate(q["opciones"]) if o == opcion_elegida)
            es_correcta = (idx_sel == q["correcta"])

            if es_correcta:
                st.session_state.racha += 1
                bono = BONO_RACHA if st.session_state.racha > 1 else 0
                ganados = PUNTOS_BASE + bono
                st.session_state.puntos += ganados
                st.session_state.max_racha = max(st.session_state.max_racha,
                                                 st.session_state.racha)
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
            st.success(f"🎉 **¡Movimiento Óptimo!** (+{fb['ganados']} pts)\n\n{fb['explicacion']}")
        else:
            st.error(f"❌ **Ruta Subóptima o Bloqueada.** Pierdes 1 vida.\n\n{fb['explicacion']}")

        # Determinar si terminamos
        sin_vidas = st.session_state.vidas <= 0
        ultimo_nodo = st.session_state.indice >= len(PREGUNTAS) - 1
        texto_btn = "🏁 Ver Resultados" if (sin_vidas or ultimo_nodo) else "➡️ Siguiente Nodo"

        if st.button(texto_btn, use_container_width=True):
            if sin_vidas or ultimo_nodo:
                st.session_state.terminado = True
            else:
                st.session_state.indice += 1
            st.session_state.respondido = False
            st.session_state.feedback = None
            st.rerun()
import streamlit as st
import time

# Configuración visual de la aplicación
st.set_page_config(
    page_title="Expedición Heurística: En Busca del Óptimo",
    page_icon="🧭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS personalizados para una interfaz moderna y tipo videojuego
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
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

# Banco de 10 preguntas completas basadas en el temario
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
        "opciones": [
            "f(B) = 15 km",
            "f(B) = 65 km",
            "f(B) = 1000 km",
            "f(B) = 50 km"
        ],
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

# Inicialización de estado del juego
if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.puntos = 0
    st.session_state.vidas = 3
    st.session_state.racha = 0
    st.session_state.historial = []
    st.session_state.terminado = False

def render_mapa_progreso(actual, total):
    """Renderiza una representación gráfica del camino recorrido en SVG"""
    nodos_html = []
    ancho_total = 600
    espacio = ancho_total / (total + 1)
    
    lineas = f'<line x1="30" y1="35" x2="{ancho_total-30}" y2="35" stroke="#475569" stroke-width="4" stroke-dasharray="6"/>'
    
    circulos = []
    for i in range(total):
        cx = 35 + i * (ancho_total - 70) / (total - 1)
        cy = 35
        if i < actual:
            # Nodo superado (Verde)
            color = "#22c55e"
            fill = "#22c55e"
            texto = "✓"
        elif i == actual:
            # Nodo activo (Azul brillante)
            color = "#38bdf8"
            fill = "#0284c7"
            texto = str(i + 1)
        else:
            # Nodo futuro (Gris)
            color = "#64748b"
            fill = "#1e293b"
            texto = str(i + 1)
            
        circulos.append(f'''
            <circle cx="{cx}" cy="{cy}" r="14" stroke="{color}" stroke-width="3" fill="{fill}" />
            <text x="{cx}" y="{cy + 4}" font-size="11" font-weight="bold" fill="white" text-anchor="middle">{texto}</text>
        ''')
        
    svg = f'''
    <div style="display:flex; justify-content:center; margin-bottom: 15px; overflow-x: auto;">
        <svg width="{ancho_total}" height="70" viewBox="0 0 {ancho_total} 70">
            {lineas}
            {"".join(circulos)}
        </svg>
    </div>
    '''
    return svg

# PANTALLA DE JUEGO TERMINADO
if st.session_state.terminado or st.session_state.vidas <= 0 or st.session_state.indice >= len(PREGUNTAS):
    st.markdown("<h2 style='text-align:center;'>🏁 Misión Heurística Finalizada</h2>", unsafe_allow_html=True)
    
    if st.session_state.vidas > 0:
        st.balloons()
        rango = "Maestro de la Búsqueda Óptima (A*)" if st.session_state.puntos >= 900 else "Explorador Heurístico Calificado"
        st.success(f"🏆 ¡Felicitaciones! Has completado el recorrido con éxito.\\n\\n**Rango obtenido:** {rango}")
    else:
        st.error("💀 ¡Has caído en un Óptimo Local sin salida! Te has quedado sin vidas.")

    st.markdown(f"""
    <div class="hud-box" style="text-align:center;">
        <h3>Estadísticas Finales</h3>
        <p style="font-size: 20px;">⭐ <b>Puntuación total:</b> {st.session_state.puntos} / 1000 pts</p>
        <p style="font-size: 18px;">🔥 <b>Mayor racha:</b> {st.session_state.racha} respuestas seguidas</p>
        <p style="font-size: 18px;">❤️ <b>Vidas conservadas:</b> {max(0, st.session_state.vidas)} / 3</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Volver a Jugar", use_container_width=True):
        st.session_state.indice = 0
        st.session_state.puntos = 0
        st.session_state.vidas = 3
        st.session_state.racha = 0
        st.session_state.historial = []
        st.session_state.terminado = False
        st.rerun()

# PANTALLA PRINCIPAL DE PREGUNTA ACTIVA
else:
    # HUD Superior (Vidas, Puntos, Racha)
    col1, col2, col3 = st.columns(3)
    with col1:
        corazones = "❤️ " * st.session_state.vidas + "🖤 " * (3 - st.session_state.vidas)
        st.markdown(f"**Vidas:** {corazones}")
    with col2:
        st.markdown(f"**Puntos:** ⭐ `{st.session_state.puntos} pts`")
    with col3:
        st.markdown(f"**Racha:** 🔥 `{st.session_state.racha}`")

    # Mapa gráfico interactivo de nodos
    st.markdown(render_mapa_progreso(st.session_state.indice, len(PREGUNTAS)), unsafe_allow_html=True)

    # Tarjeta de la pregunta actual
    q = PREGUNTAS[st.session_state.indice]
    
    st.markdown(f"""
    <div class="question-card">
        <span class="badge-topic">{q['tema']} • Nodo {st.session_state.indice + 1} de {len(PREGUNTAS)}</span>
        <h4 style="margin-top: 5px; color: #f8fafc;">{q['pregunta']}</h4>
    </div>
    """, unsafe_allow_html=True)

    # Selección de opciones
    opcion_elegida = st.radio(
        "Selecciona la decisión óptima:",
        q["opciones"],
        key=f"pregunta_{st.session_state.indice}",
        label_visibility="collapsed"
    )

    col_btn, _ = st.columns([1, 1])
    with col_btn:
        confirmar = st.button("🚀 Confirmar Movimiento", use_container_width=True)

    if confirmar:
        idx_seleccionado = q["opciones"].index(opcion_elegida)
        
        if idx_seleccionado == q["correcta"]:
            st.session_state.racha += 1
            bono = 20 if st.session_state.racha > 1 else 0
            puntos_ganados = 100 + bono
            st.session_state.puntos += puntos_ganados
            st.success(f"🎉 **¡Movimiento Óptimo!** (+{puntos_ganados} pts)\\n\\n{q['explicacion']}")
        else:
            st.session_state.vidas -= 1
            st.session_state.racha = 0
            st.error(f"❌ **Ruta Subóptima o Bloqueada.** Pierdes 1 vida.\\n\\n{q['explicacion']}")
        
        time.sleep(1.8)
        st.session_state.indice += 1
        st.rerun()
import streamlit as st

# Configuración inicial de la página
st.set_page_config(page_title="Desafío Heurístico", page_icon="🧭", layout="centered")

st.title("🧭 Desafío: El Camino Heurístico")
st.write("Demuestra qué tan bien sabes orientarte en el espacio de estados.")

# Banco de preguntas del juego
preguntas = [
    {
        "pregunta": "1. Estás en un laberinto y tienes poco tiempo. ¿Qué hace la función heurística h(n)?",
        "opciones": [
            "Te da el costo exacto y perfecto de todo el camino",
            "Estima qué tan cerca estás de la meta sin garantizar exactitud",
            "Te regresa al inicio para no perderte",
            "Revisa todas las paredes del laberinto al mismo tiempo"
        ],
        "correcta": 1,
        "explicacion": "¡Correcto! h(n) es una estimación orientadora que no garantiza exactitud pero ahorra tiempo."
    },
    {
        "pregunta": "2. En la fórmula f(n) = g(n) + h(n), ¿qué representa g(n)?",
        "opciones": [
            "La distancia estimada que te falta por recorrer",
            "El número de pistas usadas",
            "El costo real que ya acumulaste caminando desde el inicio",
            "La cantidad de memoria RAM disponible"
        ],
        "correcta": 2,
        "explicacion": "¡Exacto! g(n) es el costo real acumulado del camino ya recorrido."
    },
    {
        "pregunta": "3. Si una heurística es 'admisible', significa que:",
        "opciones": [
            "Nunca sobreestima el costo real hacia la meta",
            "Siempre calcula el doble del costo para prevenir accidentes",
            "Solo funciona si no hay obstáculos",
            "Es aceptada por el compilador de Python sin errores"
        ],
        "correcta": 0,
        "explicacion": "¡Bien! Una heurística admisible siempre es optimista: nunca sobreestima el costo real."
    },
    {
        "pregunta": "4. Estás usando 'Ascenso de Colinas' y llegas a un punto donde todos los pasos bajan, pero no es la meta final. ¿Qué ocurrió?",
        "opciones": [
            "Llegaste al óptimo global",
            "El algoritmo se quedó sin memoria",
            "Caíste en un óptimo local",
            "El algoritmo entró en recursión infinita"
        ],
        "correcta": 2,
        "explicacion": "¡Cuidado con las colinas! Caíste en un óptimo local, el problema clásico de este método."
    },
    {
        "pregunta": "5. ¿Qué algoritmo combina lo mejor del costo real g(n) y el estimado h(n) para ser óptimo?",
        "opciones": [
            "Búsqueda Voraz (Greedy)",
            "Algoritmo A*",
            "Búsqueda en Profundidad (DFS)",
            "Búsqueda a Ciegas"
        ],
        "correcta": 1,
        "explicacion": "¡Perfecto! A* equilibra costo real y heurística, garantizando la ruta óptima."
    }
]

# Inicialización de variables de estado
if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.puntos = 0
    st.session_state.vidas = 3
    st.session_state.terminado = False

# Fin del juego
if st.session_state.terminado or st.session_state.vidas <= 0 or st.session_state.indice >= len(preguntas):
    if st.session_state.vidas > 0:
        st.success(f"🎉 ¡Felicidades! Completaste la búsqueda. Puntuación final: {st.session_state.puntos} / {len(preguntas) * 100}")
        st.balloons()
    else:
        st.error("💀 Te quedaste sin vidas en el espacio de estados. ¡Inténtalo de nuevo!")
    
    if st.button("Jugar otra vez"):
        st.session_state.indice = 0
        st.session_state.puntos = 0
        st.session_state.vidas = 3
        st.session_state.terminado = False
        st.rerun()

else:
    # Barra de estado
    col1, col2 = st.columns(2)
    with col1:
        st.metric("❤️ Vidas restantes", st.session_state.vidas)
    with col2:
        st.metric("⭐ Puntos", st.session_state.puntos)

    progreso = st.session_state.indice / len(preguntas)
    st.progress(progreso)

    q = preguntas[st.session_state.indice]
    st.subheader(q["pregunta"])

    eleccion = st.radio("Selecciona tu movimiento:", q["opciones"], key=f"q_{st.session_state.indice}")

    if st.button("Confirmar decisión"):
        idx_eleccion = q["opciones"].index(eleccion)
        if idx_eleccion == q["correcta"]:
            st.success(q["explicacion"])
            st.session_state.puntos += 100
        else:
            st.error("❌ Decisión errónea. Pierdes una vida.")
            st.session_state.vidas -= 1

        st.session_state.indice += 1
        st.rerun()
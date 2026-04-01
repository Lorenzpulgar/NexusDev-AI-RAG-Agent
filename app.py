import os
import streamlit as st
from typing import TypedDict
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langgraph.graph import StateGraph, START, END
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from dotenv import load_dotenv

# Cargar variables de entorno locales desde .env (útil para pruebas)
load_dotenv()

# Configuración de LLM (Las API Keys se toman de variables de entorno o st.secrets)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
# Base de conocimiento (RAG)
@st.cache_resource
def cargar_rag():
    loader = DirectoryLoader('./conocimiento', glob="**/*.md", show_progress=True)
    documentos = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = splitter.split_documents(documentos)
    
    vectorstore = FAISS.from_documents(chunks, GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001"))
    return vectorstore.as_retriever(search_kwargs={"k": 3})

retriever = cargar_rag()

search_engine = DuckDuckGoSearchRun()

@tool
def buscar_en_web(tema: str) -> str:
    """
    Busca información actualizada en la web usando un buscador.
    Útil para consultar noticias, tendencias o responder preguntas 
    que requieran conocimientos externos actuales de la web.
    """
    resultado = search_engine.invoke(tema)
    return f"Información encontrada en la web: {resultado}"

llm_con_herramientas = llm.bind_tools([buscar_en_web])

# Tipado de estado
class EstadoAgente(TypedDict):
    pregunta: str
    historial: str
    decision: str
    respuesta: str

# Nodos
def nodo_router(state: EstadoAgente):
    prompt = PromptTemplate.from_template(
        "Eres el sistema de enrutamiento de NexusDev AI RAG, diseñado para guiar a desarrolladores y arquitectos de software. Analiza la pregunta actual y el historial de la conversación para decidir a qué módulo enviarla.\n\n"
        "REGLAS ESTRICTAS DE RESPUESTA (Responde ÚNICAMENTE con una de estas 3 opciones, sin puntuación ni texto adicional):\n"
        "- TOOL_WEB: Si el usuario pregunta por documentación actualizada de librerías, buscar código o proyectos similares en GitHub/repositorios, problemas técnicos actuales, bugs, versiones nuevas de frameworks o ejemplos de código en internet.\n"
        "- RAG: Si el usuario pregunta sobre estándares internos de la empresa, buenas prácticas de vibecoding, guías de despliegue, cómo organizar la arquitectura de un agente, diseño UI (minimalista, pixel-art, etc) o migración de código legacy.\n"
        "- GENERAL: ÚNICA Y EXCLUSIVAMENTE para saludos (ej. 'hola', 'buen día'), o peticiones que no requieran búsqueda externa del buscador ni conocimiento interno.\n\n"
        "Historial:\n{historial}\n\n"
        "Pregunta: {pregunta}\n\n"
        "TU DECISIÓN (Una sola palabra):"
    )
    chain = prompt | llm
    resultado = chain.invoke({"pregunta": state["pregunta"], "historial": state["historial"]})
    
    texto_crudo = resultado.content.strip().upper()
    # Limpieza estricta de la salida del LLM para evitar errores de enrutamiento
    if "TOOL_WEB" in texto_crudo: decision = "TOOL_WEB"
    elif "RAG" in texto_crudo: decision = "RAG"
    else: decision = "GENERAL"
    
    return {"decision": decision}

def nodo_rag(state: EstadoAgente):
    busqueda_optimizada = f"{state['historial']} {state['pregunta']}"
    docs = retriever.invoke(busqueda_optimizada) 
    contexto = "\n".join([doc.page_content for doc in docs])
    
    prompt = PromptTemplate.from_template(
        "Eres un Lead AI Architect y experto en el desarrollo de IA. Tu audiencia son emprendedores, vibecoders y programadores avanzados que buscan crear proyectos retadores.\n"
        "Responde a la nueva pregunta basándote SOLO en el contexto proporcionado y usa el historial solo para mantener el hilo, sin mencionarlo explícitamente.\n\n"
        "INSTRUCCIONES CRÍTICAS:\n"
        "1. NO ALUCINES CÓDIGO. Si generas código (LangChain, LangGraph, Python, etc.), DEBE ser código real, exacto y en inglés. JAMÁS traduzcas nombres de clases, métodos o librerías al español (ej. nunca uses 'lg.Grafo()', usa 'StateGraph()').\n"
        "2. NO HABLES DEL HISTORIAL. No uses frases como 'Recuerdo que mencionaste' o 'Como hablamos antes'. Simplemente responde a la necesidad actual directa y naturalmente.\n"
        "3. Tono: Conciso, de arquitecto tech ('vibecoder' / '10x engineer'), profesional y altamente técnico.\n\n"
        "Historial de conversación:\n{historial}\n\n"
        "Contexto encontrado:\n{contexto}\n\n"
        "Pregunta actual: {pregunta}"
    )
    chain = prompt | llm
    resultado = chain.invoke({
        "contexto": contexto, 
        "pregunta": state["pregunta"],
        "historial": state["historial"]
    })
    return {"respuesta": resultado.content}

def nodo_general(state: EstadoAgente):
    """Responde preguntas generales usando el conocimiento interno del LLM y la memoria."""
    prompt = PromptTemplate.from_template(
        "Eres el Lead AI Architect de NexusDev. Tu objetivo es colaborar con emprendedores, vibecoders y programadores senior para elaborar proyectos ambiciosos, retadores y bien estructurados.\n\n"
        "INSTRUCCIONES CRÍTICAS:\n"
        "1. NO ALUCINES LIBRERÍAS. Todo el código que proporciones debe ser 100% real, funcional y estándar (Python, JS, etc.). JAMÁS traduzcas librerías, clases o métodos al español (ej. no inventes 'lg.Grafo()'; usa 'StateGraph()' o la sintaxis original correcta).\n"
        "2. NO REPITAS COSAS DE LA MEMORIA. No dialogues sobre lo que ya se dijo (ej. evita 'Recuerdo que querías hacer...'). Ve directo al grano y soluciona el problema de la pregunta actual.\n"
        "3. El código que compartas debe estar bien comentado y aplicar las mejores prácticas.\n"
        "4. Tu tono es el de un líder técnico experto: preciso, pragmático y cero condescendiente.\n\n"
        "Historial de conversación:\n{historial}\n\n"
        "Pregunta actual: {pregunta}"
    )
    chain = prompt | llm
    resultado = chain.invoke({
        "pregunta": state["pregunta"],
        "historial": state["historial"]
    })
    return {"respuesta": resultado.content}

def nodo_tool(state: EstadoAgente):
    tema_busqueda = state['pregunta']
    
    # Enfocar búsqueda en GitHub para proyectos/ejemplos
    if any(palabra in tema_busqueda.lower() for palabra in ["proyecto", "ejemplo", "github", "repositorio"]):
        tema_busqueda += " site:github.com"
        
    if len(tema_busqueda) > 300:
        tema_busqueda = tema_busqueda[-300:]
        
    respuesta = buscar_en_web.invoke({"tema": tema_busqueda})
    
    prompt_final = PromptTemplate.from_template(
        "Eres un Lead AI Architect experto apoyando a emprendedores y vibecoders.\n"
        "Basándote en los Resultados Web (para estar actualizado) y el Historial de la conversación, responde la pregunta de manera práctica y avanzada.\n\n"
        "INSTRUCCIONES CRÍTICAS:\n"
        "1. EL CÓDIGO DEBE SER IMPECABLE. Si provees ejemplos de código, usa sintaxis 100% real de las librerías originales (nunca españolices clases o funciones; usa 'StateGraph()', no métodos inventados).\n"
        "2. IGNORA MENCIONAR EL HISTORIAL. Entiende el contexto pero no lo narres de vuelta (evita 'Como discutimos previamente...').\n"
        "3. Sé altamente técnico, conciso y directo.\n\n"
        "Historial de conversación:\n{historial}\n\n"
        "Resultados Web:\n{info}\n\n"
        "Pregunta actual: {pregunta}"
    )
    cadena = prompt_final | llm
    respuesta_redactada = cadena.invoke({
        "info": respuesta,
        "pregunta": state["pregunta"],
        "historial": state["historial"]
    })
    
    return {"respuesta": respuesta_redactada.content}

# Enrutamiento condicional
def decidir_camino(state: EstadoAgente):
    if state["decision"] == "RAG":
        return "nodo_rag"
    elif state["decision"] == "TOOL_WEB":
        return "nodo_tool"
    return "nodo_general"

# Grafo
grafo = StateGraph(EstadoAgente)
grafo.add_node("router", nodo_router)
grafo.add_node("nodo_rag", nodo_rag)
grafo.add_node("nodo_general", nodo_general)
grafo.add_node("nodo_tool", nodo_tool)  # <-- Añadimos el nodo de herramientas faltante

# Definir el flujo
grafo.add_edge(START, "router")
grafo.add_conditional_edges("router", decidir_camino)
grafo.add_edge("nodo_rag", END)
grafo.add_edge("nodo_general", END)
grafo.add_edge("nodo_tool", END)

app_grafo = grafo.compile()

# Interfaz UI
st.set_page_config(page_title="NexusDev AI RAG", page_icon="🤖", layout="centered")

try: 
    with open("styles.css", "r", encoding="utf-8") as f:
        vaporwave_css = f"<style>{f.read()}</style>"
        st.markdown(vaporwave_css, unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ Falta el cartucho de video `styles.css`. Cargando gráficos por defecto...")

st.title("🌴 N E X U S D E V 📼")
st.markdown("### HUB DE PRACTICAS DE CALIDAD PARA DESARROLLOS CON IA")
st.markdown("**Tu compañero de desarrollo y arquitecto de software.** ✨📡")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for msg in st.session_state.mensajes:
    with st.chat_message(msg["rol"]):
        st.write(msg["contenido"])

if pregunta_usuario := st.chat_input("I N G R E S A   T U   C O N S U L T A   A Q U Í . . . "):
    st.session_state.mensajes.append({"rol": "user", "contenido": pregunta_usuario})
    with st.chat_message("user"):
        st.write(pregunta_usuario)

    historial_lista = []
    import re
    
    # Extraer ultimos 4 mensajes
    for msg in st.session_state.mensajes[-5:-1]: 
        texto_limpio = msg['contenido']
        if msg['rol'] == 'assistant':
            texto_limpio = re.sub(r"\*?\*?\[Ruta usada: .*?\]\*?\*?\n*", "", texto_limpio).strip()
        historial_lista.append(f"{msg['rol']}: {texto_limpio}")
    
    historial_str = "\n".join(historial_lista)

    entradas = {
        "pregunta": pregunta_usuario,
        "historial": historial_str  # <--- Inyectamos la memoria aquí
    }
    
    with st.spinner("El agente está pensando y enrutando..."):
        resultado = app_grafo.invoke(entradas)
        respuesta_final = resultado["respuesta"]
        ruta_tomada = resultado["decision"]

    respuesta_final = re.sub(r"\*?\*?\[Ruta usada: .*?\]\*?\*?\n*", "", respuesta_final).strip()

    texto_mostrar = f"**[Ruta usada: {ruta_tomada}]**\n\n{respuesta_final}"
    st.session_state.mensajes.append({"rol": "assistant", "contenido": texto_mostrar})
    with st.chat_message("assistant"):
        st.write(texto_mostrar)
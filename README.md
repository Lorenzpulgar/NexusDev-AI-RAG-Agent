# 🌴 NexusDev AI RAG 📼

**NexusDev AI RAG** es un agente conversacional basado en la arquitectura de grafos (**LangGraph**) y Retrieval-Augmented Generation (**RAG**). Está diseñado para asistir a _Vibecoders_, arquitectos de software y emprendedores tecnológicos mediante la unificación de conocimientos internos, búsquedas en internet y razonamiento lógico avanzado.

El proyecto está orquestado con **Llama-3.3-70B-Versatile** a través de la API de **Groq** para un rendimiento y latencia ultrarrápidos, y una interfaz visual construida en **Streamlit** https://nexusdev-ai-rag-agent.streamlit.app/.

## ✨ Características Principales

1. **Enrutamiento Inteligente (LangGraph):** El agente categoriza automáticamente la pregunta del usuario en tres rutas:
   * **RAG:** Responde usando la base de conocimiento local (`/conocimiento/*.md`) con información como estándares internos, arquitectura o buenas prácticas. Vectorizado con `FAISS` y `GoogleGenerativeAIEmbeddings`.
   * **TOOL_WEB:** Utiliza `DuckDuckGoSearchRun` para navegar por internet en tiempo real si el usuario pregunta por errores recientes, actualizaciones de dependencias o documentación externa.
   * **GENERAL:** Responde apoyándose puramente en su entrenamiento base de 70 Billones de parámetros para dudas teóricas o arquitectura en general.
2. **Memoria de Contexto:** Extrae inteligentemente un historial de los últimos mensajes para mantener la continuidad conversacional.
3. **UI Vaporwave:** Diseño minimalista y de contraste (inyectado mediante CSS externo `styles.css`).

## 💡 El Valor de NexusDev (Vs. ChatGPT / Claude / Gemini)

A diferencia de usar un modelo conversacional genérico comercial (como ChatGPT o Claude), **NexusDev AI RAG** resuelve problemas críticos para el entrenamiento corporativo y el *onboarding* de nuevos desarrolladores:

1. **Onboarding Acelerado y Preciso:** Los nuevos empleados a menudo pierden horas buscando cómo se configuran las dependencias internas o qué arquitectura prefiere la empresa. NexusDev ingiere los `.md` iterativos del equipo y responde con las reglas **exactas de la empresa**, reduciendo la fricción de entrada.
2. **Cero Alucinaciones de Código Interno:** Mientras que Gemini o ChatGPT intentarán inventar una solución basada en estándares genéricos de internet, NexusDev utiliza la ruta **RAG** para citar estrictamente el código base y la documentación privada local, asegurando estándares de calidad.
3. **Agente Enrutador Inteligente (LangGraph):** No es un simple chat. Es un ecosistema que decide autónomamente qué herramienta usar. Si el junior pregunta por un bug externo reciente, usará el **Buscador (DuckDuckGo)** cruzándolo con GitHub; si pregunta por reglas de negocio, leerá la **Data Vectorial (FAISS)**; si pide consejo de carrera, actuará como un **Mentor Senior**. Esta arquitectura modular demuestra dominio en el diseño de agentes avanzados.

## ⚙️ Tecnologías

* **Python 3.10+**
* **LangChain & LangGraph**
* **Groq API** (`llama-3.3-70b-versatile`)
* **Google Gemini API** (solo para Embeddings)
* **Streamlit**
* **FAISS** (Base de datos vectorial en memoria)

---

## 🚀 Despliegue Local (Para Desarrollo)

1. **Clona el repositorio** e ingresa a la carpeta:
    ```bash
    git clone https://github.com/tu-usuario/nexusdev-ai-rag.git
    cd nexusdev-ai-rag
    ```

2. **Crea y activa un entorno virtual:**
    ```bash
    python -m venv venv
    
    # En Windows:
    venv\Scripts\activate
    # En macOS/Linux:
    source venv/bin/activate
    ```

3. **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Variables de Entorno:**
    El proyecto no incluye claves de acceso en el código por seguridad. Configura tus tokens localmente, ya sea exportándolos o mediante un archivo `.env`:
    
    ```bash
    export GROQ_API_KEY="tu_clave_de_groq_aqui"
    export GOOGLE_API_KEY="tu_clave_de_google_aqui"
    ```

5. **Añade conocimiento:**
    Inserta tus archivos Markdown (`.md`) en la carpeta `/conocimiento/`.
    
6. **Ejecuta la interfaz:**
    ```bash
    streamlit run app.py
    ```

---



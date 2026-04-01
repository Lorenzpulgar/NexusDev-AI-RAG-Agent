# NexusDev AI RAG - Estándares de Arquitectura y Agentes IA

## Cómo Crear y Configurar Agentes Eficientes
Al desarrollar sistemas multi-agente o usar herramientas como ClaudeCode, todo desarrollador o "vibecoder" debe seguir estos estándares:

### 1. Modularidad (El Patrón LangGraph)
Nunca crees un "Agente Dios" que intente hacer todo. Divide las responsabilidades en nodos especializados:
* **Nodo Router:** Clasifica la intención del usuario y decide a qué nodo especializado enviar la consulta. Debe ser determinista y rápido.
* **Nodo RAG:** Consulta bases de conocimiento vectoriales (FAISS, Pinecone, ChromaDB) para responder con información interna verificada.
* **Nodo de Herramientas (Tools):** Ejecuta acciones externas como búsquedas web (DuckDuckGo), llamadas a APIs, ejecución de código o consultas a bases de datos.
* **Nodo General:** Maneja conversación casual y saludos sin consumir recursos de búsqueda.

### 2. Prompts como Código (Prompt Engineering Profesional)
Los prompts no son texto libre, son lógica de negocio. Deben cumplir:
* **Versionamiento:** Almacena los prompts en archivos separados o constantes con control de versiones en Git. Nunca los dejes hardcodeados sin documentar.
* **Determinismo:** Incluye instrucciones estrictas de formato de salida (ej. "Responde ÚNICAMENTE con una de estas 3 opciones").
* **Contexto Limitado:** Pasa solo el contexto necesario al LLM. Un prompt sobrecargado produce alucinaciones y respuestas impredecibles.
* **Separación de Responsabilidades:** Un prompt debe hacer UNA sola cosa. Si necesitas clasificar Y responder, usa dos prompts en nodos separados.
* **Few-Shot Examples:** Incluye 2-3 ejemplos de input/output esperado dentro del prompt para guiar al modelo.

### 3. Manejo de Memoria y Contexto
Los agentes deben tener ventanas de contexto limitadas para evitar alucinaciones y altos costos de API:
* **Ventana Deslizante:** Mantén los últimos 4-6 mensajes como contexto inmediato. El historial viejo se descarta o se resume.
* **Memoria Semántica:** Para conversaciones largas, usa un LLM para resumir el historial anterior en 2-3 oraciones antes de pasarlo como contexto.
* **Memoria Persistente:** Si necesitas recordar datos entre sesiones, almacénalos en una base de datos (SQLite, Redis) y recupéralos selectivamente.

### 4. Patrones de Arquitectura Multi-Agente
* **Orquestador Central:** Un agente "director" que delega tareas a agentes especializados. Ideal para flujos complejos con múltiples pasos.
* **Pipeline Secuencial:** Los agentes se encadenan uno tras otro (A → B → C). Cada uno transforma o enriquece el estado. Útil para procesamiento de datos.
* **Patrón Supervisor:** Un agente revisa y valida la salida de otros agentes antes de enviarla al usuario. Mejora la calidad de las respuestas.
* **Agentes Reactivos vs Proactivos:** Los reactivos esperan input del usuario; los proactivos monitorean eventos y actúan automáticamente (ej. alertas de CI/CD).

## Antipatrones Comunes al Construir Agentes
Errores frecuentes que todo vibecoder y junior debe evitar:
* **El Agente Dios:** Un solo agente que intenta manejar RAG, búsqueda web, ejecución de código y conversación general. Resultado: respuestas inconsistentes y difíciles de debuggear.
* **Prompt Spaghetti:** Prompts de 500+ palabras con instrucciones contradictorias. El LLM se confunde y prioriza las últimas instrucciones sobre las primeras.
* **Sin Manejo de Errores:** No capturar excepciones de APIs externas (timeouts de búsqueda web, límites de rate del LLM). El agente debe degradarse gracefully.
* **Confianza Ciega en el LLM:** Nunca uses la salida de un LLM directamente para ejecutar código, queries SQL o acciones destructivas sin validación humana o programática.
* **Ignorar los Costos:** Cada llamada al LLM cuesta dinero. Usa modelos pequeños y rápidos (llama-3.1-8b) para tareas simples como routing, y modelos grandes (llama-3.1-70b, GPT-4) solo para tareas complejas de razonamiento.

## Herramientas Recomendadas para Desarrollo de Agentes
* **LangGraph:** Framework de grafos para crear flujos de agentes con estado. Estándar en Nexus DevHub.
* **LangChain:** Librería para encadenar LLMs con herramientas, retrievers y memorias.
* **ClaudeCode / Cursor / Windsurf:** IDEs con IA integrada para escribir, refactorizar y depurar código de agentes.
* **FAISS:** Motor de búsqueda vectorial para RAG local, rápido y sin costo de infraestructura.
* **ChromaDB:** Base vectorial open source que permite persistencia y filtrado por metadatos.
* **Streamlit:** Framework para crear interfaces de chat y dashboards para agentes conversacionales.
# Patrones de Diseño de Software en la Era de la IA

Los patrones de diseño no son teoría académica inútil. Son soluciones probadas a problemas recurrentes que aparecen en todo proyecto de software. Un vibecoder que conoce estos patrones puede dar instrucciones mucho más precisas a la IA y evaluar mejor el código generado.

## Patrones Esenciales que Todo Developer Debe Conocer

### 1. Singleton (Instancia Única)
* **Problema:** Necesitas que una clase tenga exactamente una instancia global (ej. conexión a base de datos, cliente de LLM).
* **Ejemplo real:** Tu `ChatGroq(model="llama-3.1-8b-instant")` debería ser un singleton. No crees una nueva conexión al LLM en cada request, eso desperdicia recursos y puede causar rate limiting.
* **Implementación en Python:** Usa el decorador `@st.cache_resource` en Streamlit (como ya haces con `cargar_rag()`) o implementa el patrón con `__new__()`.
* **Cuándo NO usarlo:** Cuando necesitas múltiples instancias con configuraciones diferentes (ej. un LLM para routing con temperature=0 y otro para creatividad con temperature=0.7).

### 2. Factory (Fábrica)
* **Problema:** Necesitas crear objetos de diferentes tipos sin exponer la lógica de creación al código cliente.
* **Ejemplo real:** Una función `crear_llm(proveedor="groq", modelo="llama-3.1-8b")` que internamente decide si instanciar `ChatGroq`, `ChatOpenAI` o `ChatAnthropic` según el proveedor.
* **Beneficio para vibecoders:** Te permite cambiar de proveedor de LLM sin tocar el código que lo usa. Solo cambias la configuración.

### 3. Strategy (Estrategia)
* **Problema:** Tienes múltiples algoritmos que hacen lo mismo de formas diferentes y necesitas elegir cuál usar en tiempo de ejecución.
* **Ejemplo real:** Tu nodo router en LangGraph ES un patrón Strategy. Según la clasificación (RAG, TOOL_WEB, GENERAL), ejecuta una estrategia diferente para responder.
* **Otro ejemplo:** Diferentes estrategias de embedding: OpenAI Embeddings para calidad, Google Embeddings para costo, o embeddings locales para privacidad. El código que consulta el retriever no sabe ni le importa cuál se usó.

### 4. Observer (Observador)
* **Problema:** Cuando un objeto cambia de estado, otros objetos necesitan ser notificados automáticamente.
* **Ejemplo real:** Un sistema de monitoreo donde cuando un agente produce un error, automáticamente se envía una notificación al canal de Discord del equipo, se registra en el log y se incrementa el contador de errores.
* **En agentes IA:** Los callbacks de LangChain (`on_llm_start`, `on_llm_end`, `on_tool_start`) son una implementación del patrón Observer.

### 5. Chain of Responsibility (Cadena de Responsabilidad)
* **Problema:** Una petición necesita pasar por una serie de validaciones o procesadores antes de ser manejada.
* **Ejemplo real:** Una petición de usuario pasa por: validador de input → detector de prompt injection → router → nodo especializado → filtro de contenido → respuesta. Cada eslabón puede rechazar la petición o pasarla al siguiente.
* **En LangChain:** El operador pipe `|` (`prompt | llm | output_parser`) implementa exactamente este patrón.

### 6. Decorator (Decorador)
* **Problema:** Necesitas añadir funcionalidad a un objeto sin modificar su código original.
* **Ejemplo real en Python:** Los decoradores `@tool`, `@st.cache_resource`, `@retry`. Añaden comportamiento (convertir una función en herramienta LangChain, cachear resultados, reintentar en caso de error) sin modificar la función original.
* **Uso práctico:** Crea decoradores custom para logging automático, medición de tiempo de ejecución o validación de inputs.

## Principios SOLID Simplificados para Vibecoders

### S - Single Responsibility (Responsabilidad Única)
Cada módulo, clase o función debe tener UNA sola razón para cambiar. Si tu función `procesar_consulta()` routea, busca en el RAG, llama al LLM Y formatea la respuesta, viola este principio. Divídela en 4 funciones.

### O - Open/Closed (Abierto/Cerrado)
Tu código debe estar abierto para extensión pero cerrado para modificación. Si necesitas agregar un nuevo tipo de nodo a tu grafo LangGraph, deberías poder hacerlo sin modificar los nodos existentes.

### L - Liskov Substitution (Sustitución de Liskov)
Si tienes una clase base `BaseLLM`, cualquier subclase (`ChatGroq`, `ChatOpenAI`) debe ser intercambiable sin romper el código que la usa.

### I - Interface Segregation (Segregación de Interfaces)
No obligues a una clase a implementar métodos que no necesita. Si tu nodo solo lee documentos, no debería implementar métodos de escritura.

### D - Dependency Inversion (Inversión de Dependencias)
Los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones. Tu nodo RAG no debería depender directamente de FAISS; debería depender de una interfaz "Retriever" que FAISS implementa. Así puedes cambiar a ChromaDB sin tocar el nodo.

## Arquitecturas de Software Comunes

### Monolito
* Todo el código vive en un solo proyecto/repositorio/despliegue.
* **Ventajas:** Simple de desarrollar, desplegar y debuggear al inicio.
* **Desventajas:** A medida que crece, se vuelve difícil de mantener, escalar y desplegar parcialmente.
* **Recomendado para:** Prototipos, MVPs, proyectos personales, vibecoders aprendiendo.

### Microservicios
* La aplicación se divide en servicios independientes que se comunican por APIs (REST, gRPC, mensajería).
* **Ventajas:** Cada servicio se escala, despliega y desarrolla independientemente. Diferentes equipos pueden usar diferentes tecnologías.
* **Desventajas:** Complejidad operacional alta. Necesitas orquestación (Kubernetes), service discovery, manejo de fallos distribuidos.
* **Recomendado para:** Proyectos en producción con equipos grandes y necesidades de escalabilidad.

### Serverless
* No gestionas servidores. Tu código se ejecuta en funciones que se activan bajo demanda (AWS Lambda, Google Cloud Functions).
* **Ventajas:** Pagas solo por lo que usas. Escalado automático. Cero mantenimiento de infraestructura.
* **Desventajas:** Cold starts (latencia en la primera ejecución), límites de tiempo de ejecución (15 min en Lambda), difícil de debuggear localmente.
* **Recomendado para:** APIs ligeras, webhooks, procesamiento de eventos, funciones que no necesitan estado.

### Event-Driven (Orientada a Eventos)
* Los componentes se comunican mediante eventos asincrónicos (ej. un usuario se registra → evento "user_created" → servicio de email envía bienvenida + servicio de analytics registra el evento).
* **Ventajas:** Desacoplamiento máximo. Los servicios no necesitan conocerse entre sí.
* **Recomendado para:** Sistemas con flujos complejos asincrónicos, integraciones con múltiples servicios.

# Bases de Datos y Gestión de Datos para Agentes IA

Toda aplicación seria necesita persistir datos. Los agentes IA tienen necesidades específicas de almacenamiento: historiales de chat, embeddings vectoriales, documentos de conocimiento, configuraciones de usuario y logs de trazabilidad.

## Tipos de Bases de Datos y Cuándo Usar Cada Una

### Bases de Datos Relacionales (SQL)
Almacenan datos en tablas con filas y columnas, con relaciones definidas entre ellas.
* **PostgreSQL:** La base de datos relacional más completa y robusta. Soporta JSON nativo, búsqueda de texto completo, extensiones para vectores (pgvector). Recomendada en Nexus DevHub para datos estructurados en producción.
* **SQLite:** Base de datos en un solo archivo. Ideal para prototipos, aplicaciones de escritorio y tests. No necesita servidor.
* **Cuándo usarlas:** Datos con estructura definida (usuarios, pedidos, productos), relaciones entre entidades, transacciones ACID, reportes y analytics.
* **ORM recomendado:** SQLAlchemy para Python. Permite escribir queries en Python en lugar de SQL crudo, y funciona con PostgreSQL, SQLite y MySQL indistintamente.

### Bases de Datos NoSQL
* **MongoDB:** Base de datos de documentos JSON. Flexible, sin esquema fijo. Buena para datos semi-estructurados que cambian frecuentemente.
* **Redis:** Base de datos en memoria, ultrarrápida. Ideal para caché, sesiones de usuario, rate limiting, colas de mensajes.
* **Cuándo usarlas:** Datos sin estructura fija, caché de alto rendimiento, prototipado rápido donde el esquema aún no está definido.

### Bases de Datos Vectoriales (Esenciales para RAG)
Almacenan vectores de embeddings y permiten búsqueda por similitud semántica.
* **FAISS (Facebook AI Similarity Search):** Motor de búsqueda vectorial local, rápido y sin costo de infraestructura. Ideal para RAGs locales y prototipos. No persiste por defecto (se recarga desde documentos cada vez que la app inicia, a menos que guardes el índice con `save_local()`).
* **ChromaDB:** Base vectorial open source con API simple en Python. Soporta persistencia en disco, filtrado por metadatos y operaciones CRUD sobre documentos. Ideal para proyectos que necesitan más control que FAISS.
* **Pinecone:** Base vectorial en la nube como servicio (SaaS). Escalable, con alta disponibilidad y baja latencia. Tiene capa gratuita limitada. Ideal para producción cuando el volumen de datos es alto.
* **pgvector:** Extensión de PostgreSQL que agrega soporte para vectores. Permite combinar búsqueda vectorial con queries SQL tradicionales en una sola base de datos.

## RAG (Retrieval-Augmented Generation): Guía Completa

### ¿Qué es RAG y por qué es superior a Fine-Tuning?
RAG es una técnica que enriquece las respuestas del LLM con información recuperada de una base de conocimiento propia. En lugar de entrenar el modelo (fine-tuning), le das documentos relevantes como contexto en cada consulta.

### Ventajas del RAG sobre Fine-Tuning
* **Actualización inmediata:** Agregas un nuevo documento y el RAG lo usa al instante. Fine-tuning requiere reentrenar el modelo.
* **Control de la información:** Sabes exactamente de dónde viene cada dato. En fine-tuning, el conocimiento queda "mezclado" con los datos de entrenamiento original.
* **Costo:** RAG es gratis (son documentos + embeddings). Fine-tuning cuesta dinero y tiempo de GPU.
* **Privacidad:** Tus documentos nunca salen de tu infraestructura. Fine-tuning con APIs externas implica enviar tus datos al proveedor.

### Pipeline de RAG Paso a Paso
1. **Carga de Documentos:** Usa `DirectoryLoader` de LangChain para cargar archivos .md, .pdf, .txt, .docx desde una carpeta.
2. **Chunking (Fragmentación):** Divide los documentos en chunks de 1000-2000 caracteres con 200 de overlap. El overlap evita que se pierda contexto en los bordes.
3. **Embedding:** Convierte cada chunk en un vector numérico usando un modelo de embeddings (Google Gemini Embeddings, OpenAI Embeddings, o modelos locales como all-MiniLM-L6-v2).
4. **Indexación:** Almacena los vectores en una base vectorial (FAISS, ChromaDB, Pinecone).
5. **Retrieval (Recuperación):** Cuando el usuario hace una pregunta, la conviertes a vector y buscas los K chunks más similares (cosine similarity).
6. **Generation (Generación):** Pasas la pregunta del usuario + los chunks recuperados como contexto al LLM, que genera una respuesta basada en esa información.

### Optimización del RAG
* **Chunk size:** 1000-2000 caracteres funciona bien como default. Chunks muy pequeños pierden contexto; muy grandes desperdician tokens.
* **Top-K:** Recuperar 4-8 chunks es el sweet spot. Más de 10 genera ruido y puede confundir al LLM.
* **Hybrid Search:** Combina búsqueda vectorial (semántica) con búsqueda por keywords (BM25) para mejores resultados. LangChain soporta `EnsembleRetriever`.
* **Reranking:** Después de recuperar los top-K chunks, usa un modelo de reranking (ej. Cohere Rerank) para reordenarlos por relevancia real.
* **Metadata Filtering:** Agrega metadatos a tus documentos (fecha, categoría, autor) y filtra antes de buscar. Ejemplo: si el usuario pregunta sobre "despliegue", filtra solo documentos con categoría "deploy".

## Modelado de Datos para Aplicaciones con Agentes

### Esquema para Historiales de Chat
Todo agente conversacional necesita persistir historiales de chat. Esquema recomendado:
* **Tabla conversations:** id, user_id, titulo, created_at, updated_at.
* **Tabla messages:** id, conversation_id, role (user/assistant/system), content, metadata (JSON), created_at.
* **Tabla feedback:** id, message_id, rating (1-5), comment, created_at. Para que los usuarios califiquen las respuestas y mejores continuamente.

### Esquema para Trazabilidad de Agentes
Para auditar y debuggear las decisiones de tu agente:
* **Tabla agent_traces:** id, conversation_id, message_id, node_name (router/rag/tool/general), input_state (JSON), output_state (JSON), tokens_used, latency_ms, created_at.
* Esto permite responder preguntas como: "¿Por qué el agente le dio esta respuesta al usuario?" y "¿Cuánto estamos gastando en tokens por día?".

## Migraciones de Base de Datos
* Nunca modifiques tablas de producción directamente con SQL crudo.
* Usa herramientas de migración: Alembic (para SQLAlchemy/Python), Prisma Migrate (para TypeScript).
* Cada cambio de esquema (nueva columna, nueva tabla, cambio de tipo) se registra como un archivo de migración versionado.
* Las migraciones se aplican secuencialmente y son reversibles. Si algo sale mal, puedes hacer rollback al estado anterior.

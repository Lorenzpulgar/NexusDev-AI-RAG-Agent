# Guía de Despliegue (Deploy) para Proyectos y Agentes IA

## Filosofía de Despliegue en Nexus DevHub
Desplegar no es "subir archivos a un servidor". Es el proceso de llevar código verificado desde tu máquina local hasta un entorno donde los usuarios finales pueden interactuar con él de forma confiable, segura y escalable.

## Entornos de Despliegue (Dev → Staging → Producción)
Todo proyecto profesional debe tener al menos 2 entornos separados:
* **Desarrollo (Dev):** Tu máquina local o un servidor de pruebas. Aquí rompes cosas libremente.
* **Staging:** Una réplica exacta de producción donde pruebas antes de lanzar. Los QA y testers trabajan aquí.
* **Producción (Prod):** El entorno real donde los usuarios interactúan con tu aplicación. Aquí NADA se sube sin pasar por staging.
* **Regla de Oro:** Nunca hagas cambios directamente en producción. Siempre pasa por Dev → Staging → Prod.

## Opciones de Despliegue Gratuitas (Prototipos y Portafolios)
Ideal para juniors y vibecoders que están probando sus agentes en entornos de desarrollo:

### Para Backends y APIs en Python
* **Render:** Excelente para APIs en FastAPI/Flask y bots de Discord. Ofrece capa gratuita que suspende la app tras 15 minutos de inactividad. Soporta despliegue desde GitHub automáticamente.
* **Railway:** Similar a Render pero con interfaz más moderna y mejor soporte para bases de datos PostgreSQL gratuitas. Ideal para proyectos con LangGraph que necesitan persistencia.
* **Streamlit Community Cloud:** La forma más rápida de publicar interfaces gráficas para agentes conversacionales. Conecta tu repo de GitHub y despliega en 2 minutos. Limitación: solo aplicaciones Streamlit.

### Para Frontends y Sitios Web
* **Vercel:** El estándar de la industria para Next.js, React y sitios estáticos. Despliegue automático desde GitHub con previews por cada PR. CDN global incluido.
* **Netlify:** Alternativa a Vercel con funciones serverless integradas. Ideal para sitios estáticos generados por IA con formularios de contacto.
* **GitHub Pages:** Para portafolios y documentación estática. Gratis y sin límites de ancho de banda para repositorios públicos.

## Opciones de Despliegue para Producción (Escalables)
Cuando un proyecto pasa a fase de producción o requiere manejar bases de datos vectoriales pesadas de manera constante:

### Contenedores con Docker
* **Docker** es obligatorio para proyectos de producción en Nexus DevHub. Garantiza que tu aplicación funcione igual en tu laptop, en staging y en producción.
* Todo proyecto debe tener un `Dockerfile` y un `docker-compose.yml` documentados en el repositorio.
* Estructura recomendada del Dockerfile para agentes Python:
  - Usa imagen base `python:3.11-slim` (no `python:3.11` completa, pesa 3x más).
  - Copia primero `requirements.txt` e instala dependencias antes de copiar el código fuente (aprovecha la caché de capas de Docker).
  - Nunca incluyas API keys en el Dockerfile. Usa variables de entorno o secrets managers.

### Proveedores Cloud
* **AWS (Amazon Web Services):** ECS para contenedores, Lambda para funciones serverless, S3 para almacenamiento de archivos. Curva de aprendizaje alta pero máxima flexibilidad.
* **Google Cloud Platform (GCP):** Cloud Run para contenedores con autoescalado automático. Ideal si usas integraciones con Gemini, Google Embeddings o Vertex AI.
* **DigitalOcean App Platform:** Alternativa más simple y económica que AWS/GCP. Buena para startups y proyectos medianos.

## Gestión de Variables de Entorno y Secretos
* **NUNCA** hardcodees API keys, contraseñas o tokens en el código fuente. Es la vulnerabilidad de seguridad más común en proyectos de vibecoders.
* En desarrollo local, usa archivos `.env` con la librería `python-dotenv`. Asegúrate de que `.env` esté en tu `.gitignore`.
* En producción, usa el sistema de secretos del proveedor cloud (AWS Secrets Manager, GCP Secret Manager, Railway/Render Variables).
* Rota las API keys periódicamente, especialmente las de LLMs que pueden generar costos altos si se filtran.

## CI/CD (Integración y Despliegue Continuo)
* Configura GitHub Actions para ejecutar tests automáticamente en cada push y pull request.
* Un pipeline básico de CI/CD debe incluir: instalar dependencias → ejecutar linters → ejecutar tests → construir Docker image → desplegar a staging.
* Usa branch protection en `main`: nadie hace push directo, todo pasa por Pull Request con al menos 1 revisión aprobada.

## Consideración de Costos para Agentes IA
* Los agentes IA consumen memoria al mantener historiales de chat. Configura alertas de facturación desde el día 1.
* Limita las variables de estado en los servidores: un agente con historial infinito consumirá RAM infinita.
* Usa modelos pequeños (llama-3.1-8b, gemma2-9b) para tareas de clasificación y routing donde la latencia y el costo importan más que la capacidad de razonamiento.
* Implementa rate limiting en tus APIs para evitar abusos que disparen costos de LLM.

## Monitoreo y Observabilidad
* Implementa logging estructurado (JSON) desde el día 1. Herramientas gratuitas: Logtail, Better Stack.
* Monitorea métricas clave: latencia de respuesta del agente, tasa de errores, tokens consumidos por LLM, uso de RAM/CPU.
* Configura alertas automáticas por email o Discord cuando la tasa de errores supere el 5% o la latencia supere los 10 segundos.
* Usa LangSmith para trazabilidad de las cadenas de LangChain/LangGraph en producción: permite ver exactamente qué prompt se envió, qué respondió el LLM y cuántos tokens consumió.

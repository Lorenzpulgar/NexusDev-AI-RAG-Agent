# APIs y Comunicación entre Servicios

Las APIs (Application Programming Interfaces) son el sistema nervioso de la ingeniería de software moderna. Todo agente IA, todo frontend, todo microservicio se comunica mediante APIs. Un vibecoder que domina APIs puede construir cualquier cosa.

## Fundamentos de APIs REST

### ¿Qué es una API REST?
Es un estilo arquitectónico para diseñar servicios web que usan HTTP como protocolo de comunicación. Los clientes (frontend, otros servicios, agentes IA) envían peticiones HTTP y reciben respuestas estructuradas (generalmente en JSON).

### Los Verbos HTTP y Cuándo Usarlos
* **GET:** Obtener datos. No modifica nada. Ejemplo: `GET /api/users/123` → obtiene el usuario con ID 123.
* **POST:** Crear datos nuevos. Ejemplo: `POST /api/users` con body `{"nombre": "Ana"}` → crea un nuevo usuario.
* **PUT:** Reemplazar un recurso completo. Ejemplo: `PUT /api/users/123` con body `{"nombre": "Ana María"}` → reemplaza toda la entidad.
* **PATCH:** Actualizar parcialmente. Ejemplo: `PATCH /api/users/123` con body `{"email": "ana@nexus.dev"}` → solo actualiza el email.
* **DELETE:** Eliminar un recurso. Ejemplo: `DELETE /api/users/123` → elimina el usuario.

### Códigos de Estado HTTP que Debes Conocer
* **200 OK:** La petición fue exitosa.
* **201 Created:** Se creó un recurso exitosamente (respuesta a POST).
* **400 Bad Request:** Error del cliente (datos malformados, campos faltantes).
* **401 Unauthorized:** No autenticado (falta token o credenciales).
* **403 Forbidden:** Autenticado pero sin permisos suficientes.
* **404 Not Found:** El recurso solicitado no existe.
* **422 Unprocessable Entity:** Los datos son sintácticamente correctos pero semánticamente inválidos.
* **429 Too Many Requests:** Rate limit excedido. El cliente debe esperar.
* **500 Internal Server Error:** Error del servidor (bug en tu código).

### Buenas Prácticas de Diseño de APIs
* **URLs como sustantivos, no verbos:** `/api/users` (correcto) vs `/api/getUsers` (incorrecto).
* **Plurales para colecciones:** `/api/users` (colección), `/api/users/123` (recurso individual).
* **Versionamiento:** Usa `/api/v1/users` para poder evolucionar la API sin romper clientes existentes.
* **Paginación:** Nunca devuelvas todos los registros de golpe. Usa `?page=1&limit=20`.
* **Filtrado:** Permite filtrar por query params: `?status=active&role=admin`.
* **Respuestas consistentes:** Siempre devuelve la misma estructura: `{"data": ..., "error": null, "message": "OK"}`.

## FastAPI: El Framework Recomendado en Nexus DevHub

### ¿Por qué FastAPI?
* **Rendimiento:** Es uno de los frameworks más rápidos de Python, comparable con Go y Node.js.
* **Type Hints:** Usa tipado de Python para validar datos automáticamente. Si defines `edad: int` y el cliente envía `"hola"`, FastAPI devuelve 422 automáticamente.
* **Documentación Automática:** Genera Swagger UI y ReDoc automáticamente en `/docs` y `/redoc`.
* **Asincronismo Nativo:** Soporte para `async/await` que permite manejar miles de peticiones concurrentes.
* **Integración con Pydantic:** Validación y serialización de datos con modelos tipados.

### Estructura Recomendada de un Proyecto FastAPI
* `main.py` → Punto de entrada, configuración de la app, middleware, CORS.
* `routes/` → Un archivo por dominio: `routes/users.py`, `routes/agents.py`.
* `models/` → Modelos Pydantic para validación: `models/user.py`.
* `services/` → Lógica de negocio: `services/agent_service.py`.
* `database/` → Configuración de base de datos y migraciones.
* `tests/` → Tests organizados por dominio: `tests/test_users.py`.

## Webhooks y Eventos

### ¿Qué son los Webhooks?
Son callbacks HTTP que un servicio envía a tu servidor cuando ocurre un evento:
* GitHub envía un webhook a tu servidor cuando alguien hace push a tu repo.
* Stripe envía un webhook cuando un pago es procesado.
* Discord envía un webhook cuando alguien envía un mensaje en un canal.

### Buenas Prácticas para Webhooks
* **Verifica las firmas:** Cada webhook incluye una firma criptográfica. Verifícala para asegurar que la petición viene del servicio real y no de un atacante.
* **Responde rápido:** Responde con 200 OK inmediatamente y procesa el evento asincrónicamente. Si tardas mucho, el servicio reenviará el webhook pensando que falló.
* **Idempotencia:** Diseña tu handler para que procesar el mismo webhook dos veces no cause problemas (ej. no cobrar dos veces).

## WebSockets y Comunicación en Tiempo Real
* A diferencia de HTTP request/response, WebSockets mantienen una conexión persistente bidireccional.
* **Cuándo usarlos:** Chat en tiempo real, dashboards con datos en vivo, juegos multijugador, notificaciones push.
* **Framework recomendado:** FastAPI soporta WebSockets nativamente. Para frontend, usa la API nativa de WebSocket del navegador o Socket.IO.
* **Consideración:** Los WebSockets consumen más recursos del servidor que HTTP. Úsalos solo cuando realmente necesites comunicación en tiempo real.

## Integración de APIs con Agentes IA
* Los agentes LangGraph pueden consumir APIs externas como herramientas (`@tool`). Define funciones que hagan requests HTTP y regístrenlas como tools del LLM.
* Siempre implementa timeout (máximo 30 segundos) y retry con backoff exponencial para llamadas a APIs externas.
* Cachea respuestas de APIs que no cambian frecuentemente (ej. tasas de cambio se actualizan cada hora, no cada request).
* Valida la respuesta de APIs externas antes de pasarla al LLM: parsea JSON, verifica status codes, maneja errores.

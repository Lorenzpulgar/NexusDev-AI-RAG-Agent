# Buenas Prácticas de Código Limpio Generado por IA (Vibecoding Profesional)

La IA acelera la escritura, pero el desarrollador humano es responsable de la calidad, la seguridad y el mantenimiento. El "vibecoding" no significa código sin estándares; significa usar la IA como copiloto mientras tú mantienes el volante.

## Qué es el Vibecoding y Cómo Hacerlo Bien
El vibecoding es el proceso de desarrollar software guiado por intención natural (lenguaje humano) usando agentes IA como ClaudeCode, Cursor o Copilot. El vibecoder describe lo que quiere y la IA genera el código. Esto es poderoso, pero peligroso sin disciplina.

### Las 5 Reglas de Oro del Vibecoder Profesional
1. **Entiende antes de aceptar:** Nunca hagas merge de código que no puedas explicar. Si la IA generó algo y no entiendes qué hace, pídele que lo explique línea por línea antes de aceptarlo.
2. **Itera en bloques pequeños:** No pidas "hazme una app completa". Divide en pasos: primero la estructura, luego la lógica, luego los estilos, luego los tests. Revisa cada bloque antes de continuar.
3. **Prompt con contexto, no con esperanza:** Un prompt como "hazme un login" produce basura. Un prompt como "crea un endpoint POST /auth/login en FastAPI que reciba email y password, valide contra una tabla users en PostgreSQL usando SQLAlchemy, y retorne un JWT con expiración de 24h" produce código profesional.
4. **Versiona absolutamente todo:** Haz commits frecuentes después de cada paso funcional. Si la IA rompe algo en la iteración 5, puedes revertir a la iteración 4 sin perder todo tu progreso.
5. **La IA no reemplaza el testing:** Que el código "se vea bien" no significa que funcione. Ejecuta, prueba, rompe y solo entonces acepta.

## Estándares de Código y Stack Aceptado
Nuestro Office de Arquitectura AI aprueba el uso de agentes generativos para los siguientes stacks principales:
* **Backend y Lógica de Datos:** Python (FastAPI, Django), LangChain, LangGraph.
* **Frontend y Web:** JavaScript/TypeScript, React, Next.js, HTML5/CSS3.
* **Desarrollo Interactivo y Videojuegos:** Luau (para Roblox Studio) y C# (para Unity).
* **Infraestructura:** Docker, docker-compose, GitHub Actions para CI/CD.
* **Bases de Datos:** PostgreSQL, SQLite, Redis, MongoDB. Para vectoriales: FAISS, ChromaDB, Pinecone.

## Principios de Clean Code en la Era de la IA

### Nomenclatura Clara y Consistente
* Las variables deben describir su contenido: `usuario_activo` en lugar de `ua` o `x`.
* Las funciones deben describir su acción: `calcular_precio_con_descuento()` en lugar de `proc()`.
* Los archivos deben organizarse por dominio: `auth/login.py`, `payments/stripe_handler.py`.
* En Python usa snake_case. En JavaScript/TypeScript usa camelCase. Nunca mezcles convenciones.

### Funciones Pequeñas y con Propósito Único
* Una función debe hacer UNA cosa. Si necesitas usar la palabra "y" para describir lo que hace, divídela en dos.
* Máximo 20-30 líneas por función como regla general. Si es más larga, probablemente hace demasiado.
* Evita efectos secundarios: una función que calcula un precio no debe también enviar un email.

### Manejo de Errores Robusto
* Nunca uses `except: pass` o `catch(e) {}` vacíos. Siempre registra el error o lanza una excepción significativa.
* Usa tipos de excepción específicos: `except ValueError` en lugar de `except Exception`.
* Implementa logging estructurado con niveles (DEBUG, INFO, WARNING, ERROR) desde el día 1.
* Los agentes IA deben manejar gracefully los errores de APIs externas (timeouts, rate limits, respuestas malformadas).

### Comentarios Útiles vs Ruido
* No comentes QUÉ hace el código (el código debería ser autoexplicativo). Comenta POR QUÉ se tomó una decisión.
* Malo: `# Suma a + b` → `resultado = a + b`
* Bueno: `# Usamos caché de 5 min porque la API de precios tiene rate limit de 100 req/min` → `@cache(ttl=300)`
* Usa docstrings en funciones públicas para explicar parámetros, retorno y excepciones posibles.

## Directrices de Diseño Visual e Interfaces (UI/UX)
Cuando utilices IA para generar componentes de interfaz de usuario (ej. con v0.dev o Claude Artifacts), los estilos deben alinearse con nuestra identidad visual:
* Se priorizan estéticas inmersivas como el **Cyberpunk** (colores neón, fondos oscuros, terminales) o el **Solarpunk** (tonos verdes, interfaces orgánicas y sostenibles).
* Para herramientas internas, el diseño debe ser estrictamente **Minimalista** (espacios en blanco, tipografías legibles sin serifa, reducción de ruido visual).
* Usa sistemas de diseño consistentes: define una paleta de colores, tipografía y espaciado ANTES de generar componentes individuales.
* La accesibilidad no es opcional: contraste mínimo AA (4.5:1), tamaños de fuente legibles (mínimo 16px para texto base), y navegación por teclado.

## Testing y Refactorización del Código IA

### Prohibido el "Copy-Paste" Ciego
Todo código generado por IA debe pasar por linters automatizados antes de hacer commit:
* **Python:** usa `ruff` o `flake8` para linting, `black` para formato automático, `mypy` para chequeo de tipos.
* **JavaScript/TypeScript:** usa `eslint` con reglas estrictas, `prettier` para formato.
* Configura pre-commit hooks que ejecuten estos linters automáticamente antes de cada commit.

### Pruebas Unitarias Obligatorias
Usa a tu agente asistente para generar los tests unitarios inmediatamente después de generar la lógica de negocio:
* **Python:** pytest con cobertura mínima del 70%. Usa `pytest-cov` para medir.
* **JavaScript:** Jest o Vitest con mínimo 70% de cobertura.
* **Regla de Nexus:** Nunca hagas merge de un PR que baje el porcentaje de cobertura del repositorio.

### Refactorización Continua
* Después de que el código funcione, pídele a la IA que lo refactorice para mejorar legibilidad y rendimiento.
* Busca código duplicado (DRY - Don't Repeat Yourself) y extráelo a funciones o módulos reutilizables.
* Revisa las dependencias: si importaste una librería de 50MB solo para usar una función, probablemente puedas implementarla tú mismo en 10 líneas.

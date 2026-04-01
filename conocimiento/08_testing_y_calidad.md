# Testing y Calidad de Software: Guía Completa

Sin tests automatizados, tu proyecto es una bomba de tiempo. Cada cambio que haces (o que la IA genera) puede romper funcionalidades existentes sin que te enteres hasta que un usuario lo reporte en producción.

## La Pirámide de Testing

### 1. Tests Unitarios (Base de la Pirámide - 70% del total)
Verifican que funciones individuales producen el resultado correcto para inputs dados.
* **Qué testear:** Funciones puras, lógica de negocio, transformaciones de datos, validaciones.
* **Qué NO testear unitariamente:** Llamadas a APIs externas, bases de datos, interfaces de usuario.
* **Herramientas:**
  - Python: `pytest` (obligatorio en Nexus DevHub). Usa `pytest-cov` para medir cobertura.
  - JavaScript: `Jest` o `Vitest`.
* **Ejemplo práctico para agentes LangGraph:** Testea tu función router aislada: dado un estado con pregunta "hola", verifica que devuelve `{"decision": "GENERAL"}`.

### 2. Tests de Integración (Medio - 20% del total)
Verifican que múltiples componentes trabajan correctamente juntos.
* **Qué testear:** Que tu cadena `prompt | llm` produce respuestas coherentes. Que tu retriever FAISS devuelve documentos relevantes. Que tu API endpoint responde con el status code correcto.
* **Herramientas:**
  - Python: `pytest` con fixtures para bases de datos temporales.
  - APIs: `httpx` o `requests` con un servidor de pruebas.
* **Ejemplo para agentes:** Ejecuta el grafo completo con una pregunta conocida y verifica que la ruta tomada y el formato de respuesta son correctos.

### 3. Tests End-to-End (Cima - 10% del total)
Verifican el flujo completo desde la perspectiva del usuario.
* **Qué testear:** El usuario escribe una pregunta → el agente la routea → busca información → responde correctamente → la respuesta aparece en la interfaz.
* **Herramientas:**
  - Web: Playwright, Selenium, Cypress.
  - Streamlit: `streamlit-testing-library` o tests manuales documentados.
* **Cuándo usarlos:** Solo para flujos críticos de negocio. Son lentos y frágiles.

## Testing Específico para Agentes IA

### El Problema de la No-Determinismo
Los LLMs no son deterministas: la misma pregunta puede producir respuestas diferentes. Esto hace que los tests tradicionales de "input X → output exacto Y" no funcionen directamente.

### Estrategias de Testing para LLMs
1. **Tests de Clasificación:** Para el router, verifica que clasifica correctamente un conjunto de preguntas conocidas. La clasificación (RAG/TOOL_WEB/GENERAL) SÍ es determinista si usas temperature=0.
2. **Tests de Formato:** Verifica que la respuesta tiene el formato esperado (no está vacía, no excede cierta longitud, no contiene patrones prohibidos).
3. **Tests de Relevancia Semántica:** Usa embeddings para verificar que la respuesta es semánticamente similar a una respuesta de referencia (cosine similarity > 0.7).
4. **Tests de Guardrails:** Verifica que el agente rechaza correctamente prompt injections, preguntas fuera de alcance y contenido malicioso.
5. **Tests de Regresión con Golden Datasets:** Mantén un conjunto de pares pregunta-respuesta "golden" y verifica periódicamente que el agente sigue respondiendo correctamente.

### Mocking de LLMs para Tests
* No llames al LLM real en cada test unitario (es lento y costoso).
* Usa mocks que devuelvan respuestas predefinidas: `unittest.mock.patch` en Python.
* Para tests de integración con LLM real, usa un modelo pequeño y barato (llama-3.1-8b) o un mock server local.

## Métricas de Calidad de Código

### Cobertura de Tests
* **Mínimo aceptable en Nexus DevHub:** 70% de cobertura de código.
* **Objetivo ideal:** 80-90%. Más del 90% suele indicar tests frágiles que testean implementación en lugar de comportamiento.
* **Cómo medir:** `pytest --cov=. --cov-report=html` genera un reporte visual interactivo.

### Complejidad Ciclomática
* Mide cuántos caminos de ejecución tiene una función (if/else, loops, try/catch).
* **Regla:** Si una función tiene complejidad > 10, divídela en funciones más pequeñas.
* **Herramienta:** `radon` para Python: `radon cc . -a -s`.

### Deuda Técnica
* Es el costo futuro de cambios que deberías hacer ahora pero postergas. La IA genera deuda técnica rápidamente si no revisas y refactorizas.
* **Indicadores de deuda técnica:** Código duplicado, funciones de 100+ líneas, archivos de 500+ líneas, TODO comments abandonados, tests deshabilitados.
* **Cómo gestionarla:** Dedica el 20% del sprint a pagar deuda técnica (refactorizar, documentar, agregar tests).

## Linters y Formatters Obligatorios

### Python
* **Ruff:** Linter ultrarrápido que reemplaza a flake8, isort y pyflakes. Configuración recomendada en `pyproject.toml`.
* **Black:** Formatter automático con opiniones fuertes. Elimina discusiones sobre estilo: ejecutas `black .` y todo el código se formatea igual.
* **MyPy:** Verificador de tipos estáticos. Añade type hints a tus funciones y MyPy detecta errores de tipos antes de ejecutar.

### JavaScript/TypeScript
* **ESLint:** Linter configurable con reglas para calidad de código, mejores prácticas y errores comunes.
* **Prettier:** Formatter automático similar a Black. Se integra con ESLint para no tener conflictos.
* **TypeScript:** Usar TypeScript en lugar de JavaScript puro no es opcional para proyectos serios. El sistema de tipos previene una categoría entera de bugs.

### Pre-commit Hooks
Configura hooks que ejecuten linters y formatters automáticamente antes de cada commit:
* Instala `pre-commit` y crea un archivo `.pre-commit-config.yaml` en la raíz del proyecto.
* Hooks recomendados: trailing-whitespace, end-of-file-fixer, check-yaml, black, ruff, mypy.
* Beneficio: Es imposible hacer commit de código que no pasa los estándares del proyecto.

## Code Review con IA
* Usa agentes IA (ClaudeCode, Copilot Chat) para hacer una primera pasada de review automática antes del review humano.
* Pídele al agente que identifique: bugs potenciales, violaciones de SOLID, código duplicado, oportunidades de refactorización, y tests faltantes.
* El review humano se enfoca en: lógica de negocio, decisiones de arquitectura y edge cases que la IA podría no captar.

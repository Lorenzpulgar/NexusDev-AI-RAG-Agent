# Modernización de Código Legacy y Documentación Automática

Uno de los mayores valores de la IA en la ingeniería de software es el mantenimiento de sistemas heredados (Legacy). En Nexus DevHub, ayudamos a equipos a migrar sistemas antiguos sin perder las reglas de negocio que tardaron años en construirse.

## Qué es Código Legacy y Por Qué Importa
Código legacy no significa "código viejo y malo". Legacy es cualquier código que:
* Genera valor de negocio pero nadie entiende completamente cómo funciona.
* No tiene tests automatizados, por lo que cualquier cambio puede romper funcionalidades inesperadas.
* Usa tecnologías o patrones que ya no reciben soporte o actualizaciones de seguridad.
* Fue escrito por personas que ya no están en el equipo y no dejaron documentación.

## Estrategia de Migración Progresiva (El Patrón Strangler Fig)
NO intentes reescribir todo el sistema de una vez. Eso es un antipatrón llamado "Big Rewrite" que fracasa en el 70% de los casos. En su lugar, usa el patrón Strangler Fig:

### Fase 1: Comprender
1. **Alimenta al LLM con el código legacy:** Usa herramientas RAG para crear una base de conocimiento vectorial con toda la documentación legacy, el código fuente y los tickets históricos de Jira/GitHub Issues.
2. **Genera documentación automática:** Pídele al agente que explique módulo por módulo qué hace el sistema, qué entradas recibe y qué salidas produce.
3. **Identifica las reglas de negocio críticas:** Las reglas de negocio están enterradas en condicionales if/else, validaciones y transformaciones de datos. El LLM puede extraerlas y listarlas.

### Fase 2: Envolver (Wrap)
1. **Crea una capa de API sobre el sistema legacy:** Sin tocar el código viejo, pon un API Gateway (FastAPI, Express) delante que intercepte las peticiones.
2. **Implementa tests de integración:** Antes de migrar cualquier módulo, escribe tests que capturen el comportamiento actual exacto del sistema legacy. Estos tests son tu red de seguridad.
3. **Redirige tráfico gradualmente:** El nuevo sistema maneja las peticiones nuevas; el legacy sigue manejando las existentes. Coexisten sin conflicto.

### Fase 3: Reemplazar
1. **Migra módulo por módulo:** Emplea agentes IA para traducir módulos específicos del lenguaje legacy al stack moderno (ej. Java monolítico → microservicios Python/FastAPI).
2. **Valida con los tests de integración:** Cada módulo migrado debe pasar los mismos tests que el módulo original. Si los tests pasan, el comportamiento es idéntico.
3. **Desacopla el frontend:** Separa la interfaz de usuario antigua y reconstrúyela utilizando componentes modernos (React, Next.js) que consuman la nueva API.
4. **Retira el legacy:** Solo cuando el 100% del tráfico pasa por el nuevo sistema y todos los tests pasan, apaga el sistema viejo.

## Lenguajes y Migraciones Comunes
* **Java monolítico → Python (FastAPI) + React:** La migración más frecuente en empresas medianas. FastAPI ofrece rendimiento comparable con 10x menos código.
* **PHP (WordPress/Laravel) → Next.js + Headless CMS:** Para empresas que quieren mantener la gestión de contenido pero modernizar la experiencia de usuario.
* **Scripts de Excel/VBA → Python + Streamlit:** Muy común en empresas que dependen de hojas de cálculo complejas para procesos críticos de negocio.
* **COBOL/RPG → Python:** Migración de sistemas bancarios y financieros. Requiere extremo cuidado con las reglas de cálculo numérico.

## Estándares de Documentación en Nexus DevHub

### Documentación Obligatoria
Todo agente IA y proyecto desarrollado en Nexus DevHub debe incluir:

1. **README.md:** Archivo raíz del repositorio con:
   * Descripción del proyecto y su propósito.
   * Instrucciones paso a paso para configurar el entorno de desarrollo (con versiones exactas de Python, Node, etc.).
   * Cómo ejecutar la aplicación localmente.
   * Cómo ejecutar los tests.
   * Variables de entorno necesarias (sin incluir los valores reales, solo los nombres).

2. **ARCHITECTURE.md:** Documento que explica:
   * La arquitectura general del sistema (con diagramas de flujo si usa LangGraph o sistemas multi-agente).
   * Decisiones de diseño significativas y por qué se tomaron (Architecture Decision Records - ADRs).
   * Dependencias externas y sus propósitos.

3. **CHANGELOG.md:** Registro de cambios por versión siguiendo el formato Keep a Changelog:
   * Added: funcionalidades nuevas.
   * Changed: cambios en funcionalidades existentes.
   * Fixed: corrección de bugs.
   * Removed: funcionalidades eliminadas.

### Documentación Generada por IA
* Los agentes deben ser capaces de autogenerar su propia documentación técnica.
* Usa docstrings en Python (format Google o NumPy) y JSDoc en JavaScript para que las herramientas de documentación automática (Sphinx, TypeDoc) puedan generar sitios de referencia.
* Genera diagramas de flujo de LangGraph explicados paso a paso usando Mermaid dentro de archivos Markdown.
* Documenta los prompts usados en cada nodo del agente, incluyendo su propósito, inputs esperados y outputs posibles.

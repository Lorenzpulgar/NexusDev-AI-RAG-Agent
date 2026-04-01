# Control de Versiones con Git: Guía Profesional para Vibecoders

Git no es opcional. Es la habilidad más fundamental que separa a un programador profesional de un aficionado. Si no usas Git, estás construyendo sobre arena.

## Conceptos Fundamentales

### ¿Qué es Git y por qué es no-negociable?
Git es un sistema de control de versiones distribuido. Registra cada cambio que haces en tu código, cuándo lo hiciste y por qué. Permite:
* **Revertir errores:** Si la IA genera código que rompe todo, puedes volver al estado anterior en segundos.
* **Colaborar sin conflictos:** Múltiples personas pueden trabajar en el mismo proyecto simultáneamente sin sobreescribir el trabajo de otros.
* **Auditar cambios:** Puedes ver exactamente quién cambió qué línea, cuándo y por qué.
* **Experimentar sin miedo:** Crea ramas para probar ideas locas. Si funcionan, las integras. Si no, las eliminas sin afectar el proyecto principal.

### El Flujo Básico de Git
1. `git init` → Inicializa un repositorio en tu proyecto.
2. `git add .` → Prepara los archivos modificados para el commit.
3. `git commit -m "descripción del cambio"` → Guarda una foto instantánea de tu código.
4. `git push origin main` → Sube tus cambios al repositorio remoto (GitHub).

## Estrategia de Branching (Ramas) en Nexus DevHub

### Git Flow Simplificado
* **main:** La rama de producción. Siempre debe estar estable y funcional. NADIE hace push directo a main.
* **develop:** La rama de integración. Aquí se juntan las features antes de ir a producción.
* **feature/nombre-feature:** Ramas individuales para cada funcionalidad nueva. Se crean desde develop y se integran de vuelta con Pull Request.
* **hotfix/nombre-fix:** Ramas de emergencia para bugs críticos en producción. Se crean desde main y se integran tanto a main como a develop.

### Convención de Nombres de Ramas
* `feature/add-rag-search` → Nueva funcionalidad.
* `fix/router-classification-bug` → Corrección de bug.
* `refactor/clean-prompt-templates` → Refactorización sin cambio de funcionalidad.
* `docs/update-readme` → Solo cambios de documentación.

## Commits Profesionales

### Conventional Commits (Estándar de Nexus DevHub)
Cada mensaje de commit debe seguir el formato: `tipo(alcance): descripción`
* `feat(router): add web search routing classification` → Nueva funcionalidad.
* `fix(rag): resolve FAISS index loading error on Windows` → Corrección de bug.
* `refactor(prompts): simplify system prompt for general node` → Refactorización.
* `docs(readme): add deployment instructions for Render` → Documentación.
* `style(css): adjust vaporwave color palette` → Cambios visuales.
* `test(auth): add unit tests for JWT validation` → Tests.
* `chore(deps): update langchain to 1.2.23` → Mantenimiento.

### Reglas de Oro para Commits
* **Commits atómicos:** Cada commit debe representar UN cambio lógico completo. No mezcles "arreglar bug de login" con "cambiar color del botón" en el mismo commit.
* **Commits frecuentes:** Haz commit cada vez que algo funcione. Vibecoders: después de cada iteración exitosa con la IA, haz commit.
* **Mensajes descriptivos:** "fix bug" es inaceptable. "fix(router): prevent GENERAL classification for technical questions" es profesional.
* **Nunca hagas commit de archivos generados:** `node_modules/`, `__pycache__/`, `.env`, archivos `.pyc`, carpetas `dist/` y `build/` deben estar en `.gitignore`.

## El archivo .gitignore Esencial
Todo proyecto debe tener un `.gitignore` que incluya como mínimo:
* `.env` → Variables de entorno con API keys.
* `__pycache__/` → Archivos compilados de Python.
* `node_modules/` → Dependencias de Node.js.
* `.venv/` o `venv/` → Entorno virtual de Python.
* `*.pyc` → Archivos compilados individuales.
* `.DS_Store` → Archivos de sistema de macOS.
* `dist/` y `build/` → Archivos de producción generados.
* Archivos de IDE: `.vscode/`, `.idea/`.

## Pull Requests (PRs) y Code Review

### Cómo Escribir un Buen Pull Request
1. **Título claro:** Usa el formato de Conventional Commits: `feat(rag): implement semantic search with FAISS`.
2. **Descripción:** Explica QUÉ cambiaste, POR QUÉ lo cambiaste y CÓMO probarlo.
3. **Tamaño razonable:** Un PR de 500+ líneas es imposible de revisar bien. Divide en PRs más pequeños.
4. **Screenshots:** Si cambiaste algo visual (UI, CLI output), incluye capturas de antes y después.
5. **Tests:** Incluye los tests que validan tus cambios. Un PR sin tests genera deuda técnica.

### Cómo Hacer Code Review como Arquitecto
* Revisa la lógica, no solo la sintaxis. Los linters se encargan de la sintaxis.
* Pregunta "¿qué pasa si...?" para edge cases: ¿Qué pasa si el input es vacío? ¿Si la API no responde? ¿Si hay 10,000 usuarios simultáneos?
* Busca código duplicado y sugiere abstracciones.
* Verifica que no haya API keys, credenciales o datos sensibles en el diff.
* Sé constructivo: en lugar de "esto está mal", di "esto podría ser más eficiente si usamos X porque Y".

## GitHub como Plataforma de Colaboración
* **Issues:** Usa GitHub Issues para documentar bugs, features y tareas. Etiquétalos (bug, enhancement, help wanted).
* **Projects:** Usa GitHub Projects (tableros Kanban) para organizar el trabajo del equipo: "To Do", "In Progress", "In Review", "Done".
* **Actions:** Configura GitHub Actions para CI/CD automatizado. Ejecuta tests, linters y deploys automáticamente.
* **Releases:** Crea releases con tags semánticos (v1.0.0, v1.1.0) para marcar versiones estables y publicarlas.

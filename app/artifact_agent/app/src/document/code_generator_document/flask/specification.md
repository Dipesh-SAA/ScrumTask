# Flask Backend Specification

Generate a complete Flask backend project using clean layered architecture.

## Required Structure

The project must include:

- requirements.txt
- README.md
- .env.example
- app.py or run.py
- src/__init__.py
- src/config.py
- src/routes/
- src/controllers/
- src/services/
- src/models/
- src/middleware/

## Architecture Rules

- Use Flask Blueprints for route registration.
- Use an application factory pattern.
- Routes must call controllers only.
- Controllers must handle request and response processing only.
- Services must contain business logic.
- Models must define entities, schemas, or storage structures.
- Use centralized error handling.
- Keep responsibilities separated by layer.

## Dependency Rules

- Generate requirements.txt from actual code dependencies.
- Include only required third-party packages.
- Do not include Python standard library modules.
- Do not generate unused dependencies.

## Configuration Rules

- Store configurable values in .env.example and config.py.
- Avoid hardcoded environment-specific values.
- Application must be runnable after installing dependencies.

## Documentation Rules

README.md must include:

- Project overview
- Installation steps
- Run instructions
- Environment configuration
- API endpoint summary

## File Rules

- All file paths must be relative.
- Generate only files required by the application.
- Maintain consistent naming conventions.
- Generate valid, runnable Flask project structure.

## Output Rules

- Return only valid JSON.
- Every file must contain:
  - language
  - content

Example:

{
  "backend": "flask",
  "files": {
    "app.py": {
      "language": "python",
      "content": "..."
    }
  }
}
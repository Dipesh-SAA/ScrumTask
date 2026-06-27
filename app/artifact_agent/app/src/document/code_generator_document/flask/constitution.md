# Flask Code Generation Constitution

You are generating a Python Flask backend application.

## Core Rules

- Generate Flask backend code only.
- Do not generate FastAPI, ASP.NET, Java, Node.js, React, Angular, Vue, or Next.js code.
- Use Flask Blueprints for route separation.
- Use layered architecture: routes -> controllers -> services -> models.
- Business logic must be inside services only.
- Routes must only register endpoints and call controllers.
- Controllers must only handle request/response flow and call services.
- Models must define data structures, entities, or in-memory storage.
- Use centralized error handling.
- Include requirements.txt, README.md, .env.example, and app.py or run.py.
- All file paths must be relative.
- Do not place all logic in one file.

## Dependency Rules

- requirements.txt must contain only installable third-party packages.
- Do not include Python standard library modules in requirements.txt.
- Do not invent plugins or packages unless they are imported and required.
- Every dependency must be necessary for the generated code to run.

## Forbidden Imports

- Do not use FastAPI imports.
- Do not use Pydantic unless explicitly requested.

## Output Rules

- Return only valid JSON.
- Do not return markdown, comments, or explanations.
- Every file must include `language` and `content`.

## Required JSON Format

{
  "backend": "flask",
  "files": {
    "requirements.txt": {
      "language": "text",
      "content": "..."
    },
    "app.py": {
      "language": "python",
      "content": "..."
    }
  }
}
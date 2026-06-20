# Python LangGraph FastAPI Backend Code Generator Specification

Read the OpenAPI YAML and generate Python FastAPI source code using LangGraph-style architecture according to `x-backend`.

## Backend Selection

Use only the backend value from:

x-backend: <backend>

If `x-backend` is `python` or `fastapi`, generate Python FastAPI source code using LangGraph-style architecture.

Do not generate code for any other backend in this specification file.

## Output Format

Return ONLY valid JSON.

Do not return markdown.
Do not return explanations.
Do not return code fences.

The JSON must follow this exact structure:

{
  "backend": "python",
  "files": {
    "relative/path/file.ext": {
      "language": "python",
      "content": "file content here"
    }
  }
}

## Project Type

Generate a FastAPI backend project with LangGraph-style orchestration.

The generated project must be runnable with:

python -m uvicorn main:app --reload

## Required Root Files

For Python FastAPI LangGraph architecture, these files are allowed at project root:

- main.py
- requirements.txt
- README.md
- .env.example

## Required Folder Structure

Use this structure:

- api/routes/<name>_routes.py
- models/requests/<name>_request.py
- models/responses/<name>_response.py
- models/responses/error_response.py
- graph/state/<name>_state.py
- graph/nodes/<name>_nodes.py
- graph/workflows/<name>_workflow.py
- graph/runners/<name>_runner.py
- services/<name>_service.py

## Optional Folder Structure

Use these only if required by YAML or instructions:

- repositories/<name>_repository.py
- database/db.py
- database/models.py
- core/config.py

## Strictly Forbidden Paths

Never generate paths like:

- <ProjectName>/main.py
- <ProjectName>/requirements.txt
- src/main.py
- src/app/main.py
- app/<ProjectName>/main.py
- python/main.py
- routes/<name>_routes.py
- requests/<name>_request.py
- responses/<name>_response.py
- state/<name>_state.py
- nodes/<name>_nodes.py
- workflows/<name>_workflow.py
- runners/<name>_runner.py

## Source Code Requirements

Generate clean Python FastAPI code.

Use:

- FastAPI app object named `app`
- Pydantic models for request and response validation
- APIRouter for route files
- LangGraph StateGraph for workflow orchestration
- Graph state TypedDict or Pydantic model
- Graph nodes for processing steps
- Graph workflow builder
- Graph runner called by route
- Service layer for business logic
- Proper HTTP status codes
- Proper exception handling
- Error response model
- requirements.txt

## main.py Rules

`main.py` must contain:

from fastapi import FastAPI

app = FastAPI()

If routers are used, include them in `main.py`.

The app object name MUST be:

app

Do not name it:

application
fastapi_app
api

## Route Rules

Route files must be placed in:

api/routes/<name>_routes.py

Routes must:

- Use APIRouter
- Match OpenAPI YAML paths and methods
- Use request models where requestBody exists
- Use response models where schemas exist
- Call graph runner
- Not contain business logic directly

## LangGraph State Rules

State files must be placed in:

graph/state/<name>_state.py

State must define the input, intermediate fields, output fields, and error fields required by the workflow.

Use TypedDict for graph state unless Pydantic is more suitable.

## LangGraph Node Rules

Node files must be placed in:

graph/nodes/<name>_nodes.py

Nodes must:

- Accept state as input
- Return updated state
- Call service functions for business logic
- Not contain FastAPI route code

## LangGraph Workflow Rules

Workflow files must be placed in:

graph/workflows/<name>_workflow.py

Workflow must:

- Use StateGraph from langgraph.graph
- Add required nodes
- Add edges between nodes
- Set entry point
- Compile the graph
- Return compiled workflow

For simple APIs, create a simple linear workflow:

validate_input -> process_request -> build_response

## LangGraph Runner Rules

Runner files must be placed in:

graph/runners/<name>_runner.py

Runner must:

- Accept request data
- Create initial graph state
- Invoke compiled workflow
- Return final response data
- Raise errors when graph state contains errors

## Service Rules

Service files must be placed in:

services/<name>_service.py

Services must contain business logic.

Do not put business logic directly inside route functions or graph workflow files.

## Model Rules

Request models must be placed in:

models/requests/<name>_request.py

Response models must be placed in:

models/responses/<name>_response.py

Error response must be placed in:

models/responses/error_response.py

## requirements.txt Rules

requirements.txt must include:

fastapi
uvicorn
pydantic
langgraph

If database is required, also include:

sqlalchemy

## Database Rules

If database is required, generate:

- database/db.py
- database/models.py
- repositories/<name>_repository.py

Use SQLAlchemy when database is required.

If no database is required, do not generate database files.

## Final File Path Validation

Before returning JSON:

1. Inspect every key in the `files` object.
2. Check that every file path is relative to the project root.
3. Do not include project name as the first folder.
4. Do not include API title as the first folder.
5. Do not include backend name as the first folder.
6. Do not include `src` as the first folder.
7. Do not generate graph files outside the `graph/` folder.
8. If any file violates the Python LangGraph structure, correct the path before returning.

## Final Requirement

The JSON `files` keys MUST contain the complete folder path exactly as it should appear on disk.

Return ONLY corrected valid JSON.
For every generated Python package folder, also generate an empty __init__.py file.
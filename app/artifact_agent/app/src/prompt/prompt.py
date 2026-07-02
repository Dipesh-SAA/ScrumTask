from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DOCUMENT_DIR = BASE_DIR / "document/yml_agent_document"

PROMPT_TEMPLATE = """
CONSTITUTION:
{constitution}

SPECIFICATION:
{specification}

USER INPUT:
{user_input}

Your work is to read the user input, constitution file,
specification file and user prompt.

Return ONLY valid OpenAPI YAML.

Do not return markdown.
Do not return code fences.
Do not return explanations.
Do not return any text before or after the YAML.
Do not forget x-backend in the YAML.
Set x-backend to a canonical generator value from the requested Tech Stack.
Backend Api values:
- ASP.NET Core Web API -> .net
- Node.js Express -> nodejs
- Python FastAPI -> python
- Python Flask -> flask
Frontend values:
- React -> react
- Angular -> angular
- Vue -> vue
- Next.js -> nextjs
DatabaseType values should be written to x-database, not x-backend:
- MongoDB -> mongodb
- SQL Server -> sqlserver
- MySQL -> mysql
- PostgreSQL -> postgresql
UI Library values should be written to x-ui-library:
- Tailwind CSS -> tailwindcss
- Material UI -> material-ui
- Bootstrap -> bootstrap
- Custom -> custom
AI/Agent Framework values should be written to x-ai-agent-framework:
- LangGraph -> langgraph
- LangChain -> langchain
"""

def load_document(name: str) -> str:
    path = DOCUMENT_DIR / name

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {path}"
        )

    return path.read_text(
        encoding="utf-8"
    )


def build_prompt(user_input: str) -> str:
    return PROMPT_TEMPLATE.format(
        constitution=load_document(
            "constitution.md"
        ),
        specification=load_document(
            "specification.md"        
        ),
        user_input=user_input,
    )

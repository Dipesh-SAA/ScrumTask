import json
import re
import yaml
import httpx
from pathlib import Path
from openai import (
    APIConnectionError,
    APIStatusError,
)
from app.Infrastrature.llm.loader import llm
from app.artifact_agent.app.src.prompt.prompt import build_prompt, PROMPT_TEMPLATE
from app.utils.wrapper import log_agent

# OUTPUT_FILE = Path(
#     "yml/openapi.yml"
# )

# OUTPUT_FILE = (
#     Path(__file__).resolve()
#     .parent.parent
#     / "document/yml"
#     / "openapi.yml"
# )

# def get_llm():
#     return llm

# def clean_llm_response(
#     text: str
# ) -> str:

#     text = str(text).strip()

#     text = re.sub(
#         r"<think>.*?</think>",
#         "",
#         text,
#         flags=re.IGNORECASE
#         | re.DOTALL,
#     )

#     fenced = re.search(
#         r"```(?:json|yaml|yml)?\s*(.*?)\s*```",
#         text,
#         flags=re.IGNORECASE
#         | re.DOTALL,
#     )

#     if fenced:
#         text = fenced.group(1)

#     return text.strip()

# def parse_llm_response(
#     text: str
# ):
#     text = clean_llm_response(
#         text
#     )

#     try:
#         return json.loads(text)

#     except json.JSONDecodeError:
#         pass

#     try:
#         parsed = yaml.safe_load(
#             text
#         )

#         if isinstance(
#             parsed,
#             dict
#         ):
#             return parsed

#     except Exception:
#         pass

#     return {
#         "raw_response": text
#     }

# def save_openapi_yaml(
#     data
# ):
#     OUTPUT_FILE.parent.mkdir(
#         parents=True,
#         exist_ok=True
#     )

#     yaml_content = yaml.dump(
#         data,
#         sort_keys=False,
#         default_flow_style=False,
#         allow_unicode=True,
#     )

#     OUTPUT_FILE.write_text(
#         yaml_content,
#         encoding="utf-8"
#     )


# async def yml_code_gen(
#     task: str,
#     techstack: str,
#     instructions: str
# ):
#     try:

#         user_input = f"""
# Task:
# {task}
# instructions:
# {instructions}

# rules:
# {PROMPT_TEMPLATE}

# Tech Stack:
# {techstack}



# """

#         llm_client = get_llm()

#         response = await llm_client.ainvoke(
#             build_prompt(user_input)
#         )

#         parsed_response = parse_llm_response(
#             response.content
#         )

#         save_openapi_yaml(
#             parsed_response
#         )

#         return parsed_response

#     except APIConnectionError as exc:
#         raise RuntimeError(
#             "Could not connect to LLM"
#         ) from exc

#     except APIStatusError as exc:
#         raise RuntimeError(
#             f"API Error: {exc}"
#         ) from exc

#     except httpx.HTTPError as exc:
#         raise RuntimeError(
#             f"Provider Error: {exc}"
#         ) from exc

# OUTPUT_FILE = Path(
#     "yml/openapi.yml"
# )

OUTPUT_FILE = (
    Path(__file__).resolve()
    .parent.parent
    / "document/yml"
    / "openapi.yml"
)

def get_llm():
    return llm

def clean_llm_response(
    text: str
) -> str:

    text = str(text).strip()

    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.IGNORECASE
        | re.DOTALL,
    )

    fenced = re.search(
        r"```(?:json|yaml|yml)?\s*(.*?)\s*```",
        text,
        flags=re.IGNORECASE
        | re.DOTALL,
    )

    if fenced:
        text = fenced.group(1)

    return text.strip()

def parse_llm_response(
    text: str
):
    text = clean_llm_response(
        text
    )

    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass

    try:
        parsed = yaml.safe_load(
            text
        )

        if isinstance(
            parsed,
            dict
        ):
            return parsed

    except Exception:
        pass

    return {
        "raw_response": text
    }

def save_openapi_yaml(
    data
):
    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    yaml_content = yaml.dump(
        data,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
    )

    OUTPUT_FILE.write_text(
        yaml_content,
        encoding="utf-8"
    )

def _normalize_label(value: str | None) -> str:
    label = str(value or "").lower().strip()
    label = re.sub(r"[_\-]+", " ", label)
    label = re.sub(r"\s+", " ", label)
    return label


def _is_placeholder(value: str | None) -> bool:
    label = _normalize_label(value)
    return not label or label.startswith("select ")


def _normalize_from_mapping(value: str | None, mapping: dict[str, str]) -> str:
    label = _normalize_label(value)

    if _is_placeholder(label):
        return ""

    if label in mapping:
        return mapping[label]

    for key in sorted(mapping, key=len, reverse=True):
        if key in label:
            return mapping[key]

    return label


def _extract_labeled_value(text: str | None, labels: tuple[str, ...]) -> str:
    if not text:
        return ""

    label_pattern = "|".join(re.escape(label) for label in labels)
    pattern = rf"(?im)^\s*(?:{label_pattern})\s*:\s*(.+?)\s*$"
    match = re.search(pattern, str(text))

    return match.group(1).strip() if match else ""


BACKEND_MAPPING = {
        "python": "python",
        "python fastapi": "python",
        "fastapi": "python",
        "python flask": "flask",
        "flask": "flask",
        ".net": ".net",
        ".net core": ".net",
        ".netcore": ".net",
        "dotnet": ".net",
        "dotnet core": ".net",
        "dotnetcore": ".net",
        "c#": ".net",
        "csharp": ".net",
        "asp.net": ".net",
        "asp.net core": ".net",
        "asp.net core api": ".net",
        "asp.net core web api": ".net",
        "asp.net web api": ".net",
        "asp.netcore": ".net",
        "asp.netcore webapi": ".net",
        "asp net core": ".net",
        "asp net core api": ".net",
        "asp net core web api": ".net",
        "aspnet": ".net",
        "aspnet web api": ".net",
        "aspnetcore": ".net",
        "aspnetcore api": ".net",
        "aspnetcore webapi": ".net",
        "c# api": ".net",
        "c# web api": ".net",
        "csharp api": ".net",
        "csharp web api": ".net",
        "java": "java",
        "spring": "java",
        "spring boot": "java",
        "node": "nodejs",
        "nodejs": "nodejs",
        "node.js": "nodejs",
        "node js": "nodejs",
        "node.js express": "nodejs",
        "node js express": "nodejs",
        "nodejs express": "nodejs",
        "express": "nodejs",
        "expressjs": "nodejs",
        "react": "react",
        "reactjs": "react",
        "react.js": "react",
        "angular": "angular",
        "angularjs": "angular",
        "ng": "angular",
        "vue": "vue",
        "vuejs": "vue",
        "vue.js": "vue",
        "next": "nextjs",
        "nextjs": "nextjs",
        "next.js": "nextjs",
        "sql": "sql",
        "sqlserver": "sql",
        "sql server": "sql",
        "mssql": "sql",
        "postgres": "postgresql",
        "postgresql": "postgresql",
        "postgre sql": "postgresql",
        "mysql": "mysql",
        "oracle": "oracle",
}

FRONTEND_MAPPING = {
    "react": "react",
    "angular": "angular",
    "vue": "vue",
    "next": "nextjs",
    "nextjs": "nextjs",
    "next.js": "nextjs",
}

DATABASE_MAPPING = {
    "mongodb": "mongodb",
    "mongo db": "mongodb",
    "mongo": "mongodb",
    "sql server": "sqlserver",
    "sqlserver": "sqlserver",
    "mssql": "sqlserver",
    "mysql": "mysql",
    "postgresql": "postgresql",
    "postgre sql": "postgresql",
    "postgres": "postgresql",
}

UI_LIBRARY_MAPPING = {
    "tailwind css": "tailwindcss",
    "tailwind": "tailwindcss",
    "material ui": "material-ui",
    "mui": "material-ui",
    "bootstrap": "bootstrap",
    "custom": "custom",
}

AI_AGENT_FRAMEWORK_MAPPING = {
    "langgraph": "langgraph",
    "lang graph": "langgraph",
    "langchain": "langchain",
    "lang chain": "langchain",
}


def normalize_backend(techstack: str | None) -> str:
    return _normalize_from_mapping(techstack, BACKEND_MAPPING)


def normalize_frontend(frontend: str | None) -> str:
    return _normalize_from_mapping(frontend, FRONTEND_MAPPING)


def normalize_database(database: str | None) -> str:
    return _normalize_from_mapping(database, DATABASE_MAPPING)


def normalize_ui_library(ui_library: str | None) -> str:
    return _normalize_from_mapping(ui_library, UI_LIBRARY_MAPPING)


def normalize_ai_agent_framework(framework: str | None) -> str:
    return _normalize_from_mapping(framework, AI_AGENT_FRAMEWORK_MAPPING)


def normalize_data_platform(platform: str | None) -> str:
    if _is_placeholder(platform):
        return ""
    return _normalize_label(platform)

def apply_requested_backend(
    data,
    techstack: str
):
    if isinstance(data, dict) and techstack:
        backend_value = _extract_labeled_value(
            techstack,
            ("Backend Api", "Backend API", "Backend", "API Backend"),
        )
        frontend_value = _extract_labeled_value(techstack, ("Frontend",))
        database_value = _extract_labeled_value(
            techstack,
            ("DatabaseType", "Database Type", "Database"),
        )
        ui_library_value = _extract_labeled_value(
            techstack,
            ("UI Library", "UILibrary"),
        )
        ai_agent_framework_value = _extract_labeled_value(
            techstack,
            ("AI/Agent Framework", "AI Agent Framework", "Agent Framework"),
        )
        data_platform_value = _extract_labeled_value(
            techstack,
            ("VIBE/Data Platform", "VIBE Data Platform", "Data Platform"),
        )
        has_labeled_technology = any(
            (
                backend_value,
                frontend_value,
                database_value,
                ui_library_value,
                ai_agent_framework_value,
                data_platform_value,
            )
        )

        backend = normalize_backend(backend_value)
        if not backend and not has_labeled_technology:
            backend = normalize_backend(techstack)

        frontend = normalize_frontend(frontend_value) or normalize_frontend(techstack)
        database = normalize_database(database_value)
        ui_library = normalize_ui_library(ui_library_value)
        ai_agent_framework = normalize_ai_agent_framework(ai_agent_framework_value)
        data_platform = normalize_data_platform(data_platform_value)

        if backend or frontend:
            data["x-backend"] = backend or frontend

        if frontend:
            data["x-frontend"] = frontend
        if database:
            data["x-database"] = database
        if ui_library:
            data["x-ui-library"] = ui_library
        if ai_agent_framework:
            data["x-ai-agent-framework"] = ai_agent_framework
        if data_platform:
            data["x-data-platform"] = data_platform

    return data


async def yml_code_gen(
    task: str,
    techstack: str,
    instructions: str | None = None,
    user_story_task_id: str = "",
):
    await log_agent(
        user_story_task_id=user_story_task_id,
        stage="OpenAPI YAML Generation",
        message="OpenAPI YAML Generation Started",
        status="Running",
        agent_name="Artifact YAML Agent",
    )

    try:

        user_input = f"""
Task:
{task}
instructions:
{instructions}

rules:
{PROMPT_TEMPLATE}

Tech Stack:
{techstack}



"""

        llm_client = get_llm()

        response = await llm_client.ainvoke(
            build_prompt(user_input)
        )

        parsed_response = parse_llm_response(
            response.content
        )
        parsed_response = apply_requested_backend(
            parsed_response,
            techstack
        )

        save_openapi_yaml(
            parsed_response
        )

        await log_agent(
            user_story_task_id=user_story_task_id,
            stage="OpenAPI YAML Generation",
            message="OpenAPI YAML Generation Completed",
            status="Completed",
            agent_name="Artifact YAML Agent",
        )

        return parsed_response

    except APIConnectionError as exc:
        await log_agent(
            user_story_task_id=user_story_task_id,
            stage="OpenAPI YAML Generation",
            message="Could not connect to LLM",
            status="Failed",
            agent_name="Artifact YAML Agent",
        )
        raise RuntimeError(
            "Could not connect to LLM"
        ) from exc

    except APIStatusError as exc:
        await log_agent(
            user_story_task_id=user_story_task_id,
            stage="OpenAPI YAML Generation",
            message=f"API Error: {exc}",
            status="Failed",
            agent_name="Artifact YAML Agent",
        )
        raise RuntimeError(
            f"API Error: {exc}"
        ) from exc

    except httpx.HTTPError as exc:
        await log_agent(
            user_story_task_id=user_story_task_id,
            stage="OpenAPI YAML Generation",
            message=f"Provider Error: {exc}",
            status="Failed",
            agent_name="Artifact YAML Agent",
        )
        raise RuntimeError(
            f"Provider Error: {exc}"
        ) from exc

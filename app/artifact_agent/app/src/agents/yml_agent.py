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

def normalize_backend(
    techstack: str
) -> str:
    backend = str(techstack or "").lower().strip()
    backend = re.sub(r"\s+", " ", backend)

    backend_mapping = {
        "python": "python",
        "fastapi": "python",
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
        "asp.netcore": ".net",
        "aspnetcore": ".net",
        "java": "java",
        "spring": "java",
        "spring boot": "java",
        "node": "nodejs",
        "nodejs": "nodejs",
        "node.js": "nodejs",
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
        "flask": "flask",
        "python flask": "flask",
        "sql": "sql",
        "sqlserver": "sql",
        "mssql": "sql",
        "postgres": "postgresql",
        "postgresql": "postgresql",
        "mysql": "mysql",
        "oracle": "oracle",
    }

    return backend_mapping.get(backend, backend)

def apply_requested_backend(
    data,
    techstack: str
):
    if isinstance(data, dict) and techstack:
        data["x-backend"] = normalize_backend(techstack)

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

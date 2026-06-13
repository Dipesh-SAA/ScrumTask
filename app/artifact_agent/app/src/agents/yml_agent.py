import json
import re
import yaml
import httpx
from pathlib import Path
from openai import (
    APIConnectionError,
    APIStatusError,
)
from app.artifact_agent.app.src.llm.loader import llm
from app.artifact_agent.app.src.prompt.prompt import build_prompt, PROMPT_TEMPLATE

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


async def yml_code_gen(
    task: str,
    techstack: str
    

):
    try:

        user_input = f"""
Task:
{task}

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

        save_openapi_yaml(
            parsed_response
        )

        return parsed_response

    except APIConnectionError as exc:
        raise RuntimeError(
            "Could not connect to LLM"
        ) from exc

    except APIStatusError as exc:
        raise RuntimeError(
            f"API Error: {exc}"
        ) from exc

    except httpx.HTTPError as exc:
        raise RuntimeError(
            f"Provider Error: {exc}"
        ) from exc
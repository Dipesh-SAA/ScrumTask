import json
import re
import yaml
import httpx
from openai import APIConnectionError, APIStatusError

from app.Infrastrature.llm.loader import llm
from app.test_case_agent.src.prompt import build_prompt


def parse_llm_json(text: str):
    text = str(text).strip()

    text = re.sub(r"^```(?:json|yaml)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(text[start:end + 1])
        except json.JSONDecodeError:
            pass

    try:
        parsed = yaml.safe_load(text)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass

    return {
        "error": "LLM returned neither valid JSON nor valid YAML",
        "raw_response": text
    }


async def test_case(user_story: str, task: str):
    try:
        response = await llm.ainvoke(build_prompt(user_story, task))

        return parse_llm_json(response.content)

    except APIConnectionError as exc:
        raise RuntimeError("Could not connect to OpenAI API") from exc

    except APIStatusError as exc:
        raise RuntimeError(
            f"OpenAI API error: {exc.status_code} {exc.message}"
        ) from exc

    except httpx.HTTPError as exc:
        raise RuntimeError(
            f"Could not connect to LLM provider: {exc}"
        ) from exc

import json
import re
import yaml
import httpx
from openai import APIConnectionError, APIStatusError

from app.Infrastrature.llm.loader import llm
from app.test_case_agent.src.prompt import build_prompt
from app.utils.wrapper import log_agent


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


async def test_case(UserStoryTaskId: str, user_story: str, task: str):
    await log_agent(
        user_story_task_id=UserStoryTaskId,
        stage="Test Case Generation",
        message="Test Case Generation Started",
        status="Running",
        agent_name="Test Case Agent",
    )

    try:
        response = await llm.ainvoke(build_prompt(UserStoryTaskId, user_story, task))
        result = parse_llm_json(response.content)

        await log_agent(
            user_story_task_id=UserStoryTaskId,
            stage="Test Case Generation",
            message="Test Case Generation Completed",
            status="Completed",
            agent_name="Test Case Agent",
        )

        return result

    except APIConnectionError as exc:
        await log_agent(
            user_story_task_id=UserStoryTaskId,
            stage="Test Case Generation",
            message="Could not connect to LLM provider",
            status="Failed",
            agent_name="Test Case Agent",
        )
        raise RuntimeError("Could not connect to LLM provider") from exc

    except APIStatusError as exc:
        await log_agent(
            user_story_task_id=UserStoryTaskId,
            stage="Test Case Generation",
            message=f"LLM provider API error: {exc.status_code} {exc.message}",
            status="Failed",
            agent_name="Test Case Agent",
        )
        raise RuntimeError(
            f"LLM provider API error: {exc.status_code} {exc.message}"
        ) from exc

    except httpx.HTTPError as exc:
        await log_agent(
            user_story_task_id=UserStoryTaskId,
            stage="Test Case Generation",
            message=f"Could not connect to LLM provider: {exc}",
            status="Failed",
            agent_name="Test Case Agent",
        )
        raise RuntimeError(
            f"Could not connect to LLM provider: {exc}"
        ) from exc

    except Exception as exc:
        await log_agent(
            user_story_task_id=UserStoryTaskId,
            stage="Test Case Generation",
            message=str(exc),
            status="Failed",
            agent_name="Test Case Agent",
        )
        raise

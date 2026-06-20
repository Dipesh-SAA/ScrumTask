import time
import traceback
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.test_case_agent.src.agent import test_case
from app.utils.logger import AgentLogger

test_case_agent = APIRouter(tags=["test_case"])
logger = AgentLogger()


class requestbody(BaseModel):
    user_story: str
    task: str


def safe_logger(**kwargs):
    try:
        return logger.log_event(**kwargs)
    except Exception as exc:
        print(f"\nLogger API failed: {exc}")
        return None


@test_case_agent.post("/test_case")
async def testCase_api(request: requestbody):
    start_time = time.time()
    correlation_id = str(uuid4())

    try:
        safe_logger(
            agent_name="TestCaseAgent",
            message="Test case generation request received",
            event_type="TestCaseGenerationStarted",
            source_module="TestCaseAgent.API.Routes",
            is_success=True,
            correlation_id=correlation_id,
            payload={
                "endpoint": "/test_case",
                "user_story_length": len(request.user_story or ""),
                "task_length": len(request.task or ""),
            },
        )

        response = await test_case(
            user_story=request.user_story,
            task=request.task,
        )

        duration_ms = int((time.time() - start_time) * 1000)

        safe_logger(
            agent_name="TestCaseAgent",
            message="Test case generation completed successfully",
            event_type="TestCaseGenerationCompleted",
            source_module="TestCaseAgent.API.Routes",
            is_success=True,
            duration_ms=duration_ms,
            correlation_id=correlation_id,
            payload={
                "endpoint": "/test_case",
                "response_keys": list(response.keys()) if isinstance(response, dict) else [],
            },
        )

        return response

    except Exception as exc:
        duration_ms = int((time.time() - start_time) * 1000)
        traceback.print_exc()

        safe_logger(
            agent_name="TestCaseAgent",
            message=f"Test case generation failed: {str(exc)}",
            event_type="TestCaseGenerationError",
            source_module="TestCaseAgent.API.Routes",
            is_success=False,
            duration_ms=duration_ms,
            correlation_id=correlation_id,
            payload={
                "endpoint": "/test_case",
                "error": str(exc),
                "stack_trace": traceback.format_exc(),
            },
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc

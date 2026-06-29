import shutil
import time
import traceback
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel

from app.artifact_agent.app.src.agents.yml_agent import yml_code_gen
from app.artifact_agent.app.src.agents.openapi_gen import openapi_code_gen
from app.utils.logger import AgentLogger
from pydantic import BaseModel, Field, ConfigDict

router = APIRouter(tags=["code_generator"])
logger = AgentLogger()


BASE_DIR = Path(__file__).resolve().parents[2]

YML_DIR = BASE_DIR / "document" / "yml"
YML_FILE = YML_DIR / "openapi.yml"

UPLOAD_DIR = BASE_DIR / "uploads"

class CodeGenRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    task: str
    techstack: str
    UserStoryTaskId: str = Field(alias="SubTaskId")
    instructions: str | None = Field(default=None, alias="Instructions")


def safe_logger(**kwargs):
    try:
        return logger.log_event(**kwargs)
    except Exception as exc:
        print(f"\nLogger API failed: {exc}")
        return None


@router.post("/generate-full-api")
async def generate_full_api(request: CodeGenRequest):
    start_time = time.time()
    correlation_id = str(uuid4())

    try:
        safe_logger(
            agent_name="ArtifactCodeGeneratorAgent",
            message="Full API generation request received",
            event_type="FullApiGenerationStarted",
            source_module="ArtifactAgent.API.Routes",
            is_success=True,
            correlation_id=correlation_id,
            payload={
                "endpoint": "/generate-full-api",
                "task": request.task,
                "techstack": request.techstack,
                "UserStoryTaskId": request.UserStoryTaskId,
                "has_instructions": bool(request.instructions),
            },
        )

        yml_response = await yml_code_gen(
            task=request.task,
            techstack=request.techstack,
            user_story_task_id=request.UserStoryTaskId,
            instructions=request.instructions
        )

        safe_logger(
            agent_name="ArtifactCodeGeneratorAgent",
            message="OpenAPI YAML generated successfully",
            event_type="YamlGenerationCompleted",
            source_module="ArtifactAgent.API.Routes",
            is_success=True,
            duration_ms=int((time.time() - start_time) * 1000),
            correlation_id=correlation_id,
            payload={
                "endpoint": "/generate-full-api",
                "yaml_file": str(YML_FILE),
                "UserStoryTaskId": request.UserStoryTaskId,
                "yaml_keys": list(yml_response.keys()) if isinstance(yml_response, dict) else [],
            },
        )

        if not YML_FILE.exists():
            raise FileNotFoundError(
                f"Agent 1 did not create YAML file at: {YML_FILE}"
            )

        generated_code = await openapi_code_gen(
            user_story_task_id=request.UserStoryTaskId
        )

        duration_ms = int((time.time() - start_time) * 1000)

        safe_logger(
            agent_name="ArtifactCodeGeneratorAgent",
            message="Full API generation completed successfully",
            event_type="FullApiGenerationCompleted",
            source_module="ArtifactAgent.API.Routes",
            is_success=True,
            duration_ms=duration_ms,
            correlation_id=correlation_id,
            payload={
                "endpoint": "/generate-full-api",
                "yaml_file": generated_code.get("yaml_file"),
                "UserStoryTaskId": request.UserStoryTaskId,
                "generated_dir": generated_code.get("generated_dir"),
                "generated_file_count": len(generated_code.get("saved_files") or []),
                "zip_file": generated_code.get("zip_file"),
                "backend": generated_code.get("backend"),
                "generator": generated_code.get("generator"),
            },
        )

        return {
            "status": "success",
            "message": "Agent 1 generated YAML, then Agent 2 generated source code from that YAML.",
            "UserStoryTaskId": request.UserStoryTaskId,
            "yaml_used_by_agent_2": generated_code.get("yaml_file"),
            "code_saved_at": generated_code.get("generated_dir"),
            "generated_files": generated_code.get("saved_files"),
            "zip_file": generated_code.get("zip_file"),
            "backend": generated_code.get("backend"),
            "generator": generated_code.get("generator")
        }
    except Exception as exc:
        duration_ms = int((time.time() - start_time) * 1000)
        traceback.print_exc()

        safe_logger(
            agent_name="ArtifactCodeGeneratorAgent",
            message=f"Full API generation failed: {str(exc)}",
            event_type="FullApiGenerationError",
            source_module="ArtifactAgent.API.Routes",
            is_success=False,
            duration_ms=duration_ms,
            correlation_id=correlation_id,
            payload={
                "endpoint": "/generate-full-api",
                "task": request.task,
                "techstack": request.techstack,
                "UserStoryTaskId": request.UserStoryTaskId,
                "error": str(exc),
                "stack_trace": traceback.format_exc(),
            },
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc


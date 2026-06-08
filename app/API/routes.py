from pydantic import BaseModel
from fastapi import APIRouter
from uuid import uuid4
from pathlib import Path
import json
import re
import socket
import threading
import time
import traceback

from datetime import datetime, timezone

from app.graph.workflow import create_graph
from app.graph.nodes.node import chat_test_case_llm
from app.utils.logger import logger

router = APIRouter()
graph_app = create_graph()

LOGGER_API = "https://vibeappop.saa.ai/EnterpriseLogging/api/Logs"
BASE_DIR = Path(__file__).resolve().parents[2]
GENERATED_MD_DIR = BASE_DIR / "generated_md"


def read_generated_markdown(filename):
    path = GENERATED_MD_DIR / filename

    if not path.exists():
        return ""

    return path.read_text(encoding="utf-8")


def clean_markdown_value(value):
    return re.sub(r"^\*+|\*+$", "", value.strip()).strip()


def parse_markdown_list(text):
    items = []

    for line in text.splitlines():
        line = line.strip()

        if not line or line == "---":
            continue

        match = re.match(r"^(?:[-*]|\d+\.)\s*(.*)", line)

        if match:
            items.append(clean_markdown_value(match.group(1)))

    return items


def parse_label_value(block, label):
    pattern = rf"\*?\*?{re.escape(label)}\*?\*?:\s*(.*)"
    match = re.search(pattern, block, re.I)
    return clean_markdown_value(match.group(1)) if match else ""


def parse_story_list_section(block, heading):
    pattern = (
        rf"\*?\*?{re.escape(heading)}\*?\*?:\s*"
        rf"(.*?)(?=\n\*?\*?[A-Z][A-Za-z ]+\*?\*?:|\n#|\Z)"
    )
    match = re.search(pattern, block, re.S)
    return parse_markdown_list(match.group(1)) if match else []


def parse_story_text_section(block, heading):
    pattern = (
        rf"\*?\*?{re.escape(heading)}\*?\*?:\s*"
        rf"(.*?)(?=\n\*?\*?(?:Acceptance Criteria|User Story ID|Title|Description)\*?\*?:|\n#|\Z)"
    )
    match = re.search(pattern, block, re.S | re.I)
    return clean_markdown_value(match.group(1)) if match else ""


def parse_user_story(text):
    if not text:
        return {
            "is_valid": True,
            "user_input": "",
            "user_stories": [],
        }

    if "# Invalid Feature Request" in text:
        return {
            "is_valid": False,
            "message": clean_markdown_value(
                text.replace("# Invalid Feature Request", "")
            ),
            "user_stories": [],
        }

    def section(name):
        pattern = rf"# {re.escape(name)}\s*(.*?)(?=\n# |\Z)"
        match = re.search(pattern, text, re.S)
        return match.group(1).strip() if match else ""

    stories_section = section("User Story") or section("User Stories")
    story_blocks = [
        block.strip()
        for block in re.split(r"\n---+\n|(?=User Story ID:)", stories_section)
        if "User Story ID:" in block
    ]

    user_stories = []

    for block in story_blocks:
        user_stories.append({
            "user_story_id": parse_label_value(block, "User Story ID"),
            "title": parse_label_value(block, "Title"),
            "description": parse_story_text_section(block, "Description"),
            "acceptance_criteria": parse_story_list_section(block, "Acceptance Criteria"),
        })

    return {
        "is_valid": True,
        "user_input": clean_markdown_value(section("User Input")),
        "user_stories": user_stories,
    }


def parse_tasks(text):
    tasks = []

    blocks = re.split(r"(?=TASK ID:)", text)

    for block in blocks:
        if "TASK ID:" not in block:
            continue

        def extract(pattern):
            match = re.search(pattern, block)
            return match.group(1).strip() if match else ""

        task = {
            "task_id": extract(r"TASK ID:\s*(.*)"),
            "priority": extract(r"Priority:\s*(.*)"),
            "task_name": extract(r"Task Name:\s*(.*)"),
            "task_description": extract(r"Task Description:\s*(.*)"),
        }

        # ============================
        # POINTS TO DO
        # ============================
        points = re.search(
            r"Points To Do:\s*(.*?)(?=Acceptance Criteria:|TASK ID:|$)",
            block,
            re.S
        )

        task["points_to_do"] = (
            [p.strip("- ").strip() for p in points.group(1).split("\n") if p.strip()]
            if points and points.group(1).strip()
            else []
        )

        # ============================
        # ACCEPTANCE CRITERIA
        # ============================
        ac = re.search(
            r"Acceptance Criteria:\s*(.*?)(?=Time Period:|Assigned Resource:|TASK ID:|$)",
            block,
            re.S
        )

        task["acceptance_criteria"] = (
            [a.strip("- ").strip() for a in ac.group(1).split("\n") if a.strip()]
            if ac and ac.group(1).strip()
            else []
        )

        # ============================
        # TIME PERIOD
        # ============================
        tp = re.search(r"Time Period:\s*(.*)", block)
        task["time_period"] = tp.group(1).strip() if tp else ""

        # ============================
        # ASSIGNED RESOURCE
        # ============================
        ar = re.search(r"Assigned Resource:\s*(.*)", block)
        task["assigned_resource"] = ar.group(1).strip() if ar else ""

        tasks.append(task)

    return {"tasks": tasks}


def normalize_strict_response(payload):
    if not isinstance(payload, dict):
        return []

    user_stories = []

    for story in payload.get("user_stories", []):
        if not isinstance(story, dict):
            continue

        tasks = []
        story_id = story.get("user_story_id", "")

        for index, task in enumerate(story.get("tasks", []), start=1):
            if not isinstance(task, dict):
                continue

            points_to_do = task.get("points_to_do", [])
            if not isinstance(points_to_do, list):
                points_to_do = []

            acceptance_criteria = task.get("acceptance_criteria", [])
            if not isinstance(acceptance_criteria, list):
                acceptance_criteria = []

            tasks.append({
                "task_id": task.get("task_id", f"{story_id}-T{index:02d}" if story_id else ""),
                "title": task.get("title", task.get("task_name", "")),
                "task_description": task.get("task_description", ""),
                "points_to_do": points_to_do,
                "acceptance_criteria": acceptance_criteria,
            })

        story_acceptance_criteria = story.get("acceptance_criteria", [])
        if not isinstance(story_acceptance_criteria, list):
            story_acceptance_criteria = []

        user_stories.append({
            "user_story_id": story_id,
            "title": story.get("title", ""),
            "description": story.get("description", ""),
            "acceptance_criteria": story_acceptance_criteria,
            "tasks": tasks,
            "time_period": story.get("time_period", ""),
        })

    return user_stories


def parse_json_task_response(text):
    if not text:
        return []

    cleaned_text = text.strip()

    if cleaned_text.startswith("```"):
        cleaned_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned_text, flags=re.S)

    try:
        payload = json.loads(cleaned_text)
    except json.JSONDecodeError:
        return []

    return normalize_strict_response(payload)


def parse_json_response(text):
    if not text:
        return None

    cleaned_text = text.strip()

    if cleaned_text.startswith("```"):
        cleaned_text = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned_text, flags=re.S)

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        return None


def build_strict_response(user_story_text, task_text):
    json_user_stories = parse_json_task_response(task_text)

    if json_user_stories:
        return json_user_stories

    parsed_user_story = parse_user_story(user_story_text)
    user_stories = parsed_user_story.get("user_stories", [])
    parsed_tasks = parse_tasks(task_text).get("tasks", [])

    if not user_stories:
        return []

    response = []
    for index, story in enumerate(user_stories):
        task = parsed_tasks[index] if index < len(parsed_tasks) else {}

        response.append({
            "user_story_id": story.get("user_story_id", ""),
            "title": story.get("title", ""),
            "description": story.get("description", ""),
            "acceptance_criteria": story.get("acceptance_criteria", []),
            "tasks": [
                {
                    "task_id": f"{story.get('user_story_id', '')}-T01" if story.get("user_story_id", "") else "",
                    "title": task.get("task_name", ""),
                    "task_description": task.get("task_description", ""),
                    "points_to_do": task.get("points_to_do", []),
                    "acceptance_criteria": task.get("acceptance_criteria", []),
                }
            ] if task else [],
            "time_period": task.get("time_period", ""),
        })

    return response



def safe_logger(**kwargs):

    try:
        return logger(**kwargs)
    except Exception as exc:
        print(f"\nLogger API failed: {exc}")
        return None


class ChatRequest(BaseModel):
    user_input: str

@router.post("/ask")
async def ask_question(data: ChatRequest):

    start_time = time.time()


    session_id = str(uuid4())
    correlation_id = str(uuid4())
    request_id = str(uuid4())
    log_id = str(uuid4())
    graph_thread_id = f"user-session-{uuid4()}"
    

    try:
        safe_logger(
            api_url=LOGGER_API,

            logId=log_id,

            timestampUtc=datetime.now(
                timezone.utc
            ).isoformat(),

            logLevel=2,

            message="User request received",

            eventType="UserPromptReceived",

            sourceApplication="User_Story_gen",

            sourceModule="API.Routes",

            environment="Development",

            userId="",

            sessionId=session_id,

            correlationId=correlation_id,

            requestId=request_id,

            machineName=socket.gethostname(),

            threadId=str(threading.get_ident()),

            exceptionMessage=None,

            stackTrace=None,

            metadata={
                "workflow": "spec-kit",
                "endpoint": "/ask"
            },

            durationMs=int((time.time() - start_time) * 1000),

            isSuccess=True,

            payloadJson=json.dumps({
                "user_input": data.user_input
            })
        )

        # Initial graph state
        initial_state = {
            "user_input": data.user_input,
            "retrieved_context": "",
            "constitution": "",
            "specification":"" ,
            # "planning": "",
            "task": "",
            "user_story": "",
            # "test_case": "",
        }

        config = {
            "configurable": {
                "thread_id": graph_thread_id
            }
        }

        # Run workflow graph
        result = await graph_app.ainvoke(
            initial_state,
            config=config
        )

        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        safe_logger(
            api_url=LOGGER_API,

            logId=log_id,

            timestampUtc=datetime.now(
                timezone.utc
            ).isoformat(),

            logLevel=2,

            message="Workflow completed successfully",

            eventType="WorkflowCompleted",

            sourceApplication="Spec-Kit-AI",

            sourceModule="API.Routes",

            environment="Development",

            userId="",

            sessionId=session_id,

            correlationId=correlation_id,

            requestId=request_id,

            machineName=socket.gethostname(),

            threadId=str(threading.get_ident()),

            exceptionMessage=None,

            stackTrace=None,

            metadata={
                "durationMs": duration_ms,
                "endpoint": "/ask"
            },

            durationMs=duration_ms,

            isSuccess=True,

            payloadJson=json.dumps(result)
        )

        # Return JSON response
        return {
            "success": True,
            "user_stories": build_strict_response(
                result.get("user_story", ""),
                result.get("task", "")
            ),
        }

    except Exception as e:
        duration_ms = int(
            (time.time() - start_time) * 1000
        )

        safe_logger(
            api_url=LOGGER_API,

            logId=log_id,

            timestampUtc=datetime.now(
                timezone.utc
            ).isoformat(),

            logLevel=4,

            message="Workflow execution failed",

            eventType="WorkflowError",

            sourceApplication="Spec-Kit-AI",

            sourceModule="API.Routes",

            environment="Development",

            userId="",

            sessionId=session_id,

            correlationId=correlation_id,

            requestId=request_id,

            machineName=socket.gethostname(),

            threadId=str(threading.get_ident()),

            exceptionMessage=str(e),

            stackTrace=traceback.format_exc(),

            metadata={
                "durationMs": duration_ms,
                "endpoint": "/ask"
            },

            durationMs=duration_ms,

            isSuccess=False,

            payloadJson=json.dumps({
                "user_input": data.user_input
            })
        )

        return {
            "success": False,
            "error": str(e)
        }





# ###Test case endpoint
# class TestCaseRequest(BaseModel):
#     constitution: str = ""
#     user_story: str
#     task: str


# @router.post("/test")
# async def generate_test_case(request: TestCaseRequest):

#     result = await chat_test_case_llm(
#         user_story=request.user_story,
#         task=request.task,
#     )

#     try:
#         return {
#             "success": True,
#             "constitution": request.constitution,
#             "test_case": json.loads(result.get("test_case", "{}")),
#         }

#     except json.JSONDecodeError:
#         return {
#             "success": False,
#             "error": "Generated test case response is not valid JSON.",
#             "test_case": result.get("test_case", ""),
#         }

from pydantic import BaseModel
from fastapi import APIRouter
from uuid import uuid4
import json
import re
import socket
import threading
import time
import traceback

from datetime import datetime, timezone

from app.graph.workflow import create_graph
from app.utils.logger import logger

router = APIRouter()
graph_app = create_graph()

LOGGER_API = "https://vibeappop.saa.ai/EnterpriseLogging/api/Logs"


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



def safe_logger(**kwargs):

    try:
        return logger(**kwargs)
    except Exception as exc:
        print(f"\nLogger API failed: {exc}")
        return None


class ChatRequest(BaseModel):
    question: str

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
                "user_input": data.question
            })
        )

        # Initial graph state
        initial_state = {
            "user_input": data.question,
            "retrieved_context": "",
            "constitution": "",
            # "specification": "",
            # "planning": "",
            "task": "",
            "user_story": ""
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
            "input": data.question,
            # "constitution": result.get("constitution", ""),
            # "specification": result.get("specification", ""),
            # "planning": result.get("planning", ""),
            # "task": result.get("task", ""),
            "user_story": parse_user_story(result.get("user_story", "")),
            "task": parse_tasks(result.get("task", "")),
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
                "user_input": data.question
            })
        )

        return {
            "success": False,
            "error": str(e)
        }


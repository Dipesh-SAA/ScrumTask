from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os

mongo_uri = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI") or "mongodb://localhost:27017/"
client = AsyncIOMotorClient(
    mongo_uri,
    serverSelectionTimeoutMS=int(os.getenv("MONGODB_SERVER_SELECTION_TIMEOUT_MS", "2000")),
)
db = client[os.getenv("MONGO_DB_NAME") or "ScrumAgentsActivity"]

collection = db["AgentsActivity"]


async def _insert_log(document: dict):
    try:
        await collection.insert_one(document)
    except Exception as exc:
        print(f"[log_agent] MongoDB logging skipped: {exc}")

def with_logging(stage, func):
    async def wrapper(state):
        user_story_id = state.get("user_story_id", state.get("UserStoryId", ""))

        await _insert_log({
            "UserStoryTaskId": user_story_id,
            "Stage": stage,
            "AgentName": stage,
            "Message": f"{stage} Started",
            "Status": "Running",
            "CreatedAt": datetime.utcnow(),
            "UpdatedAt": datetime.utcnow(),
        })

        try:
            result = await func(state)

            await _insert_log({
                "UserStoryTaskId": user_story_id,
                "Stage": stage,
                "AgentName": stage,
                "Message": f"{stage} Completed",
                "Status": "Completed",
                "CreatedAt": datetime.utcnow(),
                "UpdatedAt": datetime.utcnow(),
            })

            return result

        except Exception as e:

            await _insert_log({
                "UserStoryTaskId": user_story_id,
                "Stage": stage,
                "AgentName": stage,
                "Message": str(e),
                "Status": "Failed",
                "CreatedAt": datetime.utcnow(),
                "UpdatedAt": datetime.utcnow(),
            })

            raise

    return wrapper

#####################################################################################################################################################
async def log_agent(
    user_story_task_id: str,
    stage: str,
    message: str,
    status: str,
    agent_name: str = "System",
):
    now = datetime.utcnow()

    await _insert_log(
        {
            "UserStoryTaskId": user_story_task_id,
            "Stage": stage,
            "AgentName": agent_name,
            "Message": message,
            "Status": status,
            "CreatedAt": now,
            "UpdatedAt": now,
        }
    )

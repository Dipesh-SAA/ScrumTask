from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os

client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client["ScrumAgentsActivity"]

collection = db["AgentsActivity"]

def with_logging(stage, func):
    async def wrapper(state):
        user_story_id = state.get("user_story_id", state.get("UserStoryId", ""))

        await collection.insert_one({
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

            await collection.insert_one({
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

            await collection.insert_one({
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

    await collection.insert_one(
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

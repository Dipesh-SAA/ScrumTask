from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.test_case_agent.src.agent import test_case

test_case_agent = APIRouter(tags=["test_case"])


class requestbody(BaseModel):
    user_story: str
    task: str


@test_case_agent.post("/test_case")
async def testCase_api(request:requestbody):

    try:

        response = await test_case(
            user_story=request.user_story,
            task=request.task
        )

        return response

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc)
        ) from exc

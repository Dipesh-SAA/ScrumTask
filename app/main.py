import asyncio
from uuid import uuid4
from app.test_case_agent.src.router import test_case_agent
from app.graph.workflow import create_graph
from fastapi import FastAPI
from app.api.routes import router
from app.Infrastrature.embeddings.embedding_model import (generate_embedding,get_constitution_chunks, rank_chunks)
import json
import socket
import threading
import time
import traceback
from app.artifact_agent.app.src.api.routes.router import router as artifact_router
from datetime import datetime, timezone
# from app.utils.logger import logger


api = FastAPI(root_path="/scrumTask")
api.include_router(router)
api.include_router(test_case_agent)
api.include_router(artifact_router)



# LOGGER_API = "https://vibeappop.saa.ai/EnterpriseLogging/api/Logs"



# #safe logger wrapper to prevent logging failures from impacting main workflow
# def safe_logger(**kwargs):

#     try:
#         return logger(**kwargs)
#     except Exception as exc:
#         print(f"\nLogger API failed: {exc}")
#         return None
    


# async def chat():

#     # Create graph app
#     app = create_graph()

#     print("\n====================================")
#     print("        SPEC KIT AI AGENT")
#     print("====================================")

#     print("\nType 'exit' to quit.\n")

#     while True:

#         # User input
#         user_input = input("\nYou: ")

#         # Exit condition
#         if user_input.lower() in ["exit", "quit"]:
#             print("\nGoodbye 👋")
#             break

#         try:
#             start_time = time.time()

#             session_id = str(uuid4())
#             correlation_id = str(uuid4())
#             request_id = str(uuid4())
#             log_id=str((uuid4()))

#             safe_logger(
#                 api_url=LOGGER_API,

#                 logId=log_id,

#                 timestampUtc=datetime.now(
#                     timezone.utc
#                 ).isoformat(),

#                 logLevel=2,

#                 message="User request received",

#                 eventType="UserPromptReceived",

#                 sourceApplication="User_Story_gen",

#                 sourceModule="Main",

#                 environment="Development",

#                 userId="",

#                 sessionId=session_id,

#                 correlationId=correlation_id,

#                 requestId=request_id,

#                 machineName=socket.gethostname(),

#                 threadId=str(threading.get_ident()),

#                 exceptionMessage=None,

#                 stackTrace=None,

#                 metadata={
#                     "workflow": "spec-kit"
#                 },

#                 durationMs=int((time.time() - start_time) * 1000),

#                 isSuccess=True,

#                 payloadJson=json.dumps({
#                     "user_input": user_input
                    
#                 })
#             )

#             # -----------------------------------
#             # STEP 1: Generate user embedding
#             # -----------------------------------
#             user_vector = generate_embedding(user_input)

#             # -----------------------------------
#             # STEP 2: Fetch constitution chunks
#             # -----------------------------------
#             chunks = get_constitution_chunks()

#             # -----------------------------------
#             # STEP 3: Rank chunks
#             # -----------------------------------
#             ranked_chunks = rank_chunks(
#                 user_vector=user_vector,
#                 chunks=chunks,
#                 top_k=5
#             )

#             # -----------------------------------
#             # STEP 4: Create retrieved context
#             # -----------------------------------
#             retrieved_context = "\n\n".join([
#                 f"""
# Heading: {chunk['heading']}

# Text:
# {chunk['text']}
# """
#                 for chunk in ranked_chunks
#             ])

#             # -----------------------------------
#             # STEP 5: Initial state
#             # -----------------------------------
#             initial_state = {
#                 "user_input": user_input,
#                 "retrieved_context": retrieved_context,
#                 "constitution": "",
#                 "specification": "",
#                 # "planning": "",
#                 "task": "",
#                 "user_story": ""
#             }

#             config = {
#                 "configurable": {
#                     "thread_id": f"user-session-{uuid4()}"
#                 }
#             }

#             # -----------------------------------
#             # STEP 6: Run graph
#             # -----------------------------------
#             result = await app.ainvoke(
#                 initial_state,
#                 config=config
#             )

#             duration_ms = int(
#                 (time.time() - start_time) * 1000
#             )

#             safe_logger(
#                 api_url=LOGGER_API,

#                 logId=log_id,

#                 timestampUtc=datetime.now(
#                     timezone.utc
#                 ).isoformat(),

#                 logLevel=2,

#                 message="Workflow completed successfully",

#                 eventType="WorkflowCompleted",

#                 sourceApplication="Spec-Kit-AI",

#                 sourceModule="Workflow",

#                 environment="Development",

#                 userId="",

#                 sessionId=session_id,

#                 correlationId=correlation_id,

#                 requestId=request_id,

#                 machineName=socket.gethostname(),

#                 threadId=str(threading.get_ident()),

#                 exceptionMessage=None,

#                 stackTrace=None,

#                 metadata={
#                     "durationMs": duration_ms
#                 },

#                 durationMs=duration_ms,

#                 isSuccess=True,

#                 payloadJson=json.dumps(result)
#             )

#             print("\n====================================")
#             print("RETRIEVED CONTEXT")
#             print("====================================")
#             print(retrieved_context)

#             print("\n====================================")
#             print("CONSTITUTION")
#             print("====================================")
#             print(result.get("constitution", ""))

#             print("\n====================================")
#             print("SPECIFICATION")
#             print("====================================")
#             print(result.get("specification", ""))

#             print("\n====================================")
#             print("USER STORY")
#             print("====================================")
#             print(result.get("user_story", ""))

#         except Exception as e:

#             duration_ms = int(
#                 (time.time() - start_time) * 1000
#             )

#             safe_logger(
#                 api_url=LOGGER_API,

#                 logId=log_id,

#                 timestampUtc=datetime.now(
#                     timezone.utc
#                 ).isoformat(),

#                 logLevel=4,

#                 message="Workflow execution failed",

#                 eventType="WorkflowError",

#                 sourceApplication="Spec-Kit-AI",

#                 sourceModule="Workflow",

#                 environment="Development",

#                 userId="",

#                 sessionId=session_id,

#                 correlationId=correlation_id,

#                 requestId=request_id,

#                 machineName=socket.gethostname(),

#                 threadId=str(threading.get_ident()),

#                 exceptionMessage=str(e),

#                 stackTrace=traceback.format_exc(),

#                 metadata={
#                     "durationMs": duration_ms
#                 },

#                 durationMs=duration_ms,

#                 isSuccess=False,

#                 payloadJson=json.dumps({
#                     "user_input": user_input
#                 })
#             )

#             print("\nERROR:")
#             print(str(e))












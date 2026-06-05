import os
from dotenv import load_dotenv
from mistralai.client import Mistral
from datetime import datetime
import json

# ==========================
# ENV
# ==========================
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env file")

client = Mistral(api_key=api_key)
model = "mistral-large-latest"

# ==========================
# UTIL: SAFE JSON PARSER
# ==========================
def safe_parse_json(text):
    try:
        return json.loads(text), True
    except:
        return None, False

# ==========================
# UTIL: CLEAN OUTPUT
# ==========================
def clean_output(text):
    text = text.strip()
    text = text.replace("```json", "").replace("```", "")
    return text.strip()

# ==========================
# LOAD FILES
# ==========================
start_time = datetime.now()

with open("../user_story.md", "r", encoding="utf-8") as f:
    user_story = f.read()
with open("../constitution.md", "r", encoding="utf-8") as f:
    constitution = f.read()
with open("../specification.md", "r", encoding="utf-8") as f:
    specification = f.read()

# ==========================
# PROMPT
# ==========================
prompt = f"""
You are a Senior QA Engineer.

Generate high-quality test cases.

RULES:
- Return ONLY valid JSON
- No markdown
- No explanation

CONSTITUTION:
{constitution}

USER STORY:
{user_story}

SPCEFICIFATION:
{specification}

STRICT TRACEABILITY RULES

- Every test case must be directly traceable to a User Story or Acceptance Criterion.
- Do NOT invent:
  - thresholds
  - limits
  - sizes
  - retry counts
  - timeout values
  - file sizes
  - token expiry values
  - encryption algorithms
  - authentication mechanisms
  - technologies
  - tools
  - platforms

unless explicitly stated.

If a value is not provided in the User Story, use generic wording.

Bad:
"Verify rate limiting after 5 attempts"

Good:
"Verify rate limiting behavior"

Bad:
"Verify password hashing using bcrypt"

Good:
"Verify password is stored securely"

Bad:
"Verify ingestion of 1GB files"

Good:
"Verify ingestion of large files"

FORMAT:
{{
  "tickets": [
    {{
      "ticket_id": "",
      "title": "",
      "test_cases": [
        {{
          "test_case_id": "",
          "title": "",
          "category": "",
          "priority": "",
          "preconditions": "",
          "expected_result": ""
        }}
      ]
    }}
  ]
}}
"""

# ==========================
# ARTIFACT FOLDER
# ==========================
run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
base_folder = f"artifacts/{run_id}"
os.makedirs(base_folder, exist_ok=True)

# ==========================
# SAVE INPUTS
# ==========================
with open(f"{base_folder}/user_story.txt", "w", encoding="utf-8") as f:
    f.write(user_story)

with open(f"{base_folder}/constitution.txt", "w", encoding="utf-8") as f:
    f.write(constitution)

with open(f"{base_folder}/prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

# ==========================
# CALL LLM
# ==========================
status = "failed"
llm_output = ""
parsed_json = None
json_valid = False

try:
    response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    llm_output = response.choices[0].message.content
    cleaned = clean_output(llm_output)

    parsed_json, json_valid = safe_parse_json(cleaned)

    # ==========================
    # SAVE RAW OUTPUT
    # ==========================
    with open(f"{base_folder}/llm_output.txt", "w", encoding="utf-8") as f:
        f.write(llm_output)

    # ==========================
    # SAVE RESULT (SAFE)
    # ==========================
    if json_valid:
        with open(f"{base_folder}/result.json", "w", encoding="utf-8") as f:
            json.dump(parsed_json, f, indent=4)
        status = "success"
    else:
        # fallback: store raw as text JSON file
        with open(f"{base_folder}/result.json", "w", encoding="utf-8") as f:
            f.write(cleaned)

    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    meta = {
        "run_id": run_id,
        "model": model,
        "start_time": str(start_time),
        "end_time": str(end_time),
        "duration_seconds": duration,
        "status": status,
        "json_valid": json_valid,
        "output_length": len(llm_output)
    }

except Exception as e:
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    meta = {
        "run_id": run_id,
        "model": model,
        "start_time": str(start_time),
        "end_time": str(end_time),
        "duration_seconds": duration,
        "status": "failed",
        "error": str(e)
    }

# ==========================
# SAVE META
# ==========================
with open(f"{base_folder}/meta.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=4)

# ==========================
# LOG
# ==========================
print(f"\n✅ Run completed")
print(f"Status: {status}")
print(f"JSON valid: {json_valid}")
print(f"Duration: {duration}s")
print(f"Saved: {base_folder}")
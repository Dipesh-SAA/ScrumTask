from langchain_core.prompts import ChatPromptTemplate


TEST_CASE_GENERATOR_PROMPT = ChatPromptTemplate.from_template("""
You are a Senior QA Engineer.

Generate high-quality test cases.

RULES:
- Return ONLY valid JSON
- No markdown
- No explanation



USER STORY:
{user_story}

SUB_TASK:
{task}                                                          

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
""")

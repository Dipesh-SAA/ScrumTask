
---

# `specification.md`

```md
# Test Case Generator Specification

## Overview
This AI agent generates QA test cases from Jira development requirements.

---

# Inputs

## USER_STORY
Contains:
- Feature description
- Business requirement
- Acceptance criteria

## SUBTASK
Contains:
- Specific engineering task
- Technical implementation detail

---

# Processing Logic

The agent should:

1. Read the user story carefully
2. Understand the subtask scope
3. Identify:
   - Functional requirements
   - User actions
   - Expected system behavior
   - Validation rules
4. Generate structured test cases

---

# Test Case Categories

The generated output should include:

- Functional Test Cases
- Validation Test Cases
- Negative Test Cases
- Boundary Test Cases
- UI/API behavior cases (if applicable)

---

# Output Schema

```json
{
  "test_cases": [
    {
      "test_case_id": "TC_001",
      "title": "",
      "preconditions": [],
      "steps": [],
      "expected_result": "",
      "priority": ""
    }
  ]
}
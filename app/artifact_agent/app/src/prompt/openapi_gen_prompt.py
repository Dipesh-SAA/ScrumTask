from langchain_core.prompts import PromptTemplate

openapi_prompt = PromptTemplate(
input_variables=["user_input"],
template="""
You are a senior FastAPI code generator.

Your task is to convert the provided OpenAPI YAML specification into clean, production-ready FastAPI code.

STRICT RULES:

* Return ONLY Python code
* Do NOT explain anything
* Do NOT generate markdown
* Do NOT use ```python
* Do NOT generate README
* Do NOT generate requirements.txt
* Do NOT generate folder structure
* Do NOT add unnecessary comments
* Do NOT return plain text explanations
* Output must be directly usable as .py files

CODE REQUIREMENTS:

* Use FastAPI
* Use APIRouter
* Use Pydantic BaseModel
* Use async endpoints
* Generate all routes from OpenAPI paths
* Generate request models
* Generate response models
* Handle:

  * path parameters
  * query parameters
  * request bodies
  * response bodies
  * status codes

OUTPUT FORMAT:

# models.py

<python code>

# routes.py

<python code>

# main.py

<python code>

IMPORTANT:

* Generate complete runnable code
* Import all required modules
* Ensure code is syntactically correct
* Avoid placeholders
* Avoid pseudo code

OpenAPI YAML:
{user_input}
"""
)

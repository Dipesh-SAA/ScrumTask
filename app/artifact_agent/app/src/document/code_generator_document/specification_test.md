# Backend Code Generator Specification

Read the provided OpenAPI YAML and generate source code strictly according to the value of `x-backend`.

## Backend Selection

Generate code only for:

```yaml
x-backend: <backend>
```

Generate code exclusively for the specified backend.

---

## OpenAPI Compliance

Generate code strictly from the OpenAPI YAML.

Implement:

* Paths and HTTP methods
* Parameters
* Request and response models
* Validation rules
* Security schemes
* Authentication and authorization
* Status codes

Do not invent:

* Endpoints
* Fields
* Models
* Business logic
* Security rules

Generate only what is explicitly defined in the YAML.

---

## Project Generation Rules

Generate a complete, runnable, and production-ready project.

Requirements:

* Generate compilable code
* Include all required files and dependencies
* Use logging and error handling
* Use environment-based configuration
* Use async APIs where supported
* Avoid hardcoded secrets
* Generate complete implementations

Do not generate:

```text
TODO
FIXME
pass
NotImplementedException
your code here
bin/
obj/
.vs/
node_modules/
__pycache__/
target/
```

---

## Output Contract

Return ONLY valid JSON:

```json
{
  "backend": "<backend>",
  "files": {
    "<relative_path>": {
      "language": "<language>",
      "content": "<file_content>"
    }
  }
}
```

Rules:

* `backend` is required
* `files` is required
* Every file must contain:

  * `language`
  * `content`
* File content must not be empty
* Return no markdown, explanations, or code fences

---

## File Path Rules

All file paths are relative to:

```text
generated_outputs/<backend>/<api_folder>/
```

Rules:

* Use forward slashes (`/`)
* Do not generate absolute paths
* Do not use `..`
* Do not prepend project names
* Do not create additional root folders

Invalid examples:

```text
StudentApi/Program.cs
src/StudentApi/Controllers/UserController.cs
C:/project/Program.cs
../Controllers/UserController.cs
```

---

# ASP.NET Core Requirements

Generate a production-ready ASP.NET Core Web API.

## Allowed Root Files

```text
Program.cs
appsettings.json
<ProjectName>.csproj
```

## Required Folder Structure

```text
Properties/launchSettings.json
Controllers/*Controller.cs
Models/Requests/*Request.cs
Models/Responses/*Response.cs
Models/Responses/ErrorResponse.cs
Services/Interfaces/I*Service.cs
Services/Implementations/*Service.cs
Repositories/Interfaces/I*Repository.cs
Repositories/Implementations/*Repository.cs
Middleware/*.cs
Extensions/*.cs
Configuration/*.cs
DTOs/*.cs
```

## Mandatory Files

```text
Program.cs
appsettings.json
Properties/launchSettings.json
Models/Responses/ErrorResponse.cs
```

## Path Validation Rules

Controllers must start with:

```text
Controllers/
```

Requests must start with:

```text
Models/Requests/
```

Responses must start with:

```text
Models/Responses/
```

Service interfaces must start with:

```text
Services/Interfaces/
```

Service implementations must start with:

```text
Services/Implementations/
```

Repository interfaces must start with:

```text
Repositories/Interfaces/
```

Repository implementations must start with:

```text
Repositories/Implementations/
```

Launch settings must be:

```text
Properties/launchSettings.json
```

## Forbidden Paths

These paths are invalid:

```text
launchSettings.json
UserController.cs
Requests/UserRequest.cs
Responses/UserResponse.cs
Interfaces/IUserService.cs
Implementations/UserService.cs
```

If any invalid path is generated:

* Correct the path before returning JSON
* Never return invalid paths

## ASP.NET Core Coding Standards

* Use dependency injection
* Use `ILogger<T>`
* Use async/await
* Use model validation attributes
* Return `ActionResult<T>` or `IActionResult`
* Do not generate `.sln`, `bin`, or `obj`

---

# FastAPI Requirements

Mandatory files:

```text
main.py
requirements.txt
```

Implementation rules:

* Use `APIRouter`
* Use Pydantic models
* Use async endpoints
* Use `HTTPException`
* Use services when appropriate
* Avoid hardcoded secrets

---

# SQL Backend Requirements

Generate SQL only.

Do not generate:

* C#
* Python
* Java
* Node.js

Generate objects only when required:

* Tables
* Views
* Stored Procedures
* Functions
* Indexes
* Seed data
* Migrations

Rules:

* Use backend-specific SQL syntax
* Use parameterized procedures
* Include primary and foreign keys when defined or implied
* SQL files must end with `.sql`

---

## Final Validation

Before returning JSON:

1. Verify every OpenAPI path is implemented
2. Verify all schemas are generated
3. Verify request and response models exist
4. Verify authentication is implemented when specified
5. Verify file paths follow the required structure
6. Verify the generated project is logically compilable
7. Validate all file paths before returning
8. Return corrected JSON only

The generated JSON must be immediately writable to disk without requiring external path repair.

# OpenAPI YAML Generator Agent Specification — Concise

## Purpose
Convert an `API_CREATE` task into a valid OpenAPI YAML contract suitable for OpenAPI Generator, especially the `aspnetcore` generator.

## Input Contract
```yaml
taskId: US-123-T01
taskCode: API_CREATE
taskName: Create Ingestion Settings API
description: Create API to insert, update and delete data from ingestion settings table
businessContext: Healthcare data platform
technology:
  backend: .net core
  database: mongodb
operations:
  - create
  - update
  - delete
entity: ingestionSettings
```

## Required Output
Return one valid OpenAPI YAML document only.

Required top-level sections:
```yaml
openapi: 3.0.3
info:
servers:
paths:
components:
```

## Naming Rules
- API title: derive from `taskName`.
- Resource path: convert `entity` to kebab-case plural.
  - `ingestionSettings` -> `/ingestion-settings`
  - `patient` -> `/patients`
- Schema base name: convert `entity` to PascalCase singular.
  - `ingestionSettings` -> `IngestionSetting`
- Operation IDs:
  - `create{SchemaName}`
  - `update{SchemaName}`
  - `delete{SchemaName}`
  - `get{SchemaName}`
  - `list{SchemaNamePlural}`

## Operation Mapping
| Input operation | HTTP method and path |
|---|---|
| create | `POST /{resource}` |
| update | `PUT /{resource}/{id}` |
| delete | `DELETE /{resource}/{id}` |
| read | `GET /{resource}/{id}` |
| list | `GET /{resource}` |

## Response Rules
Use these default responses:
- Create: `201`, `400`, `401`, `500`
- Update: `200`, `400`, `401`, `404`, `500`
- Delete: `204`, `401`, `404`, `500`
- Read: `200`, `401`, `404`, `500`
- List: `200`, `401`, `500`

## Schema Rules
Create these schemas when relevant:
- `{SchemaName}CreateRequest`
- `{SchemaName}UpdateRequest`
- `{SchemaName}Response`
- `ErrorResponse`

When input fields are missing, use safe default properties:
```yaml
name:
  type: string
description:
  type: string
isActive:
  type: boolean
```

For response schemas, also include:
```yaml
id:
  type: string
createdAt:
  type: string
  format: date-time
updatedAt:
  type: string
  format: date-time
```

## Security Rules
If `businessContext` includes healthcare, platform, admin, secure, protected or enterprise:
- Add bearer JWT security scheme.
- Add security requirement to each operation.

## Technology Vendor Extensions
When supplied, include:
```yaml
x-backend: ".net core"
x-database: "mongodb"
```
These are valid OpenAPI extensions and can be ignored safely by OpenAPI Generator.

## OpenAPI Generator Compatibility Rules
- Use valid OpenAPI 3.0.3 syntax.
- Use stable schema references with `$ref`.
- Avoid unsupported custom syntax.
- Avoid markdown.
- Do not include implementation code.
- Do not include database connection code.
- Do not include MongoDB query logic.
- Do not include ASP.NET Core source code.

## Output Validation Checklist
Before returning:
1. YAML is valid.
2. `openapi`, `info`, `paths` and `components` exist.
3. Every operation has `summary`, `operationId`, `tags` and `responses`.
4. Request bodies use `application/json`.
5. Path parameter `{id}` is defined where used.
6. Schemas are defined under `components.schemas`.
7. Security scheme is defined when security is applied.
8. No markdown fences or explanation are included.

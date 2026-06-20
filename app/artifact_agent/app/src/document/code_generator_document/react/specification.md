# React Frontend Code Generator Specification

## Purpose

Generate a complete React + TypeScript + Vite frontend application from OpenAPI YAML.

The generated project must be structured, typed, and runnable.

## Technology Stack

* React
* TypeScript
* Vite
* React Router
* Axios
* CSS

## Required Project Structure

Root:

* package.json
* index.html
* vite.config.ts
* tsconfig.json
* tsconfig.node.json
* README.md
* .env.example

Source:

* src/main.tsx
* src/App.tsx
* src/routes/AppRoutes.tsx
* src/api/apiClient.ts
* src/types/api.types.ts
* src/styles/global.css

Additional folders when needed:

* src/api/endpoints/
* src/types/
* src/pages/
* src/components/

## package.json Requirements

Required scripts:

```json
{
  "dev": "vite",
  "build": "tsc -b && vite build",
  "preview": "vite preview",
  "lint": "eslint ."
}
```

Required dependencies:

* react
* react-dom
* react-router-dom
* axios

Required devDependencies:

* typescript
* vite
* @vitejs/plugin-react
* eslint
* @types/react
* @types/react-dom

## Environment Configuration

Generate:

```text
.env.example
```

Content:

```text
VITE_API_BASE_URL=http://localhost:8000
```

All API communication must use:

```typescript
import.meta.env.VITE_API_BASE_URL
```

## API Generation

Generate:

```text
src/api/apiClient.ts
```

Requirements:

* Axios instance
* Base URL configuration
* JSON headers
* Error interceptor

For every OpenAPI resource generate:

```text
src/api/endpoints/<resource>.service.ts
```

Each service must implement all operations defined in OpenAPI.

## Type Generation

Generate:

```text
src/types/api.types.ts
```

For each resource generate:

```text
src/types/<resource>.types.ts
```

Generate:

* Request interfaces
* Response interfaces
* Entity interfaces
* Error interfaces when defined

Type mapping:

```text
string     -> string
integer    -> number
number     -> number
boolean    -> boolean
array      -> Type[]
object     -> interface
date       -> string
date-time  -> string
```

## UI Generation

For every primary resource generate:

```text
src/pages/<Resource>Page.tsx
```

Generate reusable components under:

```text
src/components/<resource>/
```

Examples:

```text
<Resource>Form.tsx
<Resource>Table.tsx
```

Generate only when required by the OpenAPI operations.

## Functional UI Requirement

Pages must contain working UI behavior.

If the application represents a standalone feature:

* Calculator
* Converter
* Todo App
* Counter
* Form Application
* Dashboard

Implement the required client-side functionality directly in React.

Do not generate pages that only wrap API calls.

The generated application should remain usable without a running backend unless backend dependency is explicitly required.

## Routing

Generate:

```text
src/routes/AppRoutes.tsx
```

Requirements:

* BrowserRouter
* Routes
* Route
* Default route
* Resource routes

## App Entry

Generate:

```text
src/App.tsx
```

Requirements:

* Import AppRoutes
* Import global.css
* Render application routes

## README

README.md must include:

* Project overview
* Setup instructions
* npm install
* npm run dev
* npm run build
* Environment configuration

## Output Requirements

Return:

```json
{
  "backend": "react",
  "files": {
    "relative/path/file.ext": {
      "language": "language_name",
      "content": "file content"
    }
  }
}
```

Every generated file must contain:

* language
* content

All file paths must be relative paths inside the generated React project.

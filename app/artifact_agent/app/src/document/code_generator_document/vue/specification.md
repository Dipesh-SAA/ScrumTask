# Vue Frontend Code Generator Specification

## Purpose

Generate a complete Vue 3 + TypeScript frontend application from OpenAPI YAML.

The generated project must be structured, typed, and runnable.

## Technology Stack

- Vue 3
- TypeScript
- Vite
- Vue Router
- Axios
- CSS

## Required Project Structure

Root:

- package.json
- index.html
- vite.config.ts
- tsconfig.json
- README.md
- .env.example

Source:

- src/main.ts
- src/App.vue
- src/router/index.ts
- src/api/apiClient.ts
- src/types/api.types.ts
- src/assets/styles.css

Additional folders when needed:

- src/api/endpoints/
- src/types/
- src/views/
- src/components/

## package.json Requirements

Required scripts:

{
  "dev": "vite",
  "build": "vue-tsc && vite build",
  "preview": "vite preview"
}

Required dependencies:

- vue
- vue-router
- axios

Required devDependencies:

- vite
- typescript
- vue-tsc
- @vitejs/plugin-vue

## Environment Configuration

Generate:

.env.example

Content:

VITE_API_BASE_URL=http://localhost:8000

All API communication must use:

import.meta.env.VITE_API_BASE_URL

## API Generation

Generate:

src/api/apiClient.ts

Requirements:

- Axios instance
- Base URL configuration
- JSON headers
- Error interceptor

For every OpenAPI resource generate:

src/api/endpoints/<resource>.service.ts

Each service must implement all operations defined in OpenAPI.

## Type Generation

Generate:

src/types/api.types.ts

For each resource generate:

src/types/<resource>.types.ts

Generate:

- Request interfaces
- Response interfaces
- Entity interfaces
- Error interfaces when defined

Type mapping:

string     -> string
integer    -> number
number     -> number
boolean    -> boolean
array      -> Type[]
object     -> interface
date       -> string
date-time  -> string

## UI Generation

For every primary resource generate:

src/views/<Resource>View.vue

Generate reusable components when needed:

src/components/<resource>/

Examples:

- ResourceForm.vue
- ResourceTable.vue

## Functional UI Requirement

Pages must contain working UI behavior.

If the application represents:

- Calculator
- Converter
- Todo App
- Counter
- Form Application
- Dashboard

Implement the required client-side functionality directly in Vue.

Do not generate pages that only wrap API calls.

The generated application should remain usable without a running backend unless backend dependency is explicitly required.

## Routing

Generate:

src/router/index.ts

Requirements:

- createRouter
- createWebHistory
- Default route
- Resource routes

## App Entry

Generate:

src/App.vue

Requirements:

- RouterView
- Global layout

## README

README.md must include:

- Project overview
- Setup instructions
- npm install
- npm run dev
- npm run build
- Environment configuration

## Output Requirements

Return:

{
  "backend": "vue",
  "files": {
    "relative/path/file.ext": {
      "language": "language_name",
      "content": "file content"
    }
  }
}

Every generated file must contain:

- language
- content

All file paths must be relative paths inside the generated Vue project.
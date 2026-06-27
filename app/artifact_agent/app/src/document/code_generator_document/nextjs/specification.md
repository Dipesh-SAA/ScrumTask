# Next.js Frontend Code Generator Specification

## Purpose

Generate a complete Next.js + TypeScript frontend application from OpenAPI YAML.

The generated project must be structured, typed, runnable, and production-ready.

## Technology Stack

* Next.js
* React
* TypeScript
* Axios
* CSS

## Required Project Structure

Root:

* package.json
* next.config.js
* tsconfig.json
* README.md
* .env.example

Source:

* src/app/layout.tsx
* src/app/page.tsx
* src/app/globals.css
* src/lib/apiClient.ts
* src/types/api.types.ts

Additional folders when required:

* src/app/<resource>/page.tsx
* src/components/
* src/services/
* src/types/

## package.json Requirements

Required scripts:

```json
{
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "lint": "next lint"
}
```

Required dependencies:

* next
* react
* react-dom
* axios

Required devDependencies:

* typescript
* @types/node
* @types/react
* @types/react-dom
* eslint
* eslint-config-next

## Environment Configuration

Generate:

.env.example

Content:

NEXT_PUBLIC_API_BASE_URL=http://localhost:8000

All API communication must use:

process.env.NEXT_PUBLIC_API_BASE_URL

## API Generation

Generate:

src/lib/apiClient.ts

Requirements:

* Axios instance
* Base URL configuration
* JSON headers
* Error interceptor

For every OpenAPI resource generate:

src/services/<resource>.service.ts

Each service must implement all OpenAPI operations defined in the YAML.

## Type Generation

Generate:

src/types/api.types.ts

For each resource generate:

src/types/<resource>.types.ts

Generate:

* Request interfaces
* Response interfaces
* Entity interfaces
* Error interfaces when defined

Type Mapping:

* string → string
* integer → number
* number → number
* boolean → boolean
* array → Type[]
* object → interface
* date → string
* date-time → string

## UI Generation

For every resource generate:

src/app/<resource>/page.tsx

Generate reusable components when required:

src/components/<resource>/

Examples:

* ResourceForm.tsx
* ResourceTable.tsx
* ResourceResult.tsx

## Functional UI Requirement

The generated frontend must be independently usable.

Do not generate pages that only wrap API calls.

For applications such as:

* Calculator
* Addition
* Converter
* Counter
* Todo App
* Dashboard
* Form Application

implement the business logic directly in Next.js.

Example:

Calculator or Addition pages must:

* Accept user input
* Store values using useState
* Perform calculations locally
* Display results
* Handle validation and errors

The application must remain usable even when no backend is running.

## Client Component Rules

If a file uses:

* useState
* useEffect
* useRef
* Event handlers
* Form submission
* Browser APIs

it must start with:

"use client";

## Routing

Use Next.js App Router only.

Generate routes using:

* src/app/page.tsx
* src/app/<resource>/page.tsx

Do not use:

* react-router-dom
* BrowserRouter
* Routes
* Route

## App Layout

Generate:

src/app/layout.tsx

Requirements:

* Import globals.css
* Render children
* Export metadata when appropriate

## Home Page

Generate:

src/app/page.tsx

Requirements:

* Display application title
* Provide navigation to generated resources
* Serve as the landing page

## README

README.md must include:

* Project overview
* Setup instructions
* npm install
* npm run dev
* npm run build
* Environment configuration

## Output Format

Return:

{
"backend": "nextjs",
"files": {
"relative/path/file.ext": {
"language": "language_name",
"content": "file content"
}
}
}

Every generated file must contain:

* language
* content

All file paths must be relative paths inside the generated Next.js project.

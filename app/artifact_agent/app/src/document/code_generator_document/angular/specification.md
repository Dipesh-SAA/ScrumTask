# Angular Frontend Code Generator Specification

## Purpose

Generate a complete Angular + TypeScript frontend application from OpenAPI YAML.

The generated project must be structured, typed, and runnable.

## Technology Stack

- Angular
- TypeScript
- Angular Router
- Angular HttpClient
- RxJS
- CSS

## Required Project Structure

Root:

- package.json
- angular.json
- tsconfig.json
- tsconfig.app.json
- README.md

Source:

- src/main.ts
- src/index.html
- src/styles.css
- src/app/app.component.ts
- src/app/app.config.ts
- src/app/app.routes.ts
- src/app/core/api/api-client.service.ts
- src/app/core/models/api.types.ts
- src/environments/environment.ts
- src/environments/environment.prod.ts

Additional folders when needed:

- src/app/core/services/
- src/app/core/models/
- src/app/features/

## package.json Requirements

Required scripts:

{
  "start": "ng serve",
  "build": "ng build",
  "test": "ng test"
}

Required dependencies:

- @angular/animations
- @angular/common
- @angular/compiler
- @angular/core
- @angular/forms
- @angular/platform-browser
- @angular/router
- rxjs
- tslib
- zone.js

Required devDependencies:

- @angular/cli
- @angular/compiler-cli
- typescript

## Environment Configuration

Generate:

src/environments/environment.ts

Content:

export const environment = {
  production: false,
  apiBaseUrl: 'http://localhost:8000'
};

Generate:

src/environments/environment.prod.ts

Content:

export const environment = {
  production: true,
  apiBaseUrl: ''
};

All API communication must use:

environment.apiBaseUrl

## API Generation

Generate:

src/app/core/api/api-client.service.ts

Requirements:

- Injectable service
- HttpClient instance
- Base URL configuration
- get<T>
- post<T>
- put<T>
- patch<T>
- delete<T>

For every OpenAPI resource generate:

src/app/core/services/<resource>.service.ts

Each service must implement all operations defined in OpenAPI.

## Type Generation

Generate:

src/app/core/models/api.types.ts

For each resource generate:

src/app/core/models/<resource>.types.ts

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

src/app/features/<resource>/<resource>.component.ts

Generate reusable components when needed:

src/app/features/<resource>/<resource>-form.component.ts
src/app/features/<resource>/<resource>-table.component.ts

## Functional UI Requirement

Pages must contain working UI behavior.

If the application represents a standalone feature:

- Calculator
- Converter
- Todo App
- Counter
- Form Application
- Dashboard

Implement the required client-side functionality directly in Angular.

Do not generate pages that only wrap API calls.

The generated application should remain usable without a running backend unless backend dependency is explicitly required.

## Routing

Generate:

src/app/app.routes.ts

Requirements:

- Import Routes from @angular/router
- Export routes
- Include default route
- Include resource routes

## App Config

Generate:

src/app/app.config.ts

Requirements:

- Import ApplicationConfig
- Import provideRouter
- Import provideHttpClient
- Export appConfig

## App Component

Generate:

src/app/app.component.ts

Requirements:

- Standalone component
- Import RouterOutlet
- Render router-outlet

## README

README.md must include:

- Project overview
- Setup instructions
- npm install
- npm start
- npm run build
- Environment configuration

## Output Requirements

Return:

{
  "backend": "angular",
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

All file paths must be relative paths inside the generated Angular project.
# Node.js Express Code Generator Specification

## Purpose

Generate a complete, runnable Node.js + Express backend application from OpenAPI YAML.

The generated output must follow clean layered architecture and must match `x-backend: nodejs`.

## Technology Stack

- Node.js
- Express
- JavaScript
- dotenv
- cors

## Required Project Structure

Root files:

- package.json
- app.js
- README.md
- .env.example

Source folders:

- src/routes/
- src/controllers/
- src/services/
- src/models/
- src/middleware/
- src/config/

Optional folders when needed:

- src/utils/
- src/storage/
- src/validators/

## package.json Rules

- package.json must be valid JSON.
- Use double quotes only.
- Include `start` and `dev` scripts.
- The `start` script must point to the file that calls `app.listen()`.
- The `dev` script must point to the same server startup file.
- Do not point scripts to a file that only exports the Express app.
- If `nodemon` is used, include it in `devDependencies`.
- Every imported third-party package must appear in `dependencies`.
- Do not include unused dependencies.
- All JSON examples must be valid JSON.

If `app.js` contains `app.listen()`, use:

{
  "scripts": {
    "start": "node app.js",
    "dev": "nodemon app.js"
  }
}

If `src/server.js` contains `app.listen()`, use:

{
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon src/server.js"
  }
}

Default dependencies:

- express
- cors
- dotenv

## Server Entry Rules

The file used by the `start` script must:

- load environment variables
- create the Express app
- enable JSON middleware
- enable CORS
- register all routes
- register centralized error middleware
- call `app.listen(PORT)`

The generated app must be runnable using:

```bash
npm install
npm start
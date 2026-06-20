# ASP.NET Core Backend Code Generator Specification

Read the OpenAPI YAML and generate ASP.NET Core source code according to `x-backend`.

## Backend Selection

Use only the backend value from:

x-backend: <backend>

If `x-backend` is `.net`, `dotnet`, `c#`, `csharp`, `asp.net`, `asp.net core`, or `aspnetcore`, generate ASP.NET Core Web API source code.

Do not generate code for any other backend in this specification file.

## Output Format

Return ONLY valid JSON.

Do not return markdown.
Do not return explanations.
Do not return code fences.

The JSON must follow this exact structure:

{
  "backend": ".net",
  "files": {
    "relative/path/file.ext": {
      "language": "csharp",
      "content": "file content here"
    }
  }
}

## Project Type

Generate an ASP.NET Core Web API project.

The generated project must be runnable with:

dotnet restore
dotnet build
dotnet run

## Required Root Files

For ASP.NET Core, ONLY these files are allowed at the project root:

- Program.cs
- appsettings.json
- <ProjectName>.csproj

No other file may be created at the project root.

## Required Folder Structure

All generated ASP.NET Core files must follow this structure:

- Properties/launchSettings.json
- Controllers/<Name>Controller.cs
- Models/Requests/<Name>Request.cs
- Models/Responses/<Name>Response.cs
- Models/Responses/ErrorResponse.cs
- Services/Interfaces/I<Name>Service.cs
- Services/Implementations/<Name>Service.cs

## Strictly Forbidden Root-Level Files

Never generate these files at root:

- launchSettings.json
- <Name>Controller.cs
- <Name>Request.cs
- <Name>Response.cs
- ErrorResponse.cs
- I<Name>Service.cs
- <Name>Service.cs

## Strictly Forbidden Incomplete Folders

Never generate these incomplete folders:

- Requests/<Name>Request.cs
- Responses/<Name>Response.cs
- Interfaces/I<Name>Service.cs
- Implementations/<Name>Service.cs

## Valid File Path Examples

Correct:

- Controllers/SelectionSortController.cs
- Models/Requests/SelectionSortCreateRequest.cs
- Models/Requests/SelectionSortUpdateRequest.cs
- Models/Responses/SelectionSortResponse.cs
- Models/Responses/ErrorResponse.cs
- Services/Interfaces/ISelectionSortService.cs
- Services/Implementations/SelectionSortService.cs
- Properties/launchSettings.json

Invalid:

- SelectionSortController.cs
- SelectionSortCreateRequest.cs
- SelectionSortResponse.cs
- ErrorResponse.cs
- ISelectionSortService.cs
- SelectionSortService.cs
- launchSettings.json
- Requests/SelectionSortCreateRequest.cs
- Responses/SelectionSortResponse.cs
- Interfaces/ISelectionSortService.cs
- Implementations/SelectionSortService.cs

## Final File Path Validation

Before returning JSON:

1. Inspect every key in the `files` object.
2. Check that every file path is relative to the project root.
3. Do not include the project name as the first folder.
4. Do not include API title as the first folder.
5. Do not include backend name as the first folder.
6. Do not include `src` as the first folder.
7. Do not include `app` as the first folder.
8. If any file violates the ASP.NET Core structure, correct the path before returning.
9. The response is invalid if any forbidden path exists.

## Source Code Requirements

Generate clean ASP.NET Core C# code.

Use:

- Controllers for HTTP endpoints
- Request models for input DTOs
- Response models for output DTOs
- Service interfaces for abstraction
- Service implementations for business logic
- Dependency injection in Program.cs
- Swagger/OpenAPI support
- Proper HTTP status codes
- ErrorResponse model for errors
- appsettings.json
- Properties/launchSettings.json

## Entity Framework Core Rules

If the YAML or instructions require database support, generate Entity Framework Core setup.

Use SQL Server when instructions mention SQL Server.

Required EF Core files may be added only if needed:

- Data/AppDbContext.cs
- Models/Entities/<Name>.cs

If repository pattern is required, use:

- Repositories/Interfaces/I<Name>Repository.cs
- Repositories/Implementations/<Name>Repository.cs

Do not create these files unless database or repository logic is required.

## Controller Rules

Controllers must be placed only inside:

Controllers/<Name>Controller.cs

Controllers must:

- Use `[ApiController]`
- Use `[Route("api/[controller]")]` unless OpenAPI YAML specifies exact route handling
- Use constructor injection for services
- Return proper IActionResult or ActionResult<T>
- Match OpenAPI paths and methods

## Model Rules

Request models must be placed only inside:

Models/Requests/<Name>Request.cs

Response models must be placed only inside:

Models/Responses/<Name>Response.cs

Error response must be placed only inside:

Models/Responses/ErrorResponse.cs

## Service Rules

Service interfaces must be placed only inside:

Services/Interfaces/I<Name>Service.cs

Service implementations must be placed only inside:

Services/Implementations/<Name>Service.cs

## Final Requirement

The JSON `files` keys MUST contain the complete folder path exactly as it should appear on disk.

Return ONLY corrected valid JSON.
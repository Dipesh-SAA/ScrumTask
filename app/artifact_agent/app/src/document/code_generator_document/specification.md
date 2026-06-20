# Backend Code Generator Specification

Read the OpenAPI YAML and generate source code according to `x-backend`.

## Backend Selection

Use only the backend value from:

```yaml
x-backend: <backend>

CRITICAL ASP.NET CORE FILE PATH VALIDATION RULES

Before returning JSON, validate every file path in the "files" object.

The keys inside "files" are the FINAL file paths and MUST already be correct.
Do NOT rely on backend code to move or fix files later.

For ASP.NET Core (.NET/C#), ONLY these files are allowed at the project root:

* Program.cs
* appsettings.json
* <ProjectName>.csproj

Required ASP.NET Core folder structure:

* Properties/launchSettings.json
* Controllers/<Name>Controller.cs
* Models/Requests/<Name>Request.cs
* Models/Responses/<Name>Response.cs
* Models/Responses/ErrorResponse.cs
* Services/Interfaces/I<Name>Service.cs
* Services/Implementations/<Name>Service.cs

STRICTLY FORBIDDEN ROOT-LEVEL FILES:

* launchSettings.json
* <Name>Controller.cs
* <Name>Request.cs
* <Name>Response.cs
* ErrorResponse.cs
* I<Name>Service.cs
* <Name>Service.cs

Examples:

INVALID:

* SelectionSortController.cs
* SelectionSortCreateRequest.cs
* SelectionSortResponse.cs
* ErrorResponse.cs
* ISelectionSortService.cs
* SelectionSortService.cs
* launchSettings.json

VALID:

* Controllers/SelectionSortController.cs
* Models/Requests/SelectionSortCreateRequest.cs
* Models/Responses/SelectionSortResponse.cs
* Models/Responses/ErrorResponse.cs
* Services/Interfaces/ISelectionSortService.cs
* Services/Implementations/SelectionSortService.cs
* Properties/launchSettings.json

Before returning the final JSON:

1. Inspect every "files" key.
2. If any file violates the ASP.NET Core structure, automatically correct the path.
3. Return ONLY corrected JSON.
4. The response is INVALID if any forbidden path exists.
5. Never generate ASP.NET Core files at the project root except:

   * Program.cs
   * appsettings.json
   * <ProjectName>.csproj

FINAL REQUIREMENT:
The JSON "files" keys MUST contain the complete folder path exactly as it should appear on disk.

## ASP.NET Core File Path Rules

These rules are mandatory when `x-backend` is `.net`, `dotnet`, `c#`, `csharp`, `asp.net`, or `aspnetcore`.

All file paths inside the JSON `files` object MUST be relative to the project root.

The only files allowed at the project root are:

* Program.cs
* appsettings.json
* <ProjectName>.csproj

All other ASP.NET Core files MUST use these folders:

* Controllers/<Name>Controller.cs
* Models/Requests/<Name>Request.cs
* Models/Responses/<Name>Response.cs
* Models/Responses/ErrorResponse.cs
* Services/Interfaces/I<Name>Service.cs
* Services/Implementations/<Name>Service.cs
* Properties/launchSettings.json

Never generate these files at root:

* launchSettings.json
* <Name>Controller.cs
* <Name>Request.cs
* <Name>Response.cs
* ErrorResponse.cs
* I<Name>Service.cs
* <Name>Service.cs

Never generate these incomplete folders:

* Requests/<Name>Request.cs
* Responses/<Name>Response.cs
* Interfaces/I<Name>Service.cs
* Implementations/<Name>Service.cs

Correct examples:

* Controllers/CalculationsController.cs
* Models/Requests/CalculationCreateRequest.cs
* Models/Responses/CalculationResponse.cs
* Models/Responses/ErrorResponse.cs
* Services/Interfaces/ICalculationService.cs
* Services/Implementations/CalculationService.cs
* Properties/launchSettings.json

Invalid examples:

* CalculationsController.cs
* Requests/CalculationCreateRequest.cs
* Responses/CalculationResponse.cs
* Responses/ErrorResponse.cs
* Interfaces/ICalculationService.cs
* Implementations/CalculationService.cs
* launchSettings.json

Before returning JSON, inspect every key in `files`.

If backend is ASP.NET Core and any invalid file path exists, correct it before returning.

Return ONLY valid JSON with corrected file paths.

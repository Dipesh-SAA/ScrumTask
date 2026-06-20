# SQL Server Code Generator Specification

## Purpose

Generate complete SQL Server database scripts from OpenAPI YAML.

The generated output must be structured, executable, and production-ready.

## Technology

- SQL Server
- T-SQL

## Required File Structure

Use this structure:

tables/
stored_procedures/
views/
functions/
indexes/
seed/
migrations/

Only include folders that contain generated files.

## Data Type Mapping

Use this OpenAPI to SQL Server mapping:

string              -> NVARCHAR(255)
string date         -> DATE
string date-time    -> DATETIME2
integer int32       -> INT
integer int64       -> BIGINT
number float        -> FLOAT
number double       -> FLOAT
boolean             -> BIT
array               -> Separate child table when needed
object              -> Separate table or NVARCHAR(MAX) JSON when suitable
uuid                -> UNIQUEIDENTIFIER

## Table Generation

For every entity schema generate:

tables/<Entity>.sql

Each table should include:

- Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID()
- Entity fields
- NOT NULL for required fields
- NULL for optional fields
- CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
- UpdatedAt DATETIME2 NULL when update is supported

Example:

CREATE TABLE dbo.Customers (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    Name NVARCHAR(255) NOT NULL,
    Email NVARCHAR(255) NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    UpdatedAt DATETIME2 NULL
);
GO

## Relationship Rules

If schemas reference each other:

- Create foreign key columns
- Add FOREIGN KEY constraints
- Generate indexes on foreign key columns

Example:

CustomerId UNIQUEIDENTIFIER NOT NULL,
CONSTRAINT FK_Orders_Customers FOREIGN KEY (CustomerId)
REFERENCES dbo.Customers(Id)

## Stored Procedure Generation

Generate procedures based on OpenAPI operations.

POST -> usp_Create<Entity>
GET list -> usp_GetAll<Entities>
GET by id -> usp_Get<Entity>ById
PUT/PATCH -> usp_Update<Entity>
DELETE -> usp_Delete<Entity>

Use:

CREATE OR ALTER PROCEDURE

Each procedure must:

- Use parameters matching request schema
- Return affected or selected rows where suitable
- Use SET NOCOUNT ON
- Handle CreatedAt and UpdatedAt
- Use dbo schema

## View Generation

Generate views when the requirement mentions:

- view
- report
- dashboard
- summary
- listing
- read model

View file path:

views/<ViewName>.sql

Use:

CREATE OR ALTER VIEW dbo.<ViewName>

Views should:

- Join related tables when useful
- Expose readable columns
- Avoid SELECT *
- Use meaningful aliases

## Function Generation

Generate functions only when useful.

Examples:

- calculate totals
- format display names
- validate derived values

Use:

CREATE OR ALTER FUNCTION

## Index Generation

Generate indexes for:

- foreign key columns
- email fields
- code fields
- status fields
- date fields used for filtering
- name fields used for searching

Use:

CREATE INDEX

or:

CREATE UNIQUE INDEX

when uniqueness is required.

## Seed Data

Generate seed files only when requested.

Use:

seed/<Entity>Seed.sql

Seed scripts must use INSERT statements.

## Migration File

If needed, generate:

migrations/001_initial_schema.sql

This file should execute objects in safe order:

1. Tables
2. Foreign keys
3. Indexes
4. Functions
5. Views
6. Stored procedures
7. Seed data

## Output Format

Return only:

{
  "backend": "sqlserver",
  "files": {
    "relative/path/file.sql": {
      "language": "sql",
      "content": "SQL content"
    }
  }
}

## Invalid Output

Invalid output includes:

- Non-SQL files with format without .sql
- Missing CRUD procedures when CRUD is requested
- Missing views when requested
- Invalid JSON
- Markdown fences
- Python dictionary syntax
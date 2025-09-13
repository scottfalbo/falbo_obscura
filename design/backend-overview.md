# Backend Overview

## Architecture

Domain-Driven Design with Clean Architecture - .NET patterns adapted for FastAPI

## Structure

```txt
backend/
├── main.py                    # App entry point
├── api/                       # API endpoints
├── core/                      # Business logic
├── infrastructure/            # AWS services
└── shared/                    # Cross-cutting
```

## Content Types

- Tattoo, Illustrations, Coding, Game box, Retail, Series, Blog
- **Admin** - Content management

## Key Patterns

- **Repository Pattern** - Data access abstraction
- **Service Layer** - Business logic
- **Dependency Injection** - FastAPI Depends system

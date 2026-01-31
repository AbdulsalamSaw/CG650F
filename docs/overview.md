# Project Overview & Architecture Context

**Goal**: A robust FastAPI Base System with MySQL (Async), customized for performance and scalability.
**Pattern**: Layered Architecture with Strict DTOs (Separation of Concerns).

## 🛠 Tech Stack
- **Framework**: FastAPI (Async)
- **Database**: MySQL 8.0+
- **ORM**: SQLAlchemy 2.0 (Async / `aiomysql`)
- **Validation**: Pydantic v2
- **Migrations**: Alembic
- **Package Manager**: pip (`requirements.txt`)

## 📂 Architecture Map
This project follows a strict separation between Data Layer (Models) and API Layer (Schemas).

| Layer | Directory | Description |
| :--- | :--- | :--- |
| **API** | `app/api/v1/endpoints` | Route handlers (Controllers). **Input**: Pydantic DTOs. **Output**: Pydantic DTOs. |
| **Service** | `app/services` | Business Logic. Bridges API and DB. **Never** return ORM objects to API directly. |
| **Schemas** | `app/schemas` | Pydantic Models (DTOs). Defines the "Public Contract". |
| **Models** | `app/models` | SQLAlchemy Models. Defines the "Database Schema". |
| **Core** | `app/core` | Config (`config.py`), Database (`database.py`), Security (`security.py`). |
| **DB Ops** | `database/` | SQL Scripts (`sql/`), Seeders (`seeders/`), & `migrate.py` utility. |

## 🔐 Key Features implementing
1.  **RBAC System**:
    - Many-to-Many: `Users` <-> `Roles` <-> `Permissions`.
    - Dependencies: `has_permission("users.view")` in `app/core/security.py`.
2.  **Unified DB Manager**:
    - Script: `python database/migrate.py [up|seed|all]`
    - Logic: Runs proper order: `schema.sql` -> `alembic` -> `data.sql` -> `seeders`.

## 🚀 Quick Start Commands
*Run these from project root.*

**Start Server**:
```bash
uvicorn app.main:app --reload
```

**Database Operations**:
```bash
# Sync DB (Create + Migrate + Seed)
python database/migrate.py all

# Run only Seeders
python database/migrate.py seed
```

## 🧠 Critical Context for AI Agents
- **Do NOT run `python app/main.py`** directly. It breaks imports. Use `uvicorn`.
- **Imports**: `sys.path` injection is used in `database/migrate.py` to import `app`. Be careful when refactoring structure.
- **Async**: Everything in `app/` is `async` (SQLAlchemy async session).
- **Models**: All models must be imported in `app/models/__init__.py` to be detected by Alembic.

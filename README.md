# UserTask

A small Flask app for a personal task list. Add a task with a title, a description and a priority, and the list shows the newest first.

<p align="center">
  <img src="docs/landing.png" width="420">
  <img src="docs/tasks.png" width="300">
</p>

## Run

Needs Python 3.11 to 3.13. I tested 3.13. Python 3.14 does not work yet because of the pinned SQLAlchemy.

```sh
git clone https://github.com/makambo13/UserTask.git
cd UserTask
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Open http://127.0.0.1:5000. The SQLite database is created in `instance/` the first time the app starts.

## How it works

- `tasks/routes.py` handles requests
- `tasks/services.py` does the database work
- `tasks/models.py` defines `Task` and `User`
- `tasks/forms.py` has the Flask-WTF form

Not built yet: login, and editing, completing or deleting a task. Every task belongs to user 1.

## System design

### Architecture

```mermaid
%%{init: {"look": "handDrawn", "theme": "neutral"}}%%
flowchart LR
    B["Browser"] -->|"GET /"| H["home()<br/>landing_page.html"]
    B -->|"GET /tasks/<br/>POST /tasks/create"| R

    subgraph Flask["Flask app (create_app in app/__init__.py)"]
        H
        R["tasks blueprint<br/>tasks/routes.py"]
        F["TaskForm<br/>tasks/forms.py<br/>validation + CSRF"]
        S["TaskService<br/>tasks/services.py"]
        M["Task, User models<br/>tasks/models.py"]
        T["Jinja templates<br/>list.html, error.html"]
        R --> F
        R --> S
        R --> T
        S --> M
    end

    M -->|"Flask-SQLAlchemy"| DB[("SQLite<br/>instance/tasks.db")]
    MG["Alembic migrations<br/>migrations/"] -.->|"schema changes"| DB
```

### Request flow

```mermaid
%%{init: {"look": "handDrawn", "theme": "neutral"}}%%
sequenceDiagram
    actor U as User
    participant R as routes.py
    participant F as TaskForm
    participant S as TaskService
    participant D as SQLite

    U->>R: POST /tasks/create (title, description, priority)
    R->>F: validate_on_submit()
    alt form is valid
        R->>S: create_task(user_id=1, ...)
        S->>D: INSERT into tasks, commit
        alt database error
            S->>D: rollback
            R-->>U: 500 error.html
        else saved
            R-->>U: redirect to /tasks/
            U->>R: GET /tasks/
            R->>S: get_user_tasks(user_id=1)
            S->>D: SELECT tasks, newest first
            R-->>U: list.html with tasks
        end
    else form is invalid
        R-->>U: list.html with form errors
    end
```

### Data model

```mermaid
%%{init: {"look": "handDrawn", "theme": "neutral"}}%%
erDiagram
    USER ||--o{ TASK : owns
    USER {
        int id PK
        string username UK
        string email UK
        string password_hash
    }
    TASK {
        int id PK
        string title
        text description
        int user_id FK
        datetime created_at
        string status "default pending"
        string priority "High, Medium, Low"
    }
```

The `User` table exists, but login is not built yet, so every task is saved for user 1.

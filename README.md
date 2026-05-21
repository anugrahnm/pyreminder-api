# pyreminder-api

A REST API for with authentication for managing reminders, built with FastAPI and PostgreSQL.

## Endpoints

| Method | Path              | Description        | Status           |
| ------ | ----------------- | ------------------ | ---------------- |
| GET    | `/reminders`      | Get all reminders  | COMPLETE         |
| POST   | `/reminders`      | Add a new reminder | COMPLETE         |
| PUT    | `/reminders/{id}` | Edit a reminder    | COMPLETE         |
| DELETE | `/reminders/{id}` | Delete a reminder  | COMPLETE         |
| POST   | `/signup/`        | Add User           | WORK IN PROGRESS |
| POST   | `/login/`         | Fetch User         | WORK IN PROGRESS |

## Demo

> 🚨 Warning: Auth is still in progress.

[Railway](https://pyreminder-api-production.up.railway.app/docs)

> Note: Enter the date in the format: dd/mm/yyyy

## Usage

```bash
uv run uvicorn main:app --reload
```

Interactive docs available at `http://localhost:8000/docs`

## Setup

**1. Clone the repo and install dependencies**

```bash
git clone https://github.com/anugrahnm/pyreminder-api
cd pyreminder-api
uv sync
```

**2. Create a `.env` file**

```
# Postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pyreminder
DB_USER=postgres
DB_PASSWORD=your_password

# JWT
SECRET_KEY = secret_key
```

**3. Run**

```bash
uv run uvicorn main:app --reload
```

## Built with

- Python
- FastAPI
- PostgreSQL
- psycopg2-binary
- python-dotenv

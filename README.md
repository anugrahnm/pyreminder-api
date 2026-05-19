# pyreminder-api

A REST API for managing reminders, built with FastAPI and PostgreSQL.

## Endpoints


| Method | Path              | Description        |
| ------ | ----------------- | ------------------ |
| GET    | `/reminders`      | Get all reminders  |
| POST   | `/reminders`      | Add a new reminder |
| PUT    | `/reminders/{id}` | Edit a reminder    |
| DELETE | `/reminders/{id}` | Delete a reminder  |


## Demo

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
DB_HOST=localhost
DB_PORT=5432
DB_NAME=pyreminder
DB_USER=postgres
DB_PASSWORD=your_password
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


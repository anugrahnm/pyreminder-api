from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = FastAPI()

# reminders = [{"name": "test", "due_date": "26/06/2026"}]

@app.get("/reminders")
async def get_reminders():
    try:    
        with psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
            ) as connection_obj:     
            
            print("Connected to PostgreSQL")
    except psycopg2.Error as e:
        print(e)

    cursor_obj = connection_obj.cursor()

   

    results = [{cursor_obj.execute("""SELECT * FROM reminders""")}]

    rows = cursor_obj.fetchall()
    return [{"id": row[0], "reminder_name": row[1], "due_date": str(row[2])} for row in rows]

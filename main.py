from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv
from datetime import date, datetime
from pydantic import BaseModel, field_validator

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = FastAPI()

# reminders = [{"name": "test", "due_date": "26/06/2026"}]

@app.get("/reminders/")
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

   

    cursor_obj.execute("""SELECT * FROM reminders""")

    rows = cursor_obj.fetchall()
    return [{"id": row[0], "reminder_name": row[1], "due_date": str(row[2])} for row in rows]


class Item(BaseModel):
    reminder_name: str
    due_date: date

    @field_validator('due_date', mode='before')
    @classmethod
    def date_parse(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, "%d/%m/%Y").date()
        return value


@app.post("/reminders/")
async def add_reminders(item: Item):
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

    add_reminder_query = """
            INSERT INTO REMINDERS (reminder_name, due_date) VALUES (%s,%s)
        """
    ddate = item.due_date
    
    cursor_obj.execute(add_reminder_query, [item.reminder_name, ddate])
    connection_obj.commit()
    print("Reminder Added!")
   
    return item


@app.put("/reminders/{id}")
async def edit_reminder(id: int, item: Item):
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

    
    update_name_due_date_query = """
        UPDATE REMINDERS
        SET reminder_name = %s, due_date = %s
        WHERE id = %s
        """
    cursor_obj.execute(update_name_due_date_query, [item.reminder_name, item.due_date, id])
    connection_obj.commit()
    print("Reminder Added!")

    return id

@app.delete("/reminders/{id}")
async def delete_reminder(id: int):
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
    
    delete_reminder_query = """
                DELETE FROM REMINDERS WHERE id = %s
            """
    try:
        cursor_obj.execute(delete_reminder_query, (id, ))
        connection_obj.commit()
    except ValueError as e:
        print(e)
    
    return id
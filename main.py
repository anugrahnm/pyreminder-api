from fastapi import FastAPI
import psycopg2
import os
from dotenv import load_dotenv
from datetime import date, datetime
from pydantic import BaseModel, field_validator
from typing import Optional
import bcrypt
from jose import jwt

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

# reminders = [{"name": "test", "due_date": "26/06/2026"}]

@app.get("/")
async def read_root():
    return {"message": "Welcome to the pyreminder-api!"}   


@app.get("/reminders/")
async def get_reminders(id: Optional[int] = None):
    try:    
        with psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
            ) as connection_obj:     
            
            print("Connected to PostgreSQL")
            cursor_obj = connection_obj.cursor()

            if id is not None:
                cursor_obj.execute("""SELECT * FROM reminders WHERE id = %s""", (id,))

            else:
                cursor_obj.execute("""SELECT * FROM reminders""")

            rows = cursor_obj.fetchall()
            return [{"id": row[0], "reminder_name": row[1], "due_date": str(row[2])} for row in rows]

    except psycopg2.Error as e:
        print(e)
        return {"error": "Database issue", "details": str(e)}

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
            cursor_obj = connection_obj.cursor()

            add_reminder_query = """
                    INSERT INTO REMINDERS (reminder_name, due_date) VALUES (%s,%s)
                """
            ddate = item.due_date
            
            cursor_obj.execute(add_reminder_query, [item.reminder_name, ddate])
            connection_obj.commit()
            print("Reminder Added!")
        
            return item

    except psycopg2.Error as e:
        print(e)
        return {"error": "Database issue", "details": str(e)}
    

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

    except psycopg2.Error as e:
        print(e)
        return {"error": "Database issue", "details": str(e)}



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
    except psycopg2.Error as e:
        print(e)
        return {"error": "Database issue", "details": str(e)}


class User(BaseModel):
    email: str
    password: str

    @field_validator("password", mode="before")
    @classmethod
    def hash_password(cls, value):
        pw = bytes(value, encoding="utf-8")
        hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
        return hashed


@app.post("/signup/")
async def add_user(user: User):
    try:    
        with psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
            ) as connection_obj:     
            
            print("Connected to PostgreSQL")

            with connection_obj.cursor() as cursor_obj:
            
                add_user_query = """
                    INSERT INTO users (email, password_hash) VALUES (%s,%s) 
                """
                try:
                    cursor_obj.execute(add_user_query, (user.email, user.password, ))
                    connection_obj.commit()
                except ValueError as e:
                    print(e)
                
                return {"message":"Successfully created new user!"}
    except psycopg2.errors.UniqueViolation as e:
        print(e)
        return {"error": "This email is already registered! Login or try again with a different email.", "details": str(e)}

    except psycopg2.Error as e:
        print(e)
        return {"error": "Database issue", "details": str(e)}

class LoginUser(BaseModel):
    email: str
    password: str

@app.post("/login/")
async def get_user(login_user: LoginUser):
    try:    
        with psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
            ) as connection_obj:     
            
            print("Connected to PostgreSQL")

            with connection_obj.cursor() as cursor_obj:
            
                get_user_query = """
                    SELECT * FROM users WHERE email= %s
                """
                try:
                    cursor_obj.execute(get_user_query, (login_user.email, ))
                    result = cursor_obj.fetchone()
                    pw = result[2].encode("utf-8")
                    if bcrypt.checkpw(login_user.password.encode("utf-8"), pw):
                        print("It Matches!")
                        token = jwt.encode({ 'id': result[0] }, SECRET_KEY, algorithm='HS256')

                        return token
                    else:
                        print("It Does not Match :(")
                        return {"message":f"User Found But Password Doesn't Match: {login_user.email}!"}

                except ValueError as e:
                    print(e)
                

    except psycopg2.Error as e:
        print(e)
        return {"error": "Database issue", "details": str(e)}
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
users = []
app = FastAPI()
app = FastAPI(
    title="Nexus API",
    description="AI-powered knowledge engine backend",
    version="1.0.0"
)
class User(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

@app.get("/")
def home():
    return {
        "message": "Welcome to Nexus!"
    }

@app.get("/version")
def version():
    return {
        "version": "1.0.0"
    }
@app.get("/status")
def status():
    return {
        "status": "online"
    }

@app.post("/register")
def register(user: User):
    users.append(user)

    return {
        "message": "User registered successfully!"
    }

@app.get("/users")
def get_users():
    return [
        {
            "name": user.name,
            "email": user.email
        }
        for user in users
    ]

@app.get("/users")
def get_users():
    return [
        {
            "name": user.name,
            "email": user.email
        }
        for user in users
    ]

@app.get("/find-user/{email}")
def find_user(email: str):

    for user in users:
        if user.email == email:
            return{
                "name": user.name,
                "email": user.email
            }

    return {
        "message": "User not found"
    }
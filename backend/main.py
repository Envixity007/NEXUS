from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from database.database import get_db
from models.user import User as UserModel
from utils.security import hash_password, verify_password

app = FastAPI(
    title="Nexus API",
    description="AI-powered knowledge engine backend",
    version="1.0.0"
)


class User(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

class Login(BaseModel):
    email: EmailStr
    password: str

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
def register(user: User, db: Session = Depends(get_db)):

    existing_user = (
        db.query(UserModel)
        .filter(UserModel.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )
    print("Password:", user.password)
    print("Type:", type(user.password))
    print("Length:", len(user.password))

    new_user = UserModel(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully!",
        "id": new_user.id
    }

@app.post("/login")
def login(login_data: Login, db: Session = Depends(get_db)):

    user = (
        db.query(UserModel)
        .filter(UserModel.email == login_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    return {
        "message": "Login successful"
    }


@app.get("/users")
def get_users(db: Session = Depends(get_db)):

    users = db.query(UserModel).all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in users
    ]


@app.get("/find-user/{email}")
def find_user(email: str, db: Session = Depends(get_db)):

    user = (
        db.query(UserModel)
        .filter(UserModel.email == email)
        .first()
    )

    if user:
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )
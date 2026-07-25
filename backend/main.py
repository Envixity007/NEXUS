from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from database.database import get_db
from models.user import User as UserModel
from utils.security import hash_password, verify_password
from utils.jwt_handler import create_access_token, verify_access_token

app = FastAPI(
    title="Nexus API",
    description="AI-powered knowledge engine backend",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload


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

    access_token = create_access_token(
        data={
            "user_id": user.id,
            "email": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/users")
def get_users(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

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
def find_user(
    email: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):

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
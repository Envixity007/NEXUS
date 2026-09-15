from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from models.user import User as UserModel
from utils.dependencies import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def get_users(
    current_user: UserModel = Depends(get_current_user),
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


@router.get("/find/{email}")
def find_user(
    email: str,
    current_user: UserModel = Depends(get_current_user),
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


@router.get("/me")
def get_me(
    current_user: UserModel = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }
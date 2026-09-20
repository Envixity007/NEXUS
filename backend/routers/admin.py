from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database.database import get_db
from models.user import User as UserModel
from utils.dependencies import require_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

class RoleUpdate(BaseModel):
    role: Literal["student", "admin"]

@router.get("/users")
def get_all_users(
    current_user: UserModel = Depends(require_admin),
    db: Session = Depends(get_db)
):
    users = db.query(UserModel).all()

    return[
        {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
        }
        for user in users
    ]

@router.patch("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    role_data: RoleUpdate,
    current_user: UserModel = Depends(require_admin),
    db: Session = Depends(get_db)
):
    user = (
        db.query(UserModel)
        .filter(UserModel.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User ain't found"
        )

    user.role = role_data.role

    db.commit()
    db.refresh(user)

    return{
        "message": "User role has been updated successfully",
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: UserModel = Depends(require_admin),
    db: Session = Depends(get_db)
):
    user = (
        db.query(UserModel)
        .filter(UserModel.id == user_id)
        .first()
    )
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User ain't found"
        )
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Admin can't delete their own account"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User deleted successfully",
        "id": user_id
    }
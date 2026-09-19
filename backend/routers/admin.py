from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.database import get_db
from models.user import User as UserModel
from utils.dependencies import require_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

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
from fastapi import APIRouter, Depends

from models.user import User as UserModel
from utils.dependencies import require_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/users")
def get_all_users(
    current_user: UserModel = Depends(require_admin)
):
    return {
        "message": "Welcome Admin",
        "admin": current_user.email
    }


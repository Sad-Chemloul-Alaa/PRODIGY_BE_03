from fastapi import APIRouter , Depends ,status,Response 
from typing import List
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse , User ,UserUpdate
from uuid import UUID
from app.crud import user as crud_user
from app.core.database import get_db
from app.security.jwt import get_current_user, require_roles
from app.models.user import Role, User as user_model
router = APIRouter(
    prefix="/user",
    tags=['user']
)

@router.get("/me", response_model=UserResponse)
def get_current_user_infos(current: User = Depends(get_current_user)):
    return crud_user.Get_current_user_info(current)

@router.get('/{user_id}' , response_model=UserResponse,dependencies=[Depends(require_roles(Role.admin))])
def get_user_by_id(user_id: UUID ,db: Session = Depends(get_db)):
    return crud_user.Get_user_infos_by_id(user_id, db)

@router.put("/", response_model=UserResponse)
def update_user(payload: UserUpdate, db: Session = Depends(get_db), current: user_model = Depends(get_current_user)):
    return crud_user.update_current_user(db, current, payload)

@router.get("/", response_model=List[UserResponse], dependencies=[Depends(require_roles(Role.admin))])
def get_all_users(db: Session = Depends(get_db)):
    return crud_user.Display_all_users_infos(db)

@router.delete("/{user_id}", dependencies=[Depends(require_roles(Role.admin))])
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    return crud_user.Delete_user(user_id, db)

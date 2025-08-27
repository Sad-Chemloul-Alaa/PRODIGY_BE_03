from fastapi import APIRouter , Depends ,status,Response 
from typing import List
from sqlalchemy.orm import Session
from app.schemas.user import UserResponse , User ,UserUpdate
from uuid import UUID
from app.crud import user as crud_user
from app.core.database import get_db

router = APIRouter(
    prefix="/user",
    tags=['user']
)


@router.get('/' , response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return crud_user.Display_all_users_infos(db)
    
@router.get('/{user_id}' , response_model=UserResponse)
def get_user_by_id(user_id: UUID ,db: Session = Depends(get_db)):
    return crud_user.Get_user_infos_by_id(user_id, db)

@router.put('/{user_id}' , response_model=UserResponse)
def update_user(user_id: UUID ,data: UserUpdate,db: Session = Depends(get_db)):
    return crud_user.Update_user( user_id, data ,db)

@router.post('/' , response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: User,db: Session = Depends(get_db)):
    return crud_user.Create_user(data , db)

@router.delete('/{user_id}')
def delete_user(user_id: UUID,db: Session = Depends(get_db)):
    return crud_user.Delete_user(user_id , db)
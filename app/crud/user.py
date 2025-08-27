from fastapi import Depends ,Response ,HTTPException ,status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import user as user_schemas
from app.models.user import User as user_model
from uuid import UUID
from app.security.jwt import get_current_user
from sqlalchemy.exc import IntegrityError

def update_current_user(db: Session, current: user_model, payload: user_schemas.UserUpdate) -> user_model:
    if payload.user_name is not None:
        current.user_name = payload.user_name
    if payload.password:
        from app.security.hash import hash_password
        current.user_hashed_password = hash_password(payload.password)
    db.add(current)
    db.commit()
    db.refresh(current)
    return current


def Display_all_users_infos(db: Session):
    users = db.query(user_model).all()
    return users

def Get_user_infos_by_id(user_id: UUID , db: Session ):
    user = db.query(user_model).filter( user_model.user_id == user_id ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found.")
    return user

def Get_current_user_info(current: user_model ):
    return current

def Delete_user(user_id: UUID,db: Session ):
    user = db.query(user_model).filter( user_model.user_id == user_id ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found.")
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

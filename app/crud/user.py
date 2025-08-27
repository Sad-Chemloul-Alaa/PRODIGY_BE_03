from fastapi import Depends ,Response ,HTTPException ,status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas import user as user_schemas
from app.models.user import User as user_model
from uuid import UUID

def Display_all_users_infos(db: Session = Depends(get_db)):
    users = db.query(user_model).all()
    return users

def Get_user_infos_by_id(user_id: UUID , db: Session = Depends(get_db)):
    user = db.query(user_model).filter( user_model.user_id == user_id ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user not found.")
    return user

def Update_user(user_id: UUID, data: user_schemas.UserUpdate,db: Session = Depends(get_db)):
    user = db.query(user_model).filter( user_model.user_id == user_id ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user not found.")
    existing_user = db.query(user_model).filter(user_model.user_email == data.user_email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user.user_name = data.user_name
    user.user_email= data.user_email
    user.user_age = data.user_age
    db.commit()
    return user

def Create_user(data: user_schemas.User, db: Session = Depends(get_db)):
    existing_user = db.query(user_model).filter(user_model.user_email == data.user_email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_user = user_model(user_name = data.user_name,
                               user_email= data.user_email,
                               user_age = data.user_age
                               )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def Delete_user(user_id: UUID,db: Session = Depends(get_db)):
    user = db.query(user_model).filter( user_model.user_id == user_id ).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f" user not found.")
    db.delete(user)
    db.commit()
    return {"message":"Deleted"}

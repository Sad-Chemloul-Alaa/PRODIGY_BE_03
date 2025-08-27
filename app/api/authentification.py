from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import user as user_schema
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.security.hash import hash_password, verify_password
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
from app.security.jwt import create_access_token, create_refresh_token, decode_token,get_current_user
from app.models.user import User , Role
from app.schemas.authentification import Token ,RefreshRequest
from uuid import UUID

router = APIRouter(prefix="/authentification", tags=["auth"])

@router.post("/register", response_model=user_schema.UserResponse, status_code=201)
def register(payload: user_schema.User, db: Session = Depends(get_db)):
    new_user = User(
    user_name=payload.user_name,
    user_email=payload.user_email,
    user_age=payload.user_age,
    user_hashed_password=hash_password(payload.password),
    user_role=payload.user_role if payload.user_role else Role.normal_user
    )
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_email == form.username).first()
    if not user or not verify_password(form.password, user.user_hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    user.is_active = True
    db.commit()
    return Token(
        access_token=create_access_token(str(user.user_id)),
        refresh_token=create_refresh_token(str(user.user_id)),
    )

@router.post("/refresh", response_model=Token)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    data = decode_token(payload.refresh_token)
    if data.type != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    user = db.get(User, UUID(data.sub))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive or missing user")
    return Token(
        access_token=create_access_token(UUID(user.user_id)),
        refresh_token=create_refresh_token(UUID(user.user_id)),
    )

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.is_active = False
    db.commit()
    return {"msg": "Logged out successfully"}

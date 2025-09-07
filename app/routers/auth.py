from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import init_db
from app.deps import get_db
from app.security import get_password_hash, verify_password, create_access_token

router = APIRouter()

@router.on_event("startup")
def _startup():
    init_db()

@router.post("/signup", status_code=201)
def signup(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(email=payload.email).first():
        raise HTTPException(400, "Email already registered")
    user = models.User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email}

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Ici `username` = email
    user = db.query(models.User).filter_by(email=form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

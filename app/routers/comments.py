from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.deps import get_db, get_current_user

router = APIRouter()

@router.post("/{recipe_id}", response_model=schemas.CommentOut, status_code=201)
def add_comment(recipe_id: int, body: schemas.CommentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    recipe = db.get(models.Recipe, recipe_id)
    if not recipe:
        raise HTTPException(404, "Recipe not found")
    c = models.Comment(text=body.text, rating=body.rating, author_id=user.id, recipe_id=recipe_id)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get("/for/{recipe_id}", response_model=List[schemas.CommentOut])
def list_comments(recipe_id: int, db: Session = Depends(get_db)):
    return db.query(models.Comment).filter_by(recipe_id=recipe_id).all()

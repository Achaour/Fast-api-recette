from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.deps import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.RecipeOut, status_code=201)
def create_recipe(body: schemas.RecipeCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    recipe = models.Recipe(**body.model_dump(), author_id=user.id)
    db.add(recipe); db.commit(); db.refresh(recipe)
    return recipe

@router.get("/", response_model=List[schemas.RecipeOut])
def list_recipes(
    ingredient: str | None = None,
    difficulty: str | None = Query(None, pattern="^(easy|medium|hard)$"),
    max_time: int | None = None,
    db: Session = Depends(get_db),
):
    q = db.query(models.Recipe)
    if ingredient:
        q = q.filter(models.Recipe.ingredients.ilike(f"%{ingredient}%"))
    if difficulty:
        q = q.filter(models.Recipe.difficulty == difficulty)
    if max_time is not None:
        q = q.filter(models.Recipe.prep_minutes <= max_time)
    return q.order_by(models.Recipe.id.desc()).all()

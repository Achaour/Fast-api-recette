from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

# Auth
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Recipe
class RecipeBase(BaseModel):
    title: str
    ingredients: str
    instructions: str
    prep_minutes: int = 0
    difficulty: str = Field(default="easy", pattern="^(easy|medium|hard)$")

class RecipeCreate(RecipeBase): pass

class RecipeOut(RecipeBase):
    id: int
    author_id: int
    class Config: from_attributes = True

# Comment
class CommentCreate(BaseModel):
    text: str
    rating: float = Field(ge=1, le=5)

class CommentOut(CommentCreate):
    id: int
    author_id: int
    recipe_id: int
    class Config: from_attributes = True

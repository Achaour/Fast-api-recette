from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)

    recipes = relationship("Recipe", back_populates="author", cascade="all,delete")
    comments = relationship("Comment", back_populates="author", cascade="all,delete")

class Recipe(Base):
    __tablename__ = "recipes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    ingredients: Mapped[str] = mapped_column(Text)  # simple: texte séparé par lignes
    instructions: Mapped[str] = mapped_column(Text)
    prep_minutes: Mapped[int] = mapped_column(Integer, default=0)
    difficulty: Mapped[str] = mapped_column(String, default="easy")
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    author = relationship("User", back_populates="recipes")
    comments = relationship("Comment", back_populates="recipe", cascade="all,delete")

class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(Text)
    rating: Mapped[float] = mapped_column(Float)  # 1.0–5.0
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"))

    author = relationship("User", back_populates="comments")
    recipe = relationship("Recipe", back_populates="comments")

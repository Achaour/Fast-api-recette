from fastapi import FastAPI
from app.routers import auth, recipes, comments

app = FastAPI(title="Recipes API")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/categories/{category_id}/descendants", response_model=list[schemas.CategorySchema])
def get_category_descendants(category_id: int, db: Session = Depends(get_db)):
    result = crud.get_descendants(db, category_id)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found or has no descendants")
    return result

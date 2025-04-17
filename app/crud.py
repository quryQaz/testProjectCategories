from sqlalchemy.orm import Session
from sqlalchemy import text
from . import models

def get_descendants(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        return []

    query = text("""
        SELECT * FROM categories
        WHERE path LIKE :like_path
          AND id != :category_id
    """)
    like_path = f"{category.path}%"
    result = db.execute(query, {"like_path": like_path, "category_id": category_id}).mappings()

    return [models.Category(**row) for row in result]

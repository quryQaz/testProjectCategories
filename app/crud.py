from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from . import models

def get_descendants(db: Session, category_id: int):
    query = text("""
        WITH RECURSIVE category_tree AS (
            SELECT * FROM categories WHERE id = :category_id
            UNION ALL
            SELECT c.* FROM categories c
            INNER JOIN category_tree ct ON c.parent_id = ct.id
        )
        SELECT * FROM category_tree WHERE id != :category_id;
    """)
    result = db.execute(query, {"category_id": category_id}).mappings()
        
    return [models.Category(**row) for row in result]


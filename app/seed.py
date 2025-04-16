from app.database import SessionLocal
from app.models import Category
from sqlalchemy import text

def seed():
    session = SessionLocal()

    categories = [
        {"id": 1, "name": "Электроника", "parent_id": None},
        {"id": 2, "name": "Телефоны", "parent_id": 1},
        {"id": 3, "name": "Ноутбуки", "parent_id": 1},
        {"id": 4, "name": "Смартфоны", "parent_id": 2},
        {"id": 5, "name": "Аксессуары", "parent_id": 2},
        {"id": 6, "name": "Чехлы", "parent_id": 5},
        {"id": 7, "name": "Зарядки", "parent_id": 5},
        {"id": 8, "name": "Одежда", "parent_id": None},
        {"id": 9, "name": "Мужская", "parent_id": 8},
        {"id": 10, "name": "Женская", "parent_id": 8},
    ]

    for cat in categories:
        session.merge(Category(**cat))

    session.execute(text("SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories))"))

    session.commit()

    session.close()
    print("Success")

if __name__ == "__main__":
    seed()

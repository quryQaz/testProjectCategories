from app.database import SessionLocal
from app.models import Category
from sqlalchemy import text

def create_triggers(session):

    trigger_text = """
    CREATE OR REPLACE FUNCTION set_category_path()
    RETURNS TRIGGER AS $$
    DECLARE
        parent_path TEXT;
    BEGIN
        IF NEW.parent_id IS NULL THEN
            NEW.path := '/' || NEW.id || '/';
        ELSE
            SELECT path INTO parent_path FROM categories WHERE id = NEW.parent_id;
            IF parent_path IS NULL THEN
                RAISE EXCEPTION 'Parent category not found';
            END IF;
            NEW.path := parent_path || NEW.id || '/';
        END IF;
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    CREATE TRIGGER set_path_before_insert
    BEFORE INSERT ON categories
    FOR EACH ROW
    EXECUTE FUNCTION set_category_path();
    """

    session.execute(text(trigger_text))

    trigger_update_text = """
    CREATE OR REPLACE FUNCTION update_category_path()
    RETURNS TRIGGER AS $$
    DECLARE
        new_parent_path TEXT;
        old_path TEXT;
        new_path TEXT;
    BEGIN
        IF NEW.parent_id IS DISTINCT FROM OLD.parent_id THEN
            
            IF NEW.parent_id IS NULL THEN
                new_parent_path := '/';
            ELSE
                SELECT path INTO new_parent_path FROM categories WHERE id = NEW.parent_id;
                IF new_parent_path IS NULL THEN
                    RAISE EXCEPTION 'New parent category not found';
                END IF;
            END IF;
            
            old_path := OLD.path;
            new_path := new_parent_path || NEW.id || '/';
            
            NEW.path := new_path;
            
            UPDATE categories
            SET path = new_path || substring(path FROM length(old_path) + 1)
            WHERE path LIKE old_path || '%';
            
        END IF;

        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;
    CREATE TRIGGER update_path_before_update
    AFTER UPDATE ON categories
    FOR EACH ROW
    EXECUTE FUNCTION update_category_path();
    """
    session.execute(text(trigger_update_text))


def seed():
    session = SessionLocal()

    create_triggers(session)

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

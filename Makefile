.PHONY: seed run up down

seed:
	docker-compose exec web python app/seed.py

migrate:
	docker-compose exec web alembic upgrade head

run:
	docker-compose exec web uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

up:
	docker-compose up --build

down:
	docker-compose down

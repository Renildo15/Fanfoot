migrate:
	alembic revision --autogenerate -m "$(m)"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

run:
	flet run main.py

dep:
	pip freeze > requirements.txt

populate:
	PYTHONPATH=. python scripts/populate_country.py

coach:
	PYTHONPATH=. python scripts/populate_coach.py
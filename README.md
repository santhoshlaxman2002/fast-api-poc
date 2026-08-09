uv run alembic revision --autogenerate -m "description"

uv run alembic upgrade head

uv run alembic heads

uv run alembic merge -m "merge diff heads" head_id_1 head_id_2
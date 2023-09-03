# air-receipt


Run
uvicorn --reload main:app


Open
http://127.0.0.1:8000/redoc
or
http://127.0.0.1:8000/doc

Use this to initialize empty db

alembic init -t generic  migrations
alembic revision --autogenerate -m "create inital tables"
alembic upgrade head


# use for async db connections
alembic init -t async migrations
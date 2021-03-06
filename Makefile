up:
	docker-compose up

build:
	docker-compose build

down:
	docker-compose down

test:
	pytest test

run:1
	uvicorn core.main:app --reload

init_db:
	alembic init alembic

migrate:
	#alembic revision -m 'init'
	docker-compose run web alembic upgrade head
	docker-compose run web alembic revision --autogenerate -m "New Migration"

makemigratoins:
	alembic revision -m 'init'

restart:
	#pipenv install 	graphene
#	pipenv install 	graphql-core
#	pipenv install 	graphql-relay
#	pipenv install 	greenlet

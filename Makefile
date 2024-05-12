run:
	@uvicorn store.main:app  --reload

precommit-install:
	@poetry run pre-commit install

test:
	@poetry run pytest

test-matching:
	@poetry run pytest -s -rx -k $(K) --pdb store ./tests/

run-docker:
	@docker-compose up -d

docker-check:
	@docker ps

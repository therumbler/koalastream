build:
	echo ${DOCKER_USER}
	docker build -t ${DOCKER_USER}/koalastream .

run-external:
	pipenv run uvicorn main:external_app --port=13001 --reload


unit-test:
	pipenv run pytest -s tests/unit/

test: unit-test

build:
	echo ${DOCKER_USER}
	docker build -t ${DOCKER_USER}/koalastream .

run-external:
	pipenv run uvicorn main:external_app --reload


unit-test:
	pipenv run pytest tests/unit/

test: unit-test
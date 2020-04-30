bootstrap:
	rm -rf ./env
	virtualenv -p python3 env
	env/bin/pip install poetry
	env/bin/poetry install

run:
	env/bin/uvicorn synctabs.presentation.web.app:app

run_dev:
	env/bin/uvicorn synctabs.presentation.web.app:app --reload

test:
	env/bin/mypy synctabs
	env/bin/flake8 synctabs
	env/bin/pytest -s --ff tests --cov=synctabs

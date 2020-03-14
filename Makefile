install:
	poetry install

run:
	poetry run page-loader

lint:
	poetry run flake8 page-loader

test:
	poetry run pytest --cov=page_loader tests/ --cov-report xml

build:
	poetry build

publish: build
	poetry publish -r page_loader -u $(USER) -p $(PASSWORD)



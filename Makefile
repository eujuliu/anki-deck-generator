.PHONY: format lint check

dev:
	flask run --debug

format:
	black .

lint:
	flake8 .

check: 
	black --check . && flake8 .
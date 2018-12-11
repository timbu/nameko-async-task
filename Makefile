test: flake8 pylint pytest

flake8:
	flake8 nameko_async_task test

pylint:
	pylint nameko_async_task -E

pytest:
	coverage run --source nameko_async_task --branch -m pytest test
	coverage report --show-missing --fail-under=100

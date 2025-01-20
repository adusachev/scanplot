requirements:
	poetry run pip freeze > requirements.txt && sed -i '/scanplot/d' requirements.txt

black:
	poetry run black src/scanplot

isort:
	poetry run isort src/scanplot

format:
	make black && make isort
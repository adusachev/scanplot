requirements:
	poetry export --without-hashes --format requirements.txt | awk '{ print $$1 }' FS=';' > requirements.txt

black:
	poetry run black src/scanplot

isort:
	poetry run isort src/scanplot

format:
	make black && make isort
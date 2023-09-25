generate:
	python3 generate.py
	prettier -w data.json

static: static.html

static.html: data.json index.html
	./ssg

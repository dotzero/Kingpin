all: build run

build:
	docker build --platform linux/amd64 -t kingpin .

run:
	docker run -v $(PWD):/build kingpin

files: pdf epub

pdf:
	python build_pdf.py

epub:
	python build_epub.py

.PHONY: build run files pdf epub

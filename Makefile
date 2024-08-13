# makefile

build: docker-compose build web

run: docker-compose up -d

test: pytest tests

install-test: pip install -r .\requirements-test.txt

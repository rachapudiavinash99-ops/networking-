
.PHONY: build run test

build:
	docker-compose build

run:
	docker-compose up -d

test:
	pytest backend/tests/

install:
	npm install --prefix frontend
	pip install -r backend/requirements.txt

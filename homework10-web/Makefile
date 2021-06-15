.PHONY: up
up:
	docker-compose build
	docker-compose up

.PHONY: rund
rund:
	docker-compose build
	docker-compose up -d

.PHONY: dev
dev:
	docker-compose -f docker-compose.dev.yml build
	docker-compose -f docker-compose.dev.yml up -d


.PHONY: run
run: up

.DEFAULT_GOAL := up
SHELL := /bin/bash
CWD := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
ME := $(shell whoami)

nothing:
	@echo "do nothing"

build:
	docker compose build

drop:
	docker compose down -v

up:
	docker compose up --remove-orphans --build \
		db__bot \
		broker__bot \
		app__bot \
		admin_web__bot \
		internal_api__db__bot


db__init:
	docker compose up -d --remove-orphans --build \
		db__bot \
		admin_web__bot

	docker compose build manager_db__bot
	docker compose run --rm manager_db__bot python src/bot__db/manager/manage.py init_db

db__drop:
	docker compose up -d --remove-orphans --build \
		db__bot \
		admin_web__bot

	docker compose build manager_db__bot
	docker compose run --rm manager_db__bot python src/bot__db/manager/manage.py drop_db

db__upgrade:
	docker compose up -d --remove-orphans --build \
		db__bot \
		admin_web__bot

	docker compose build manager_db__bot
	docker compose run --rm manager_db__bot python src/bot__db/manager/manage.py upgrade_db

SHELL=/bin/bash

##### Set parameters #####

HEALTH_CHECK_TIMEOUT ?= 60

##### SELF-DOCUMENTATION ####

.DEFAULT_GOAL := help
.PHONY: help

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

###### MAIN COMMANDS ######

provision: build migrate ## [Provision the project]

up: ## [Start dev environment]
	@docker-compose up

prod-up: ## [Start the production environment]
	@docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --scale lighthouse=3 -d

###### HELPERS ######

build: ## [Build it all from scratch]
	@docker-compose build --no-cache

makemigrations: ## [Create migrations for the django db]
	@docker-compose run --rm prospect manage.py makemigrations
	@docker-compose stop

migrate: ## [Apply a db migration for the django db]
	@docker-compose run --rm prospect manage.py migrate
	@docker-compose stop

dbshell: ## [Get a sqllite shell to the django database]
	@docker-compose run --rm prospect manage.py dbshell
	@docker-compose stop

deep-clean: ## [Destroys containers, images, networks and volumes]
	@docker-compose down -v --rmi all

setup-git-hooks: ## [Adds pre-commit hooks]
	git config core.hooksPath .githooks

##### Linters #####

hadolint_lint: ## [Checks validity and styling  of this repo's Dockerfiles]
	@scripts/run_hadolint

shellcheck_lint: ## [Checks validity and styling of this repo's shell script files]
	@scripts/run_shellcheck

docker-compose_lint: ## [Checks docker-compose files]
	@scripts/run_compose_lint

python_lint: ## [Checks python files]
	@scripts/run_python_lint

lint:  ## [Run all linting tasks]
	@scripts/run_linters

##### Testing #####

health-checks:
	@HEALTH_CHECK_TIMEOUT=${HEALTH_CHECK_TIMEOUT} scripts/health-check

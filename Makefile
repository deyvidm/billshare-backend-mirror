# Windows Dependant Variables
ifeq ($(OS),Windows_NT)
else
    UNAME_S := $(shell uname -s)
    UID := $(shell id -u $$(whoami))

    # OS X Dependant Variables
    ifeq ($(UNAME_S), Darwin)

    INSTALL_COMMAND := sh scripts/macos-install-latest-docker.sh
    UP_COMMAND := open -a Docker

    # GNU/Linux Depedant Variables
    else ifeq ($(UNAME_S), Linux)

    INSTALL_COMMAND := sh scripts/ubuntu-install-latest-docker.sh

    endif
endif

DJANGO_PROJECT_NAME := app

DJANGO_DOCKER_CONTAINER_NAME := app
DATABASE_DOCKER_CONTAINER_NAME := db

DOCKER_NAME := billshare
DOCKER_COMPOSE_PRODUCTION_YAML := docker-compose.prod.yml

DOCKER_COMPOSE_COMMAND := docker-compose
DOCKER_MACHINE_COMMAND := docker-machine

DOCKER_COMMAND := docker
LOCAL_CONTAINER_NAME := billsharebackend_app_1

# Make Manage
MANAGE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(MANAGE_ARGS):;@:)

.PHONY: all install up start stop ssh build manage hooks machine-export machine-import startapp

all:
	@echo Targets:
	@make -qp | awk -F':' '/^[a-zA-Z0-9][^$$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print "    "A[i]}' | grep -v Makefile | sort

install: hooks
	$(INSTALL_COMMAND)

ssh:
	$(DOCKER_COMMAND) exec -it $(LOCAL_CONTAINER_NAME) /bin/bash

up:
	$(UP_COMMAND)
	$(DOCKER_COMPOSE_COMMAND) up

start:
	$(DOCKER_COMPOSE_COMMAND) start

stop:
	$(DOCKER_COMPOSE_COMMAND) stop

build:
	$(DOCKER_COMPOSE_COMMAND) build

manage:
	$(DOCKER_COMPOSE_COMMAND) exec $(DJANGO_DOCKER_CONTAINER_NAME) python manage.py $(MANAGE_ARGS)

startapp:
	mkdir -p $(DJANGO_PROJECT_NAME)/$(MANAGE_ARGS)
	$(DOCKER_COMPOSE_COMMAND) exec --user $(UID):$(UID) $(DJANGO_DOCKER_CONTAINER_NAME) python manage.py startapp $(MANAGE_ARGS) $(DJANGO_PROJECT_NAME)/$(MANAGE_ARGS)

hooks:
	cp hooks/* .git/hooks/

machine-import:
	machine-import $(DOCKER_NAME).zip
	@echo '!! Hard Delete $(DOCKER_NAME).zip'

machine-export:
	machine-export $(DOCKER_NAME)

.PHONY: prod-connect prod-create prod-ssh prod-disconnect prod-deploy prod-stop prod-build prod-start prod-up prod-create-digital-ocean prod-recreate prod-manage

prod-deploy: prod-build prod-up prod-start

prod-start:
	$(DOCKER_COMPOSE_COMMAND) -f $(DOCKER_COMPOSE_PRODUCTION_YAML) start

prod-build:
	$(DOCKER_COMPOSE_COMMAND) -f $(DOCKER_COMPOSE_PRODUCTION_YAML) build

prod-recreate:
	$(DOCKER_COMPOSE_COMMAND) -f $(DOCKER_COMPOSE_PRODUCTION_YAML) provision

prod-up:
	$(DOCKER_COMPOSE_COMMAND) -f $(DOCKER_COMPOSE_PRODUCTION_YAML) up -d

prod-stop:
	$(DOCKER_COMPOSE_COMMAND) -f $(DOCKER_COMPOSE_PRODUCTION_YAML) stop

prod-connect:
	@echo '!! Copy the last line and manually run it in your current terminal session'
	$(DOCKER_MACHINE_COMMAND) env $(DOCKER_NAME)
	eval $$($(DOCKER_MACHINE_COMMAND) env $(DOCKER_NAME))

prod-disconnect:
	@echo '!! Copy the last line and manually run it in your current terminal session'
	eval $$($(DOCKER_MACHINE_COMMAND) env -u)

prod-manage:
	$(DOCKER_COMPOSE_COMMAND) -f $(DOCKER_COMPOSE_PRODUCTION_YAML) exec app python manage.py $(MANAGE_ARGS)

prod-create: prod-create-digital-ocean prod-up

prod-create-digital-ocean:
	$(DOCKER_MACHINE_COMMAND) create --driver=digitalocean --digitalocean-access-token=$(MANAGE_ARGS) --digitalocean-size=512mb --digitalocean-region=tor1 $(DOCKER_NAME)
# --digitalocean-ipv6=true

prod-destroy:
	$(DOCKER_MACHINE_COMMAND) rm $(DOCKER_NAME)

prod-ssh:
	$(DOCKER_MACHINE_COMMAND) ssh $(DOCKER_NAME)

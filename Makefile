# Windows Dependant Variables
ifeq ($(OS),Windows_NT)
else
    UNAME_S := $(shell uname -s)

    # OS X Dependant Variables
    ifeq ($(UNAME_S), Darwin)

    INSTALL_COMMAND := sh scripts/macos-install-latest-docker.sh
    UP_COMMAND := open -a Docker

    # GNU/Linux Depedant Variables
    else ifeq ($(UNAME_S), Linux)

    INSTALL_COMMAND := sh scripts/ubuntu-install-latest-docker.sh

    endif
endif

DOCKER_NAME := billshare

# Make Manage
MANAGE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(MANAGE_ARGS):;@:)

.PHONY: all install up start stop build manage hooks

all:
	@echo Targets:
	@make -qp | awk -F':' '/^[a-zA-Z0-9][^$$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print "    "A[i]}' | grep -v Makefile | sort

install: hooks
	$(INSTALL_COMMAND)

up:
	$(UP_COMMAND)
	docker-compose up

start:
	docker-compose start

stop:
	docker-compose stop

build:
	docker-compose build

manage:
	docker-compose exec app python manage.py $(MANAGE_ARGS)

hooks:
	cp hooks/* .git/hooks/

.PHONY: prod-connect prod-create prod-ssh prod-disconnect prod-deploy prod-stop prod-build prod-start prod-up prod-create-digital-ocean

prod-deploy: prod-stop prod-build prod-up prod-start

prod-start:
	docker-compose -f docker-compose.prod.yml start

prod-build:
	docker-compose -f docker-compose.prod.yml build

prod-up:
	docker-compose -f docker-compose.prod.yml up -d

prod-stop:
	docker-compose -f docker-compose.prod.yml stop

prod-connect:
	docker-machine env $(DOCKER_NAME)
	eval $$(docker-machine env $(DOCKER_NAME))

prod-disconnect:
	eval $$(docker-machine env -u)

prod-create: prod-create-digital-ocean prod-up

prod-create-digital-ocean:
	docker-machine create --driver=digitalocean --digitalocean-access-token=$(MANAGE_ARGS) --digitalocean-size=512mb --digitalocean-region=tor1 $(DOCKER_NAME)
# --digitalocean-ipv6=true

prod-destroy:
	docker-machine rm $(DOCKER_NAME)

prod-ssh:
	docker-machine ssh $(DOCKER_NAME)

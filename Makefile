# Windows Dependant Variables
ifeq ($(OS),Windows_NT)
else
    UNAME_S := $(shell uname -s)

    # OS X Dependant Variables
    ifeq ($(UNAME_S), Darwin)

    INSTALL_COMMAND := sh macos-install-latest-docker.sh

    # GNU/Linux Depedant Variables
    else ifeq ($(UNAME_S), Linux)

    INSTALL_COMMAND := sh ubuntu-install-latest-docker.sh

    endif
endif

.PHONY: all install up start stop build migrate

all:
	@echo Targets:
	@make -qp | awk -F':' '/^[a-zA-Z0-9][^$$#\/\t=]*:([^=]|$$)/ {split($$1,A,/ /);for(i in A)print "    "A[i]}' | grep -v Makefile | sort

install:
	$(INSTALL_COMMAND)

up:
	docker-compose up

start:
	docker-compose start

stop:
	docker-compose stop

build:
	docker-compose build

migrate:
	docker-compose exec web python manage.py migrate

.PHONY: up start stop build migrate

up:
	sudo docker-compose up

start:
	sudo docker-compose start

stop:
	sudo docker-compose stop

build:
	sudo docker-compose build

migrate:
	sudo docker-compose exec web python manage.py migrate


# Bill Share Django Backend

Group expense sharing app - [billshare.io](https://billshare.io/) django backend

## Installation

1. Docker, docker-compose, docker-machine
2. Python3, Django, PEP8

```Bash
make install
```

Or try to manually install docker: https://www.docker.com/get-docker

## Starting Docker

```Bash
make up
```

> Check `0.0.0.0:3000` to see if server is up and running

## Basic Docker Commands

```Bash
# Run docker-compose build
make build

# Copy git hooks to .git
make hooks

# Run docker-compose start
make start

# Run docker-compose stop
make stop
```

## Django Manage

```Bash
make manage <command1> <command2> ...

# make manage migrate
# make manage makemigrations
# make manage dbshell
# make manage shell
```

## Creating Apps

```Bash
make startapp <app-name>
```

## Production Access

### Getting Setup

1. Get \<machine-name\>.zip from DevOps (using `machine-share`)

2. Import \<machine-name\> using `machine-share`

```Bash
npm install -g machine-share
make machine-import
```

### Connecting to Production

* Set local environment to \<machine-name\>

```Bash
# Copy the last command and run it in your current shell
make prod-connect
# You can disconnect with `make prod-disconnect` same as above
```

### Deploying to Production

* Make sure your current branch is on master with no extra files

```Bash
make prod-deploy
```

### Creating Server (Droplet, EC2 instance)

* This costs money

```Bash
make prod-create <DO-or-AWS-auth-token>
```

### Reprovisioning or Destroying Server

```Bash
# Reprovision current instance (keeps DO static IP, usually best to do this)
make prod-recreate

# Completely destroys current instance, you lose everything
make prod-destroy
```

### Other Production commands

```Bash
# docker-compose build
make prod-build

# docker-compose start
make prod-start

# docker-compose stop
make prod-stop

# docker-compose up -d
make prod-up

# SSH to server
make prod-ssh
```

## Development Environment Debugging

### Docker Can't Access Project Files (manage.py)

Usually a problem on Linux

#### Error Messages

`python: can't open file 'manage.py': [Errno 2]`

#### Solution 1

Set Docker User (on Linux)

```Bash
sudo groupadd docker
sudo gpasswd -a $USER docker
newgrp docker
# Log out, back in may help, or restart computer
```

#### Solution 2

Run Docker commands as Sudo

```Bash
sudo docker-compose up
```

### App Not Accessible From browser

Usually means a syntax or "code" error, currently `make up` does not show _all_ Django errors

#### Solution 1

* Get back to a good state, checkout master
* Once in a good state, change code back to bad state, and `make up` output might show errors

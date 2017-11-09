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

> Check `127.0.0.1:3000` to see if server is up and running

## Rebuilding Docker

```Bash
make build
make up
```

## Basic Docker Commands

```Bash
# SSH into the local container
make ssh

# Run docker-compose build, rebuilds when you make docker-level changes
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

# Nuke the database
# make manage flush
# make manage sqlmigrate app_name 0001
```

### Check Django Security

> Connect to production to run against prod settings

```Bash
make manage check '\-\-deploy'
```

> https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

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
make prod-manage <command1> <command2> ...

# make prod-manage migrate
# make prod-manage dbshell
# make prod-manage shell

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

## Manual DevOps Server Settings

### Server Firewall

Inbound rules are for SSH, Docker Swarm, HTTPS, HTTP, API Port

```Bash
Inbound Rules
Type    Protocol    Port Range  Destinations
SSH     TCP         22          All IPv4 All IPv6
HTTP    TCP         80          All IPv4 All IPv6
HTTPS   TCP         443         All IPv4 All IPv6
Custom  TCP         2376        All IPv4 All IPv6
Custom  TCP         2377        All IPv4 All IPv6
Custom  TCP         3000        All IPv4 All IPv6
Custom  TCP         7946        All IPv4 All IPv6
Custom  UDP         4789        All IPv4 All IPv6
Custom  UDP         7946        All IPv4 All IPv6

Outbound Rules
Type        Protocol    Port Range  Destinations
ICMP        ICMP            -       All IPv4 All IPv6
All TCP     TCP         All ports   All IPv4 All IPv6
All UDP     UDP         All ports   All IPv4 All IPv6
```

### Namecheap

```Bash
Type        Host            Value                   TTL
A Record    @               <IP Address>            Automatic
A Record    www             <IP Address>            Automatic
NS Record   billshare.io    ns3.digitalocean.com.   Automatic
NS Record   billshare.io    ns1.digitalocean.com.   Automatic
NS Record   billshare.io    ns2.digitalocean.com.   Automatic
```

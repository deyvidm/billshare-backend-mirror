#!/usr/bin/env bash

# https://gist.github.com/wdullaer/f1af16bd7e970389bad3

# Ask for the user password
# Script only works if sudo caches the password for a few minutes
sudo true

# Add docker to USER to allow non-sudo docker-compose up
sudo groupadd docker
sudo gpasswd -a $USER docker

# Install Python reqs
sudo apt install python3 && pip3 install django pep8

# Install kernel extra's to enable docker aufs support
# sudo apt-get -y install linux-image-extra-$(uname -r)

# Add Docker PPA and install latest version
# sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
# sudo sh -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
# sudo apt-get update
# sudo apt-get install lxc-docker -y

# Alternatively you can use the official docker install script
wget -qO- https://get.docker.com/ | sh

# Install docker-compose
COMPOSE_VERSION=`git ls-remote https://github.com/docker/compose | grep refs/tags | grep -oP "[0-9]+\.[0-9][0-9]+\.[0-9]+$" | tail -n 1`
sudo sh -c "curl -L https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose"
sudo chmod +x /usr/local/bin/docker-compose
sudo sh -c "curl -L https://raw.githubusercontent.com/docker/compose/${COMPOSE_VERSION}/contrib/completion/bash/docker-compose > /etc/bash_completion.d/docker-compose"

# Install docker-machine
MACHINE_VERSION=`git ls-remote https://github.com/docker/machine | grep refs/tags | grep -oP "[0-9]+\.[0-9][0-9]+\.[0-9]+$" | tail -n 1`
curl -L https://github.com/docker/machine/releases/download/v${MACHINE_VERSION}/docker-machine-`uname -s`-`uname -m` >/tmp/docker-machine &&
chmod +x /tmp/docker-machine &&
sudo cp /tmp/docker-machine /usr/local/bin/docker-machine

# Install docker-cleanup command
#cd /tmp
#git clone https://gist.github.com/76b450a0c986e576e98b.git
#cd 76b450a0c986e576e98b
#sudo mv docker-cleanup /usr/local/bin/docker-cleanup
#sudo chmod +x /usr/local/bin/docker-cleanup

sudo mv ubuntu-docker-cleanup.sh /usr/local/bin/docker-cleanup
sudo chmod +x /usr/local/bin/docker-cleanup
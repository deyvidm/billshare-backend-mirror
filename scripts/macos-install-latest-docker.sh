#!/usr/bin/env bash

if ! brew info cask &>/dev/null; then
  echo "No Brew Cask (Homebrew Extension)"
  exit 1
fi

#Docker
brew cask install docker
brew cask install docker-compose
brew cask install docker-machine

# Python Items
brew install python3
pip3 install Django
pip3 install pep8
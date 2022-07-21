# Base Python Architecture

[![Python Syntax Check and Docker Image](https://github.com/SteinPrograms/base-python-architecture/actions/workflows/workflow.yml/badge.svg)](https://github.com/SteinPrograms/base-python-architecture/actions/workflows/workflow.yml)

Stein programs python algorithm is aiming for high frequency arbitrage between dapps
until now it has been a crypto trading algorithm following rules passed inside a database with buy and sell levels

To get the variable on local systems (M1) use :

```sh
export $(grep -v '^#' .env | xargs)
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```

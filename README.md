# Base Python Architecture

[![Python Syntax Check and Docker Image](https://github.com/SteinPrograms/base-python-architecture/actions/workflows/workflow.yml/badge.svg)](https://github.com/SteinPrograms/base-python-architecture/actions/workflows/workflow.yml)

Stein programs python algorithm is aiming for high frequency arbitrage between dapps
until now it has been a crypto trading algorithm following rules passed inside a database with buy and sell levels

To get the variable on local systems (M1) use :

```sh
export $(grep -v '^#' .env | xargs)
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```

Entry and exit explanation :
    Calculation of the variation between trade 1 and trade final on agregation price change
    If there is a higher price change than usual in long positions (in the top 95% of the volatitlty registered) -> buy entry
    If there is ____ in short positions -> exit trigger
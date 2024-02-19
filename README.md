# Base Python Architecture

[![Python Syntax Check and Docker Image](https://github.com/SteinPrograms/base-python-architecture/actions/workflows/workflow.yml/badge.svg)](https://github.com/SteinPrograms/base-python-architecture/actions/workflows/workflow.yml)

## Details

### Motivations

Stein programs python algorithm is aiming for high frequency arbitrage between dapps
until now it has been a crypto trading algorithm following rules passed inside a database with buy and sell levels

### Why open sourcing ?

This repository hosts all algorithms used by Stein Programs. They are built under open source license in order to ensure auditability and allow trading community to grow towards algorithmic methodology.

My moto is "you miss 100% of the shots you don't take", this means that if I want to do something and I hesitate, I should do it anyway.

## Credits

In fact, if you find this repository useful in someway, feel free to reach at : <a href="mailto:h2menez@gmail.com">this mail address</a>

## Code rules

In life, communication is the hardest skill to master. I try to master code communication at its best and I try to follow PEP recommendation as much as possible. That's why I added a pylint workflow which checks code quality.

## Algorithm targets

As said above, this repository hosts all different trading algorithm built on top of python language.
Here is a list of different algorithm

- Ichimoku Trading Style
- Moving Average (finding best strategy through a backtesting algorithm before running)

## Troubleshoot

To get the variable on local systems (M1) use :

```sh
export $(grep -v '^#' .env | xargs)
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```

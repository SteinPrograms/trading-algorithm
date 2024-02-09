# Realtime News API

[![Python Syntax Check and Docker Image](https://github.com/SteinPrograms/base-python-architecture/actions/workflows/workflow.yml/badge.svg)](https://github.com/SteinPrograms/base-python-architecture/actions/workflows/workflow.yml)

## Details

### Motivations

Getting machine readable news data is either hard or expensive.
My goal is to make it accessible to everyone and for cheap.

Having relevent data about the market, and the ability to interpret the news is extremely important in trading. 

Indeed, some strategies are only based on technical analysis but required tons of backtesting and are not reliable enough to keep running without serious overlook.

That's why I strive to develop a trading algorithm which behaves as human do, without the emotional over reaction. A trading algorithm with the sharp analysis of the human brain has no emotion but understands them.

### Why open sourcing ?

This repository hosts all algorithms used by Stein Programs. They are built under open source license in order to ensure auditability and allow trading community to grow towards algorithmic methodology.

My moto is "you miss 100% of the shots you don't take", this means that if you want to do something and you hesitate, you should do it anyway.

By no means, this repository consists of financial advice. By running any algorithm hosted on this repository you expose your self to possible financial losses.

## Credits

If you find this repository useful in someway, feel free to reach at : <a href="mailto:h2menez@gmail.com">this mail address</a>

## Code rules

In life, communication is the hardest skill to master. 
Trying to master code communication at its best and to follow PEP recommendation as much as possible is important. 
There is a pylint workflow which checks code quality before anything gets to production.

The project is also translated to rely on python types.

## Troubleshoot

To get the variable on local systems (M1) use :

```sh
export $(grep -v '^#' .env | xargs)
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```

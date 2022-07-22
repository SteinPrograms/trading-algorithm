# Using python latest docker image
FROM python:alpine3.15

# Defining the working directory
WORKDIR /usr/src

# Adding files
ADD ./app ./app
COPY ./requirements.txt ./


RUN apk add build-base
RUN apk add libffi-dev

# Creating virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Upgrading pip
RUN pip install --upgrade pip

# Installing requirements
RUN pip install --no-cache-dir -r requirements.txt

# Defining timezone to work correctly when using time in python
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Finally running the script
CMD [ "python", "app" ]
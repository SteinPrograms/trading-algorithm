# Using python 3.10 docker image
FROM python:3.10

# Defining the working directory
WORKDIR /usr/src/app

# Adding files
ADD ./app ./
COPY ./requirements.txt ./

# Upgrading pip and installing dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Defining timezone to work correctly when using time in python
ENV TZ=Europe/Paris
ENV VIRTUAL_ENV=/opt/venv
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Finally running the script
CMD ["bash", "-c", "python3 /usr/app/main.py"]
# Using python 3.10 docker image
FROM python:3.10

# Defining the working directory
WORKDIR /usr/src/app

# Adding files
ADD ./app ./
COPY ./requirements.txt ./

# Upgrading pip
RUN pip install --upgrade pip

# Creating virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Installing requirements
RUN pip install --no-cache-dir -r requirements.txt

# Defining timezone to work correctly when using time in python
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Finally running the script
CMD ["python","-u","main.py"]
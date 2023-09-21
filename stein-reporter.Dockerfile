# Using python latest docker image
FROM python
# Defining the working directory
WORKDIR /usr/src

# Adding files
ADD ./reporter ./app
ADD ./helpers ./app/helpers

# Upgrading pip
RUN pip install --upgrade pip
# Installing requirements
RUN pip install --no-cache-dir -r ./app/requirements.txt

# Defining timezone to work correctly when using time in python
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Finally running the script
CMD [ "python", "app" ]
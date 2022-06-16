FROM python:3.10

RUN apt-get update\
	&& apt-get install -y --no-install-recommends \
	vim


ENV TZ=Europe/Paris
ENV VIRTUAL_ENV=/opt/venv

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone



ADD ./app /usr/app
ADD ./requirements.txt .

RUN python -m  pip install --upgrade pip && \
    python -m  pip install --no-cache-dir -r requirements.txt

CMD ["bash", "-c", "python3 /usr/app/main.py"]  
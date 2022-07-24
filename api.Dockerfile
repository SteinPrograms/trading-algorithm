# 
FROM python:3.9

# 
WORKDIR /code

# 
COPY ./api.requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./api /code/app

# 
CMD ["python", "/code/app/main.py"]

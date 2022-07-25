# 
FROM python:3.9

# 
WORKDIR /code

# 
ADD ./api /code/app

# 
RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt

#
CMD ["python", "/code/app/main.py"]

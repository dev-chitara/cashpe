# Dockerfile

# pull the official docker image
FROM python:3.11

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependancies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /app

# exposing port
EXPOSE 8000

# running command
CMD ["python", "main.py"]


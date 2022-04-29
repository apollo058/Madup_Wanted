FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR  /usr/src/app
COPY requirements.txt /usr/src/app
RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc
RUN pip install -r requirements.txt
COPY . .
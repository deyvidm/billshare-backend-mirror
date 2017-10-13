FROM python:3
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

ADD . /app/
EXPOSE 3000
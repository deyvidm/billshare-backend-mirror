FROM ubuntu:latest
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
ADD manage.py /app/

RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        postgresql \
        postgresql-contrib

RUN cd /usr/local/bin && \
    ln -s /usr/bin/python3 python && \
    pip3 install --upgrade pip

RUN pip install -r requirements.txt

COPY config/app/prod/uwsgi.ini /app/uwsgi.ini
ADD app /app/app

CMD ["uwsgi", "--ini", "/app/uwsgi.ini"]
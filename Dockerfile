FROM python:3
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/

RUN apt-get update && \
    apt-get install -y \
        postgresql \
        postgresql-contrib \
        nginx \
        supervisor
RUN pip install -r requirements.txt

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/default
COPY supervisor-app.conf /etc/supervisor/conf.d/

ADD . /app/
EXPOSE 3000

CMD ["supervisord", "-n"]
FROM nginx:latest

RUN mkdir /nginx
WORKDIR /nginx

COPY config/nginx/dev/uwsgi_params /nginx/
COPY config/nginx/dev/nginx-app.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
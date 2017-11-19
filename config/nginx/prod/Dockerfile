FROM nginx:latest

RUN mkdir /nginx
WORKDIR /nginx

COPY config/nginx/prod/uwsgi_params /nginx/
COPY config/nginx/prod/nginx-app.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
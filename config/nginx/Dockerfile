FROM nginx:latest

RUN mkdir /nginx
WORKDIR /nginx

COPY config/nginx/uwsgi_params /nginx/
COPY config/nginx/nginx-app.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]